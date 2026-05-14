#!/usr/bin/env python
"""
Prediction service that adapts the `predict()` logic from the GUI `final_pred.py`.

This service:
 - accepts POST /predict with JSON { "image": "data:image/jpeg;base64,..." }
 - detects hand(s) using cvzone HandDetector
 - builds the 400x400 white hand skeleton image used by the model
 - runs the Keras model and applies the same heuristics as `final_pred.py`
 - returns { label: <string or null>, confidence: <float> }

Run:
  pip install -r requirements.txt
  python predict_service.py

By default the service listens on 127.0.0.1:5001
"""
import base64
import io
import os
import traceback
from typing import Optional, Tuple

from PIL import Image
import numpy as np
import enchant
from flask import Flask, request, jsonify
from flask_cors import CORS

from tensorflow.keras.models import load_model
import mediapipe as mp
import cv2


APP_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(APP_DIR, 'cnn8grps_rad1_model.h5')

app = Flask(__name__)
CORS(app)

try:
    ddd = enchant.Dict("en_US")
except Exception as e:
    print("Warning: enchant not available. Suggestions disabled.")
    ddd = None

mp_hands = mp.solutions.hands
hands1 = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
hands2 = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

offset = 29
confidence_threshold = 0.25

MODEL = None
INPUT_H = INPUT_W = None


def ensure_model_loaded():
    global MODEL, INPUT_H, INPUT_W
    if MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        MODEL = load_model(MODEL_PATH)
        shape = MODEL.input_shape
        INPUT_H = int(shape[1])
        INPUT_W = int(shape[2])


def decode_data_url_to_cvimg(data_url: str) -> np.ndarray:
    if ',' in data_url:
        _, b64 = data_url.split(',', 1)
    else:
        b64 = data_url
    data = base64.b64decode(b64)
    pil = Image.open(io.BytesIO(data)).convert('RGB')
    arr = np.array(pil)
    # convert RGB to BGR for cv2
    img = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    img = cv2.flip(img, 1)
    return img


def build_white_hand_image_and_pts(cvimg: np.ndarray) -> Tuple[Optional[np.ndarray], Optional[list]]:
    """Detect hand, produce a 400x400 white image with skeleton as in final_pred and return pts list (21 landmarks).
    Returns (res_image, pts) or (None, None) if no hand detected.
    """
    # PASS 1: Extract initial bounding box from full frame
    img_rgb = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
    results1 = hands1.process(img_rgb)
    
    if not results1.multi_hand_landmarks:
        return None, None

    hand_landmarks1 = results1.multi_hand_landmarks[0]
    img_h, img_w, _ = img_rgb.shape
    
    xList = [int(lm.x * img_w) for lm in hand_landmarks1.landmark]
    yList = [int(lm.y * img_h) for lm in hand_landmarks1.landmark]
    xmin, xmax = min(xList), max(xList)
    ymin, ymax = min(yList), max(yList)
    boxW, boxH = xmax - xmin, ymax - ymin
    
    # Apply exact cvzone default padding (20px) to match original bounding box size
    padding = 20
    x, y, w, h = xmin - padding, ymin - padding, boxW + (padding * 2), boxH + (padding * 2)
    
    # Apply original code's crop offset
    x1 = max(0, x - offset)
    y1 = max(0, y - offset)
    x2 = min(img_w, x + w + offset)
    y2 = min(img_h, y + h + offset)
    
    if x2 <= x1 or y2 <= y1:
        return None, None

    image_crop = cvimg[y1:y2, x1:x2]
    rgb_crop = cv2.cvtColor(image_crop, cv2.COLOR_BGR2RGB)
    
    # PASS 2: Process the tight crop to generate highly detailed landmarks matching the CNN
    results2 = hands2.process(rgb_crop)
    
    if not results2.multi_hand_landmarks:
        return None, None

    hand_landmarks2 = results2.multi_hand_landmarks[0]
    crop_h, crop_w, _ = rgb_crop.shape
    
    pts = []
    for lm in hand_landmarks2.landmark:
        pts.append((int(lm.x * crop_w), int(lm.y * crop_h)))
        
    # Re-apply exact offset math from the original predict_service.py
    os_ = ((400 - w) // 2) - 15
    os1 = ((400 - h) // 2) - 15
    
    white = np.ones((400, 400, 3), np.uint8) * 255
    
    for start, end in [(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),(13,14),(14,15),(15,16),(17,18),(18,19),(19,20)]:
        cv2.line(white, (pts[start][0] + os_, pts[start][1] + os1), (pts[end][0] + os_, pts[end][1] + os1), (0,255,0), 3)
    for conn in [(0,1),(0,5),(5,9),(9,13),(13,17),(17,0),(0,17)]:
        cv2.line(white, (pts[conn[0]][0] + os_, pts[conn[0]][1] + os1), (pts[conn[1]][0] + os_, pts[conn[1]][1] + os1), (0,255,0), 3)
    for i in range(21):
        cv2.circle(white, (pts[i][0] + os_, pts[i][1] + os1), 3, (0,0,255), -1)

    cv2.imwrite("debug_api.png", white)
    return white, pts


def predict_from_white_image(res_image: np.ndarray, pts: list) -> Tuple[Optional[str], float]:
    """Apply the model and heuristics from final_pred to return (label, confidence).
    Returns label (str) or None and confidence float.
    """
    ensure_model_loaded()
    img = res_image.copy()
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.resize(img, (INPUT_W, INPUT_H))
    # Convert directly to normalized float32
    inp = img.astype('float32') / 255.0
    inp = np.expand_dims(inp, axis=0)

    preds = MODEL.predict(inp, verbose=0)[0]
    max_prob = float(np.max(preds))
    if max_prob < confidence_threshold:
        return None, max_prob

    ch1_idx = int(np.argmax(preds))
    ch1 = ch1_idx

    prob = preds.copy()
    prob[ch1] = 0
    ch2 = int(np.argmax(prob))
    prob[ch2] = 0
    ch3 = int(np.argmax(prob))

    pl = [ch1, ch2]

    # The following heuristics are ported from final_pred.py
    # Note: pts is a list of [x,y] pairs
    def dist(a,b):
        return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5

    # various conditions from original file
    l = [[5, 2], [5, 3], [3, 5], [3, 6], [3, 0], [3, 2], [6, 4], [6, 1], [6, 2], [6, 6], [6, 7], [6, 0], [6, 5],
         [4, 1], [1, 0], [1, 1], [6, 3], [1, 6], [5, 6], [5, 1], [4, 5], [1, 4], [1, 5], [2, 0], [2, 6], [4, 6],
         [1, 0], [5, 7], [1, 6], [6, 1], [7, 6], [2, 5], [7, 1], [5, 4], [7, 0], [7, 5], [7, 2]]
    if pl in l:
        try:
            if (pts[6][1] < pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]):
                ch1 = 0
        except Exception:
            pass

    l = [[2,2],[2,1]]
    if pl in l:
        try:
            if (pts[5][0] < pts[4][0]):
                ch1 = 0
        except Exception:
            pass

    l = [[0,0],[0,6],[0,2],[0,5],[0,1],[0,7],[5,2],[7,6],[7,1]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[0][0] > pts[8][0] and pts[0][0] > pts[4][0] and pts[0][0] > pts[12][0] and pts[0][0] > pts[16][0] and pts[0][0] > pts[20][0]) and pts[5][0] > pts[4][0]:
                ch1 = 2
        except Exception:
            pass

    l = [[6,0],[6,6],[6,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if dist(pts[8], pts[16]) < 52:
                ch1 = 2
        except Exception:
            pass

    l = [[1,4],[1,5],[1,6],[1,3],[1,0]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[6][1] > pts[8][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1] and pts[0][0] < pts[8][0] and pts[0][0] < pts[12][0] and pts[0][0] < pts[16][0] and pts[0][0] < pts[20][0]:
                ch1 = 3
        except Exception:
            pass

    l = [[4,6],[4,1],[4,5],[4,3],[4,7]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[4][0] > pts[0][0]:
                ch1 = 3
        except Exception:
            pass

    l = [[5,3],[5,0],[5,7],[5,4],[5,2],[5,1],[5,5]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[2][1] + 15 < pts[16][1]:
                ch1 = 3
        except Exception:
            pass

    l = [[6,4],[6,1],[6,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if dist(pts[4], pts[11]) > 55:
                ch1 = 4
        except Exception:
            pass

    l = [[1,4],[1,6],[1,1]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (dist(pts[4], pts[11]) > 50) and (pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]):
                ch1 = 4
        except Exception:
            pass

    l = [[3,6],[3,4]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[4][0] < pts[0][0]):
                ch1 = 4
        except Exception:
            pass

    l = [[2,2],[2,5],[2,4]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[1][0] < pts[12][0]):
                ch1 = 4
        except Exception:
            pass

    l = [[3,6],[3,5],[3,4]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]) and pts[4][1] > pts[10][1]:
                ch1 = 5
        except Exception:
            pass

    l = [[3,2],[3,1],[3,6]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[4][1] + 17 > pts[8][1] and pts[4][1] + 17 > pts[12][1] and pts[4][1] + 17 > pts[16][1] and pts[4][1] + 17 > pts[20][1]:
                ch1 = 5
        except Exception:
            pass

    l = [[4,4],[4,5],[4,2],[7,5],[7,6],[7,0]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[4][0] > pts[0][0]:
                ch1 = 5
        except Exception:
            pass

    l = [[0,2],[0,6],[0,1],[0,5],[0,0],[0,7],[0,4],[0,3],[2,7]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[0][0] < pts[8][0] and pts[0][0] < pts[12][0] and pts[0][0] < pts[16][0] and pts[0][0] < pts[20][0]:
                ch1 = 5
        except Exception:
            pass

    l = [[5,7],[5,2],[5,6]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[3][0] < pts[0][0]:
                ch1 = 7
        except Exception:
            pass

    l = [[4,6],[4,2],[4,4],[4,1],[4,5],[4,7]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[6][1] < pts[8][1]:
                ch1 = 7
        except Exception:
            pass

    l = [[6,7],[0,7],[0,1],[0,0],[6,4],[6,6],[6,5],[6,1]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[18][1] > pts[20][1]:
                ch1 = 7
        except Exception:
            pass

    l = [[0,4],[0,2],[0,3],[0,1],[0,6]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[5][0] > pts[16][0]:
                ch1 = 6
        except Exception:
            pass

    l = [[7,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[18][1] < pts[20][1] and pts[8][1] < pts[10][1]:
                ch1 = 6
        except Exception:
            pass

    l = [[2,1],[2,2],[2,6],[2,7],[2,0]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if dist(pts[8], pts[16]) > 50:
                ch1 = 6
        except Exception:
            pass

    l = [[4,6],[4,2],[4,1],[4,4]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if dist(pts[4], pts[11]) < 60:
                ch1 = 6
        except Exception:
            pass

    l = [[1,4],[1,6],[1,0],[1,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[5][0] - pts[4][0] - 15 > 0:
                ch1 = 6
        except Exception:
            pass

    l = [[5,0],[5,1],[5,4],[5,5],[5,6],[6,1],[7,6],[0,2],[7,1],[7,4],[6,6],[7,2],[5,0],[6,3],[6,4],[7,5],[7,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] > pts[20][1]):
                ch1 = 1
        except Exception:
            pass

    l = [[6,1],[6,0],[0,3],[6,4],[2,2],[0,6],[6,2],[7,6],[4,6],[4,1],[4,2],[0,2],[7,1],[7,4],[6,6],[7,2],[7,5],[7,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[6][1] < pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] > pts[20][1]):
                ch1 = 1
        except Exception:
            pass

    l = [[6,1],[6,0],[4,2],[4,1],[4,6],[4,4]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] > pts[20][1]):
                ch1 = 1
        except Exception:
            pass

    l = [[5,0],[3,4],[3,0],[3,1],[3,5],[5,5],[5,4],[5,1],[7,6]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if ((pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]) and (pts[2][0] < pts[0][0]) and pts[4][1] > pts[14][1]):
                ch1 = 1
        except Exception:
            pass

    l = [[4,1],[4,2],[4,4]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (dist(pts[4], pts[11]) < 50) and (pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]):
                ch1 = 1
        except Exception:
            pass

    l = [[3,4],[3,0],[3,1],[3,5],[3,6]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if ((pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]) and (pts[2][0] < pts[0][0]) and pts[14][1] < pts[4][1]):
                ch1 = 1
        except Exception:
            pass

    l = [[6,6],[6,4],[6,1],[6,2]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[5][0] - pts[4][0] - 15 < 0:
                ch1 = 1
        except Exception:
            pass

    l = [[5,4],[5,5],[5,1],[0,3],[0,7],[5,0],[0,2],[6,2],[7,5],[7,1],[7,6],[7,7]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if ((pts[6][1] < pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] > pts[20][1])):
                ch1 = 1
        except Exception:
            pass

    l = [[1,5],[1,7],[1,1],[1,6],[1,3],[1,0]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if (pts[4][0] < pts[5][0] + 15) and (pts[6][1] < pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] > pts[20][1]):
                ch1 = 7
        except Exception:
            pass

    l = [[5,5],[5,0],[5,4],[5,1],[4,6],[4,1],[7,6],[3,0],[3,5]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if ((pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1])) and pts[4][1] < pts[9][1]:
                ch1 = 1
        except Exception:
            pass

    l = [[3,5],[3,0],[3,6],[5,1],[4,1],[2,0],[5,0],[5,5]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if not (pts[0][0] + 13 < pts[8][0] and pts[0][0] + 13 < pts[12][0] and pts[0][0] + 13 < pts[16][0] and pts[0][0] + 13 < pts[20][0]) and not (pts[0][0] > pts[8][0] and pts[0][0] > pts[12][0] and pts[0][0] > pts[16][0] and pts[0][0] > pts[20][0]) and dist(pts[4], pts[11]) < 50:
                ch1 = 1
        except Exception:
            pass

    l = [[5,0],[5,5],[0,1]]
    pl = [ch1, ch2]
    if pl in l:
        try:
            if pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1]:
                ch1 = 1
        except Exception:
            pass

    # final stage: map numeric ch1 to letters/special tokens
    if ch1 == 0:
        ch = 'S'
        try:
            if pts[4][0] < pts[6][0] and pts[4][0] < pts[10][0] and pts[4][0] < pts[14][0] and pts[4][0] < pts[18][0]:
                ch = 'A'
            if pts[4][0] > pts[6][0] and pts[4][0] < pts[10][0] and pts[4][0] < pts[14][0] and pts[4][0] < pts[18][0] and pts[4][1] < pts[14][1] and pts[4][1] < pts[18][1]:
                ch = 'T'
            if pts[4][1] > pts[8][1] and pts[4][1] > pts[12][1] and pts[4][1] > pts[16][1] and pts[4][1] > pts[20][1]:
                ch = 'E'
            if pts[4][0] > pts[6][0] and pts[4][0] > pts[10][0] and pts[4][0] > pts[14][0] and pts[4][1] < pts[18][1]:
                ch = 'M'
            if pts[4][0] > pts[6][0] and pts[4][0] > pts[10][0] and pts[4][1] < pts[18][1] and pts[4][1] < pts[14][1]:
                ch = 'N'
        except Exception:
            ch = 'S'
        return ch, max_prob

    if ch1 == 2:
        try:
            if dist(pts[12], pts[4]) > 42:
                return 'C', max_prob
            else:
                return 'O', max_prob
        except Exception:
            return 'O', max_prob

    if ch1 == 3:
        try:
            if dist(pts[8], pts[12]) > 72:
                return 'G', max_prob
            else:
                return 'H', max_prob
        except Exception:
            return 'H', max_prob

    if ch1 == 7:
        try:
            if dist(pts[8], pts[4]) > 42:
                return 'Y', max_prob
            else:
                return 'J', max_prob
        except Exception:
            return 'J', max_prob

    if ch1 == 4:
        return 'L', max_prob

    if ch1 == 6:
        return 'X', max_prob

    if ch1 == 5:
        try:
            if pts[4][0] > pts[12][0] and pts[4][0] > pts[16][0] and pts[4][0] > pts[20][0]:
                if pts[8][1] < pts[5][1]:
                    return 'Z', max_prob
                else:
                    return 'Q', max_prob
            else:
                return 'P', max_prob
        except Exception:
            return 'P', max_prob

    if ch1 == 1:
        try:
            if (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] > pts[20][1]):
                return 'B', max_prob
            if (pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]):
                return 'D', max_prob
            if (pts[6][1] < pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] > pts[20][1]):
                return 'F', max_prob
            if (pts[6][1] < pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] > pts[20][1]):
                return 'I', max_prob
            if (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] < pts[20][1]):
                return 'W', max_prob
            if (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]) and pts[4][1] < pts[9][1]:
                return 'K', max_prob
            if ((dist(pts[8], pts[12]) - dist(pts[6], pts[10])) < 8) and (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]):
                return 'U', max_prob
            if ((dist(pts[8], pts[12]) - dist(pts[6], pts[10])) >= 8) and (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]) and (pts[4][1] > pts[9][1]):
                return 'V', max_prob
            if (pts[8][0] > pts[12][0]) and (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] < pts[20][1]):
                return 'R', max_prob
        except Exception:
            pass

    # special tokens
    try:
        if ch1 in [1, 'E', 'S', 'X', 'Y', 'B']:
            if (pts[6][1] > pts[8][1] and pts[10][1] < pts[12][1] and pts[14][1] < pts[16][1] and pts[18][1] > pts[20][1]):
                return ' ', max_prob
    except Exception:
        pass

    try:
        if ch1 in ['E', 'Y', 'B']:
            if (pts[4][0] < pts[5][0]) and (pts[6][1] > pts[8][1] and pts[10][1] > pts[12][1] and pts[14][1] > pts[16][1] and pts[18][1] > pts[20][1]):
                return 'next', max_prob
    except Exception:
        pass

    try:
        if ch1 in ['next', 'B', 'C', 'H', 'F', 'X']:
            if (pts[0][0] > pts[8][0] and pts[0][0] > pts[12][0] and pts[0][0] > pts[16][0] and pts[0][0] > pts[20][0]) and (pts[4][1] < pts[8][1] and pts[4][1] < pts[12][1] and pts[4][1] < pts[16][1] and pts[4][1] < pts[20][1]) and (pts[4][1] < pts[6][1] and pts[4][1] < pts[10][1] and pts[4][1] < pts[14][1] and pts[4][1] < pts[18][1]):
                return 'Backspace', max_prob
    except Exception:
        pass

    # fallback: map numeric index 0-25 to A-Z (if reached here)
    try:
        if isinstance(ch1, int) and 0 <= ch1 < 26:
            return chr(ord('A') + ch1), max_prob
    except Exception:
        pass

    return None, max_prob


@app.route('/predict', methods=['POST'])
def predict():
    try:
        payload = request.get_json(force=True)
        image_b64 = payload.get('image')
        if not image_b64:
            return jsonify({'error': 'image required'}), 400

        cvimg = decode_data_url_to_cvimg(image_b64)
        res_image, pts = build_white_hand_image_and_pts(cvimg)
        if res_image is None or pts is None:
            return jsonify({'label': None, 'confidence': 0.0, 'error': 'no_hand_detected', 'hand_detected': False})

        label, confidence = predict_from_white_image(res_image, pts)
        
        # Convert skeleton image to base64 for frontend
        _, buffer = cv2.imencode('.png', res_image)
        skeleton_b64 = "data:image/png;base64," + base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'label': label, 
            'confidence': float(confidence),
            'skeleton_image': skeleton_b64,
            'hand_detected': True
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'internal_error', 'detail': str(e)}), 500

@app.route('/suggest', methods=['POST'])
def suggest():
    try:
        payload = request.get_json(force=True)
        word = payload.get('word', '').strip()
        
        if not word or not ddd:
            return jsonify({'suggestions': []})
            
        suggestions = ddd.suggest(word)
        # Limit to top 4 suggestions
        return jsonify({'suggestions': suggestions[:4]})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'internal_error', 'detail': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', os.environ.get('PREDICT_PORT', 5001)))
    host = os.environ.get('PREDICT_HOST', '0.0.0.0')
    # Attempt to preload model for faster first response
    try:
        ensure_model_loaded()
        print('Model loaded successfully')
    except Exception as e:
        print('Model load deferred or failed at startup:', e)
    app.run(host=host, port=port)
