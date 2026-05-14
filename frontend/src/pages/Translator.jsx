import { useState, useContext, useRef, useEffect, useCallback } from 'react';
import Webcam from 'react-webcam';
import { motion } from 'framer-motion';
import { Volume2, RefreshCw, Save, Loader2 } from 'lucide-react';
import { aiAPI, historyAPI } from '../api';
import { AuthContext } from '../context/AuthContext';

const Translator = () => {
  const { user } = useContext(AuthContext);
  const webcamRef = useRef(null);
  
  const [prediction, setPrediction] = useState('-');
  const [confidence, setConfidence] = useState(0);
  const [sentence, setSentence] = useState('');
  const [isActive, setIsActive] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);
  
  const [skeletonImage, setSkeletonImage] = useState(null);
  const [stabilizingLabel, setStabilizingLabel] = useState(null);
  const [stableCount, setStableCount] = useState(0);
  const [spaceAdded, setSpaceAdded] = useState(true);
  const [suggestions, setSuggestions] = useState([]);
  
  const STABILITY_THRESHOLD = 3;
  const noHandFrames = useRef(0);
  
  // Refs for tracking mutable state inside useCallback interval without stale closures
  const stabilizingLabelRef = useRef(null);
  const stableCountRef = useRef(0);

  const captureAndPredict = useCallback(async () => {
    if (!isActive || !webcamRef.current) return;
    
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    setIsProcessing(true);
    try {
      setError(null);
      const res = await aiAPI.predict(imageSrc);
      const { label, confidence, error, skeleton_image, hand_detected } = res.data;
      
      if (error || !hand_detected) {
        setPrediction('-');
        setConfidence(0);
        setError(null);
        setSkeletonImage(null);
        
        noHandFrames.current += 1;
        // Auto space if hand is gone for ~5 frames
        if (noHandFrames.current > 5 && !spaceAdded) {
           setSentence(prev => {
               if (prev && !prev.endsWith(' ')) return prev + ' ';
               return prev;
           });
           setSpaceAdded(true);
        }
      } else if (label) {
        noHandFrames.current = 0;
        setPrediction(label);
        setConfidence(confidence);
        setSkeletonImage(skeleton_image);
        setSpaceAdded(false);
        
        // Stabilize prediction using Refs to avoid stale closures
        if (label === stabilizingLabelRef.current) {
            if (stableCountRef.current + 1 === STABILITY_THRESHOLD) {
                // Confirm action
                if (label === 'next') {
                    // Do nothing
                } else if (label === 'Backspace') {
                    setSentence(prev => prev.slice(0, -1));
                } else if (label.length === 1 && label !== ' ') {
                    setSentence(prev => {
                        if (!prev.endsWith(label)) return prev + label;
                        return prev;
                    });
                } else if (label === ' ') {
                    setSentence(prev => {
                        if (!prev.endsWith(' ')) return prev + ' ';
                        return prev;
                    });
                    setSpaceAdded(true);
                }
                stableCountRef.current += 1; // increment past threshold to avoid repeated triggers
            } else if (stableCountRef.current < STABILITY_THRESHOLD) {
                stableCountRef.current += 1;
            }
        } else {
            stabilizingLabelRef.current = label;
            stableCountRef.current = 1;
        }
        
        // Sync UI State
        setStabilizingLabel(stabilizingLabelRef.current);
        setStableCount(stableCountRef.current);
      }
    } catch (err) {
      console.error("Prediction error:", err);
      setError("AI Service Offline. Ensure Python predict_service.py is running on port 5001.");
      setIsActive(false);
    } finally {
      setIsProcessing(false);
    }
  }, [isActive]);

  useEffect(() => {
    let interval;
    if (isActive) {
      interval = setInterval(captureAndPredict, 300); // 300ms = ~3 FPS for API calls
    }
    return () => clearInterval(interval);
  }, [isActive, captureAndPredict]);

  useEffect(() => {
    const fetchSuggestions = async () => {
      const words = sentence.split(' ');
      const lastWord = words[words.length - 1];
      if (lastWord && lastWord.length >= 2) {
        try {
          const res = await aiAPI.suggest(lastWord);
          setSuggestions(res.data.suggestions || []);
        } catch (e) {
          console.error("Suggestion error:", e);
        }
      } else {
        setSuggestions([]);
      }
    };

    const debounceTimer = setTimeout(fetchSuggestions, 500);
    return () => clearTimeout(debounceTimer);
  }, [sentence]);

  const handleBackspace = () => {
    setSentence(prev => prev.slice(0, -1));
  };

  const handleSuggestionClick = (suggestion) => {
    setSentence(prev => {
      const words = prev.split(' ');
      words.pop();
      const prefix = words.length > 0 ? words.join(' ') + ' ' : '';
      return prefix + suggestion.toUpperCase() + ' ';
    });
    setSuggestions([]);
    setSpaceAdded(true);
  };

  const speak = () => {
    if (!sentence) return;
    const utterance = new SpeechSynthesisUtterance(sentence);
    window.speechSynthesis.speak(utterance);
  };

  const saveToHistory = async () => {
    if (!user || !sentence) return;
    try {
      await historyAPI.saveSentence(sentence);
      alert('Saved to history!');
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen pt-24 px-4 pb-12 max-w-7xl mx-auto">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Live Translation</h1>
        <button 
          onClick={() => setIsActive(!isActive)}
          className={`px-6 py-2 rounded-full font-bold transition flex items-center gap-2 ${isActive ? 'bg-red-500/20 text-red-400 border border-red-500/50' : 'bg-primary text-white shadow-[0_0_15px_rgba(59,130,246,0.5)]'}`}
        >
          {isActive ? 'Stop Camera' : 'Start Camera'}
        </button>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-400 p-4 rounded-lg mb-6">
          {error}
        </div>
      )}

      <div className="grid lg:grid-cols-3 gap-8">
        {/* Camera Panel */}
        <div className="glass-panel overflow-hidden relative aspect-video bg-black/50 flex items-center justify-center lg:col-span-1">
          {isActive ? (
            <Webcam
              audio={false}
              ref={webcamRef}
              mirrored={false}
              screenshotFormat="image/png"
              className="w-full h-full object-cover"
              videoConstraints={{ width: 640, height: 480, facingMode: "user" }}
            />
          ) : (
            <div className="text-gray-500 flex flex-col items-center">
              <RefreshCw className="w-12 h-12 mb-4 opacity-20" />
              <p>Camera is disabled</p>
            </div>
          )}
          
          <div className="absolute top-4 left-4 glass-panel px-3 py-1 flex items-center gap-2 text-sm border-none bg-black/40">
            <div className={`w-2 h-2 rounded-full ${isActive ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`} />
            {isActive ? 'Live' : 'Offline'}
          </div>
        </div>

        {/* Skeleton Preview Panel */}
        <div className="glass-panel overflow-hidden relative aspect-video bg-white flex items-center justify-center lg:col-span-1">
          {skeletonImage ? (
            <img src={skeletonImage} alt="Hand Skeleton" className="w-full h-full object-contain" />
          ) : (
            <div className="text-gray-300 flex flex-col items-center">
              <p>No Hand Detected</p>
            </div>
          )}
          
          {isActive && confidence > 0 && (
             <div className="absolute bottom-4 left-4 glass-panel px-3 py-1 text-sm border-none bg-black/60 text-white">
                Conf: {(confidence * 100).toFixed(0)}%
             </div>
          )}
        </div>

        {/* Prediction Panel */}
        <div className="flex flex-col gap-6 lg:col-span-1">
          <motion.div className="glass-panel p-8 flex-1 flex flex-col items-center justify-center relative">
            {isProcessing && isActive && <Loader2 className="absolute top-4 right-4 animate-spin text-primary opacity-50" />}
            <h3 className="text-gray-400 text-sm tracking-widest uppercase mb-2">Detected Symbol</h3>
            <div className="text-8xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-500">
              {prediction}
            </div>
            {isActive && prediction !== '-' && (
               <div className="mt-4 text-xs text-gray-500">
                  Stabilizing: {Math.min(stableCount, STABILITY_THRESHOLD)}/{STABILITY_THRESHOLD}
               </div>
            )}
          </motion.div>

          <div className="glass-panel p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-gray-400 text-sm tracking-widest uppercase">Sentence</h3>
              <div className="flex gap-2">
                <button onClick={handleBackspace} className="p-2 hover:bg-white/5 rounded-md text-gray-400 hover:text-white transition" title="Backspace">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-delete"><path d="M20 5H9l-7 7 7 7h11a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2Z"/><line x1="18" x2="12" y1="9" y2="15"/><line x1="12" x2="18" y1="9" y2="15"/></svg>
                </button>
                <button onClick={() => setSentence('')} className="p-2 hover:bg-white/5 rounded-md text-gray-400 hover:text-white transition" title="Clear">
                  <RefreshCw size={18} />
                </button>
                <button onClick={speak} className="p-2 hover:bg-white/5 rounded-md text-primary transition" title="Speak">
                  <Volume2 size={18} />
                </button>
                {user && (
                  <button onClick={saveToHistory} className="p-2 hover:bg-white/5 rounded-md text-green-400 transition" title="Save to Dashboard">
                    <Save size={18} />
                  </button>
                )}
              </div>
            </div>
            <div className="w-full min-h-[100px] bg-black/30 rounded-lg p-4 font-mono text-lg border border-white/5 break-words">
              {sentence || <span className="text-gray-600">Start signing...</span>}
            </div>
            
            {/* Suggestions Panel */}
            {suggestions.length > 0 && (
              <div className="mt-4">
                <h4 className="text-xs text-gray-500 uppercase tracking-wider mb-2">Suggestions</h4>
                <div className="flex flex-wrap gap-2">
                  {suggestions.map((sugg, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSuggestionClick(sugg)}
                      className="px-4 py-1.5 bg-primary/20 hover:bg-primary/40 text-primary-200 border border-primary/30 rounded-full text-sm font-medium transition"
                    >
                      {sugg.toUpperCase()}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Translator;
