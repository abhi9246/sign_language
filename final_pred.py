# Importing Libraries
import numpy as np
import math
import cv2
import os
import traceback
import pyttsx3
from keras.models import load_model

import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands1 = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)
hands2 = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

import tkinter as tk
from PIL import Image, ImageTk
import time
import enchant

# Set language for enchant dictionary
ddd = enchant.Dict("en_US")

offset = 29

# Application Class
class Application:
    def __init__(self):
        self.vs = cv2.VideoCapture(0)
        self.vs.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Prevent OpenCV frame buffering delay
        self.current_image = None
        self.model = load_model('./cnn8grps_rad1_model.h5')
        self.input_h, self.input_w = self.model.input_shape[1], self.model.input_shape[2]
        print(f"Loaded model from disk. input_shape = {self.model.input_shape}")
        
        self.speak_engine = pyttsx3.init()
        self.speak_engine.setProperty("rate", 100)
        voices = self.speak_engine.getProperty("voices")
        self.speak_engine.setProperty("voice", voices[0].id)

        # Initialize counters and flags
        self.prev_char = ""
        self.count = -1
        self.ten_prev_char = [" " for _ in range(10)]
        self.frame_counter = 0

        # Stability variables
        self.last_pred = None
        self.pred_count = 0
        self.appended = False
        self.confidence_threshold = 0.25
        self.stability_threshold = 3

        # Hand visibility for space
        self.hand_visible = False
        self.space_added = True  # Start as true to avoid initial space

        # Set up Tkinter GUI
        self.root = tk.Tk()
        self.root.title("Sign Language To Text Conversion")
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        self.root.geometry("1300x700")

        self.panel = tk.Label(self.root)  # Webcam feed
        self.panel.place(x=40, y=3, width=480, height=640)

        self.panel2 = tk.Label(self.root)  # Hand skeleton
        self.panel2.place(x=550, y=115, width=400, height=400)

        self.T = tk.Label(self.root, text="Sign Language To Text Conversion", font=("Times New Roman", 30, "bold"))
        self.T.place(x=60, y=5)

        # Sign language reference image
        image1 = Image.open("signs.png")
        image1 = image1.resize((500, 400), Image.LANCZOS)
        test = ImageTk.PhotoImage(image1)
        label1 = tk.Label(image=test)
        label1.image = test
        label1.place(x=1000, y=110)

        self.panel3 = tk.Label(self.root)  # Current Symbol
        self.panel3.place(x=280, y=585)

        self.T1 = tk.Label(self.root, text="Character :", font=("Times New Roman", 30, "bold"))
        self.T1.place(x=10, y=580)

        self.panel5 = tk.Label(self.root)  # Sentence
        self.panel5.place(x=260, y=632)

        self.T3 = tk.Label(self.root, text="Sentence :", font=("Times New Roman", 30, "bold"))
        self.T3.place(x=10, y=632)

        self.T4 = tk.Label(self.root, text="Suggestions :", fg="red", font=("Times New Roman", 30, "bold"))
        self.T4.place(x=10, y=700)

        # Suggestion buttons
        self.b1 = tk.Button(self.root, font=("Times New Roman", 20), wraplength=825, command=self.action1)
        self.b1.place(x=390, y=700)

        self.b2 = tk.Button(self.root, font=("Times New Roman", 20), wraplength=825, command=self.action2)
        self.b2.place(x=590, y=700)

        self.b3 = tk.Button(self.root, font=("Times New Roman", 20), wraplength=825, command=self.action3)
        self.b3.place(x=790, y=700)

        self.b4 = tk.Button(self.root, font=("Times New Roman", 20), wraplength=825, command=self.action4)
        self.b4.place(x=990, y=700)

        self.speak = tk.Button(self.root, text="Speak", font=("Times New Roman", 20), wraplength=100, command=self.speak_fun)
        self.speak.place(x=1305, y=630)

        self.clear = tk.Button(self.root, text="Clear", font=("Times New Roman", 20), wraplength=100, command=self.clear_fun)
        self.clear.place(x=1205, y=630)

        self.sentence = ""
        self.word = ""
        self.current_symbol = ""
        self.word1 = self.word2 = self.word3 = self.word4 = ""

        self.last_frame_time = time.time()
        self.video_loop()

    def video_loop(self):
        try:
            self.frame_counter += 1
            ok, frame = self.vs.read()
            if not ok:
                self.root.after(15, self.video_loop)
                return

            cv2image = cv2.flip(frame, 1)
            
            # Process with MediaPipe
            rgb_image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGB)
            results1 = hands1.process(rgb_image)

            self.current_image = Image.fromarray(rgb_image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            hand_detected = bool(results1.multi_hand_landmarks)

            if hand_detected:
                self.hand_visible = True
                self.space_added = False
                hand_landmarks1 = results1.multi_hand_landmarks[0]
                
                img_h, img_w, _ = rgb_image.shape
                
                # Extract initial bounding box from full frame
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
                
                if x2 > x1 and y2 > y1:
                    image_crop = cv2image[y1:y2, x1:x2]
                    rgb_crop = cv2.cvtColor(image_crop, cv2.COLOR_BGR2RGB)
                    
                    # PASS 2: Process the tight crop with the second isolated tracker
                    results2 = hands2.process(rgb_crop)
                    
                    if results2.multi_hand_landmarks:
                        hand_landmarks2 = results2.multi_hand_landmarks[0]
                        crop_h, crop_w, _ = rgb_crop.shape
                        
                        self.pts = []
                        for lm in hand_landmarks2.landmark:
                            self.pts.append((int(lm.x * crop_w), int(lm.y * crop_h)))
                            
                        # Exact offset math from the original code
                        os_ = ((400 - w) // 2) - 15
                        os1 = ((400 - h) // 2) - 15
                        
                        white = np.ones((400, 400, 3), np.uint8) * 255
                        
                        # Draw finger connections (thumb to pinky)
                        for start, end in [(1,2),(2,3),(3,4),(5,6),(6,7),(7,8),(9,10),(10,11),(11,12),(13,14),(14,15),(15,16),(17,18),(18,19),(19,20)]:
                            cv2.line(white, (self.pts[start][0] + os_, self.pts[start][1] + os1),
                                     (self.pts[end][0] + os_, self.pts[end][1] + os1), (0, 255, 0), 3)

                        # Draw palm connections
                        for conn in [(0,1),(0,5),(5,9),(9,13),(13,17),(17,0),(0,17)]:
                            cv2.line(white, (self.pts[conn[0]][0] + os_, self.pts[conn[0]][1] + os1),
                                     (self.pts[conn[1]][0] + os_, self.pts[conn[1]][1] + os1), (0, 255, 0), 3)

                        # Draw landmarks
                        for i in range(21):
                            cv2.circle(white, (self.pts[i][0] + os_, self.pts[i][1] + os1), 3, (0, 0, 255), -1)

                        res = white
                        
                        # Predict only every 5 frames to prevent GUI freezing
                        if self.frame_counter % 5 == 0:
                            predicted = self.predict(res)
                            if predicted:
                                self.current_symbol = predicted
                        
                        self.panel3.config(text=self.current_symbol, font=("Times New Roman", 30))

                        self.current_image2 = Image.fromarray(res)
                        imgtk = ImageTk.PhotoImage(image=self.current_image2)
                        self.panel2.imgtk = imgtk
                        self.panel2.config(image=imgtk)
                    else:
                        self.hand_visible = False
                else:
                    self.hand_visible = False

            if not hand_detected:
                if self.hand_visible and not self.space_added and self.sentence and self.sentence[-1] != " ":
                    self.sentence += " "
                    self.space_added = True
                self.hand_visible = False
                self.clear_panel2()

            self.update_suggestions()
            self.b1.config(text=self.word1)
            self.b2.config(text=self.word2)
            self.b3.config(text=self.word3)
            self.b4.config(text=self.word4)

            self.panel5.config(text=self.sentence, font=("Times New Roman", 30), wraplength=1025)
        except Exception:
            print("Error:", traceback.format_exc())
        finally:
            self.root.after(15, self.video_loop)

    def clear_panel2(self):
        blank = Image.new('RGB', (400, 400), (255, 255, 255))
        imgtk_blank = ImageTk.PhotoImage(image=blank)
        self.panel2.imgtk = imgtk_blank
        self.panel2.config(image=imgtk_blank)
        self.current_symbol = ""
        self.panel3.config(text=self.current_symbol, font=("Times New Roman", 30))

    def distance(self, x, y):
        return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))

    def action1(self):
        self.replace_word(self.word1)

    def action2(self):
        self.replace_word(self.word2)

    def action3(self):
        self.replace_word(self.word3)

    def action4(self):
        self.replace_word(self.word4)

    def replace_word(self, new_word):
        if self.word and new_word:
            idx = self.sentence.rfind(self.word)
            if idx != -1:
                self.sentence = self.sentence[:idx] + new_word.upper() + self.sentence[idx + len(self.word):]

    def speak_fun(self):
        self.speak_engine.say(self.sentence)
        self.speak_engine.runAndWait()

    def clear_fun(self):
        self.sentence = ""
        self.word1 = self.word2 = self.word3 = self.word4 = ""
        self.space_added = True

    def predict(self, test_image):
        img = test_image.copy()
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        img = cv2.resize(img, (self.input_w, self.input_h))
        inp = img.astype('float32') / 255.0
        inp = np.expand_dims(inp, axis=0)

        preds = self.model.predict(inp, verbose=0)[0]
        max_prob = np.max(preds)
        
        top3_idx = np.argsort(preds)[-3:][::-1]
        top3_str = ", ".join([f"Class {i}: {preds[i]:.2f}" for i in top3_idx])
        print(f"Top-3 Probs: [{top3_str}]")
        
        if max_prob < self.confidence_threshold:
            print(f"Weak confidence: {max_prob:.2f} (Threshold: {self.confidence_threshold})")
            return None

        ch1_idx = int(np.argmax(preds))
        ch1 = ch1_idx

        # Refinement logic
        prob = preds.copy()
        prob[ch1] = 0
        ch2 = int(np.argmax(prob))
        prob[ch2] = 0
        ch3 = int(np.argmax(prob))

        pl = [ch1, ch2]

        # Condition for [Aemnst]
        l = [[5, 2], [5, 3], [3, 5], [3, 6], [3, 0], [3, 2], [6, 4], [6, 1], [6, 2], [6, 6], [6, 7], [6, 0], [6, 5],
             [4, 1], [1, 0], [1, 1], [6, 3], [1, 6], [5, 6], [5, 1], [4, 5], [1, 4], [1, 5], [2, 0], [2, 6], [4, 6],
             [1, 0], [5, 7], [1, 6], [6, 1], [7, 6], [2, 5], [7, 1], [5, 4], [7, 0], [7, 5], [7, 2]]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                ch1 = 0

        # Condition for [o][s]
        l = [[2, 2], [2, 1]]
        if pl in l:
            if (self.pts[5][0] < self.pts[4][0]):
                ch1 = 0

        # Condition for [c0][aemnst]
        l = [[0, 0], [0, 6], [0, 2], [0, 5], [0, 1], [0, 7], [5, 2], [7, 6], [7, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[4][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and self.pts[5][0] > self.pts[4][0]:
                ch1 = 2

        # Condition for [c0][aemnst]
        l = [[6, 0], [6, 6], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) < 52:
                ch1 = 2

        # Condition for [gh][bdfikruvw]
        l = [[1, 4], [1, 5], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1] and self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 3

        # Condition for [gh][l]
        l = [[4, 6], [4, 1], [4, 5], [4, 3], [4, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 3

        # Condition for [gh][pqz]
        l = [[5, 3], [5, 0], [5, 7], [5, 4], [5, 2], [5, 1], [5, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[2][1] + 15 < self.pts[16][1]:
                ch1 = 3

        # Condition for [l][x]
        l = [[6, 4], [6, 1], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) > 55:
                ch1 = 4

        # Condition for [l][d]
        l = [[1, 4], [1, 6], [1, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) > 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 4

        # Condition for [l][gh]
        l = [[3, 6], [3, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[4][0] < self.pts[0][0]):
                ch1 = 4

        # Condition for [l][c0]
        l = [[2, 2], [2, 5], [2, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[1][0] < self.pts[12][0]):
                ch1 = 4

        # Condition for [gh][z]
        l = [[3, 6], [3, 5], [3, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and self.pts[4][1] > self.pts[10][1]:
                ch1 = 5

        # Condition for [gh][pq]
        l = [[3, 2], [3, 1], [3, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][1] + 17 > self.pts[8][1] and self.pts[4][1] + 17 > self.pts[12][1] and self.pts[4][1] + 17 > self.pts[16][1] and self.pts[4][1] + 17 > self.pts[20][1]:
                ch1 = 5

        # Condition for [l][pqz]
        l = [[4, 4], [4, 5], [4, 2], [7, 5], [7, 6], [7, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[4][0] > self.pts[0][0]:
                ch1 = 5

        # Condition for [pqz][aemnst]
        l = [[0, 2], [0, 6], [0, 1], [0, 5], [0, 0], [0, 7], [0, 4], [0, 3], [2, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[0][0] < self.pts[8][0] and self.pts[0][0] < self.pts[12][0] and self.pts[0][0] < self.pts[16][0] and self.pts[0][0] < self.pts[20][0]:
                ch1 = 5

        # Condition for [pqz][yj]
        l = [[5, 7], [5, 2], [5, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[3][0] < self.pts[0][0]:
                ch1 = 7

        # Condition for [l][yj]
        l = [[4, 6], [4, 2], [4, 4], [4, 1], [4, 5], [4, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] < self.pts[8][1]:
                ch1 = 7

        # Condition for [x][yj]
        l = [[6, 7], [0, 7], [0, 1], [0, 0], [6, 4], [6, 6], [6, 5], [6, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[18][1] > self.pts[20][1]:
                ch1 = 7

        # Condition for [x][aemnst]
        l = [[0, 4], [0, 2], [0, 3], [0, 1], [0, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] > self.pts[16][0]:
                ch1 = 6

        # Condition for [yj][x]
        l = [[7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[18][1] < self.pts[20][1] and self.pts[8][1] < self.pts[10][1]:
                ch1 = 6

        # Condition for [c0][x]
        l = [[2, 1], [2, 2], [2, 6], [2, 7], [2, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[8], self.pts[16]) > 50:
                ch1 = 6

        # Condition for [l][x]
        l = [[4, 6], [4, 2], [4, 1], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if self.distance(self.pts[4], self.pts[11]) < 60:
                ch1 = 6

        # Condition for [x][d]
        l = [[1, 4], [1, 6], [1, 0], [1, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 > 0:
                ch1 = 6

        # Condition for [b][pqz]
        l = [[5, 0], [5, 1], [5, 4], [5, 5], [5, 6], [6, 1], [7, 6], [0, 2], [7, 1], [7, 4], [6, 6], [7, 2], [5, 0],
             [6, 3], [6, 4], [7, 5], [7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        # Condition for [f][pqz]
        l = [[6, 1], [6, 0], [0, 3], [6, 4], [2, 2], [0, 6], [6, 2], [7, 6], [4, 6], [4, 1], [4, 2], [0, 2], [7, 1],
             [7, 4], [6, 6], [7, 2], [7, 5], [7, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        l = [[6, 1], [6, 0], [4, 2], [4, 1], [4, 6], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 1

        # Condition for [d][pqz]
        l = [[5, 0], [3, 4], [3, 0], [3, 1], [3, 5], [5, 5], [5, 4], [5, 1], [7, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[4][1] > self.pts[14][1]):
                ch1 = 1

        l = [[4, 1], [4, 2], [4, 4]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.distance(self.pts[4], self.pts[11]) < 50) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 1

        l = [[3, 4], [3, 0], [3, 1], [3, 5], [3, 6]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1]) and (self.pts[2][0] < self.pts[0][0]) and self.pts[14][1] < self.pts[4][1]):
                ch1 = 1

        l = [[6, 6], [6, 4], [6, 1], [6, 2]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[5][0] - self.pts[4][0] - 15 < 0:
                ch1 = 1

        # Condition for [i][pqz]
        l = [[5, 4], [5, 5], [5, 1], [0, 3], [0, 7], [5, 0], [0, 2], [6, 2], [7, 5], [7, 1], [7, 6], [7, 7]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] > self.pts[20][1])):
                ch1 = 1

        # Condition for [yj][bfdi]
        l = [[1, 5], [1, 7], [1, 1], [1, 6], [1, 3], [1, 0]]
        pl = [ch1, ch2]
        if pl in l:
            if (self.pts[4][0] < self.pts[5][0] + 15) and (
                    self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                    self.pts[18][1] > self.pts[20][1]):
                ch1 = 7

        # Condition for [uvr]
        l = [[5, 5], [5, 0], [5, 4], [5, 1], [4, 6], [4, 1], [7, 6], [3, 0], [3, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if ((self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and
                 self.pts[18][1] < self.pts[20][1])) and self.pts[4][1] < self.pts[9][1]:
                ch1 = 1

        # Condition for [w]
        l = [[3, 5], [3, 0], [3, 6], [5, 1], [4, 1], [2, 0], [5, 0], [5, 5]]
        pl = [ch1, ch2]
        if pl in l:
            if not (self.pts[0][0] + 13 < self.pts[8][0] and self.pts[0][0] + 13 < self.pts[12][0] and self.pts[0][0] + 13 < self.pts[16][0] and
                    self.pts[0][0] + 13 < self.pts[20][0]) and not (
                    self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and self.distance(self.pts[4], self.pts[11]) < 50:
                ch1 = 1

        # Condition for [w]
        l = [[5, 0], [5, 5], [0, 1]]
        pl = [ch1, ch2]
        if pl in l:
            if self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1]:
                ch1 = 1

        # Conditions for subgroups
        if ch1 == 0:
            ch1 = 'S'
            if self.pts[4][0] < self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0]:
                ch1 = 'A'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] < self.pts[10][0] and self.pts[4][0] < self.pts[14][0] and self.pts[4][0] < self.pts[18][0] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'T'
            if self.pts[4][1] > self.pts[8][1] and self.pts[4][1] > self.pts[12][1] and self.pts[4][1] > self.pts[16][1] and self.pts[4][1] > self.pts[20][1]:
                ch1 = 'E'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][0] > self.pts[14][0] and self.pts[4][1] < self.pts[18][1]:
                ch1 = 'M'
            if self.pts[4][0] > self.pts[6][0] and self.pts[4][0] > self.pts[10][0] and self.pts[4][1] < self.pts[18][1] and self.pts[4][1] < self.pts[14][1]:
                ch1 = 'N'

        if ch1 == 2:
            if self.distance(self.pts[12], self.pts[4]) > 42:
                ch1 = 'C'
            else:
                ch1 = 'O'

        if ch1 == 3:
            if (self.distance(self.pts[8], self.pts[12])) > 72:
                ch1 = 'G'
            else:
                ch1 = 'H'

        if ch1 == 7:
            if self.distance(self.pts[8], self.pts[4]) > 42:
                ch1 = 'Y'
            else:
                ch1 = 'J'

        if ch1 == 4:
            ch1 = 'L'

        if ch1 == 6:
            ch1 = 'X'

        if ch1 == 5:
            if self.pts[4][0] > self.pts[12][0] and self.pts[4][0] > self.pts[16][0] and self.pts[4][0] > self.pts[20][0]:
                if self.pts[8][1] < self.pts[5][1]:
                    ch1 = 'Z'
                else:
                    ch1 = 'Q'
            else:
                ch1 = 'P'

        if ch1 == 1:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = 'B'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                ch1 = 'D'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = 'F'
            if (self.pts[6][1] < self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = 'I'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] < self.pts[20][1]):
                ch1 = 'W'
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] < self.pts[20][1]) and self.pts[4][1] < self.pts[9][1]:
                ch1 = 'K'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) < 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 'U'
            if ((self.distance(self.pts[8], self.pts[12]) - self.distance(self.pts[6], self.pts[10])) >= 8) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]) and (self.pts[4][1] > self.pts[9][1]):
                ch1 = 'V'
            if (self.pts[8][0] > self.pts[12][0]) and (
                    self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] <
                    self.pts[20][1]):
                ch1 = 'R'

        if ch1 in [1, 'E', 'S', 'X', 'Y', 'B']:
            if (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] < self.pts[12][1] and self.pts[14][1] < self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = " "

        if ch1 in ['E', 'Y', 'B']:
            if (self.pts[4][0] < self.pts[5][0]) and (self.pts[6][1] > self.pts[8][1] and self.pts[10][1] > self.pts[12][1] and self.pts[14][1] > self.pts[16][1] and self.pts[18][1] > self.pts[20][1]):
                ch1 = "next"

        if ch1 in ['next', 'B', 'C', 'H', 'F', 'X']:
            if (self.pts[0][0] > self.pts[8][0] and self.pts[0][0] > self.pts[12][0] and self.pts[0][0] > self.pts[16][0] and self.pts[0][0] > self.pts[20][0]) and (self.pts[4][1] < self.pts[8][1] and self.pts[4][1] < self.pts[12][1] and self.pts[4][1] < self.pts[16][1] and self.pts[4][1] < self.pts[20][1]) and (self.pts[4][1] < self.pts[6][1] and self.pts[4][1] < self.pts[10][1] and self.pts[4][1] < self.pts[14][1] and self.pts[4][1] < self.pts[18][1]):
                ch1 = 'Backspace'

        if ch1 == "next" and self.prev_char != "next":
            if self.ten_prev_char[(self.count - 2) % 10] != "next":
                if self.ten_prev_char[(self.count - 2) % 10] == "Backspace":
                    self.sentence = self.sentence[:-1]
                else:
                    if self.ten_prev_char[(self.count - 2) % 10] != "Backspace":
                        self.sentence = self.sentence + self.ten_prev_char[(self.count - 2) % 10]
            else:
                if self.ten_prev_char[(self.count - 0) % 10] != "Backspace":
                    self.sentence = self.sentence + self.ten_prev_char[(self.count - 0) % 10]

        if ch1 == " " and self.prev_char != " ":
            self.sentence = self.sentence + " "

        if ch1 == 'Backspace' and self.prev_char != 'Backspace':
            if self.sentence:
                self.sentence = self.sentence[:-1]

        # Stability check for letters only
        if isinstance(ch1, str) and len(ch1) == 1 and ch1.isalpha() and ch1.isupper():
            if ch1 == self.last_pred:
                self.pred_count += 1
            else:
                self.last_pred = ch1
                self.pred_count = 1
                self.appended = False

            if self.pred_count >= self.stability_threshold and not self.appended:
                self.sentence += ch1
                self.appended = True
                self.prev_char = ch1
                self.count += 1
                self.ten_prev_char[self.count % 10] = ch1
                print(f"Appended to sentence: {ch1} (Confidence: {max_prob:.2f})")
                return ch1
            else:
                print(f"Detected: {ch1} (Confidence: {max_prob:.2f}) | Stabilizing: {self.pred_count}/{self.stability_threshold}")
                return ch1
        else:
            self.pred_count = 0
            self.appended = False

        print(f"Detected token: {ch1} (Confidence: {max_prob:.2f})")
        return None

    def update_suggestions(self):
        if not self.sentence.strip():
            self.word1 = self.word2 = self.word3 = self.word4 = ""
            return

        st = self.sentence.rfind(" ")
        word = self.sentence[st + 1:].strip()
        self.word = word
        if word:
            suggestions = ddd.suggest(word)
            lenn = len(suggestions)
            self.word1 = suggestions[0] if lenn >= 1 else ""
            self.word2 = suggestions[1] if lenn >= 2 else ""
            self.word3 = suggestions[2] if lenn >= 3 else ""
            self.word4 = suggestions[3] if lenn >= 4 else ""
        else:
            self.word1 = self.word2 = self.word3 = self.word4 = ""

    def destructor(self):
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

print("Starting Application...")
app = Application()
app.root.mainloop()
