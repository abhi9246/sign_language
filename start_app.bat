@echo off
echo ===================================================
echo Starting MERN Sign Language Translator Services
echo ===================================================

echo [1/3] Starting Python AI Prediction Service...
start cmd /k "title Python AI Service && .\venv311\Scripts\activate && python predict_service.py"

echo [2/3] Starting Node.js Backend Server...
start cmd /k "title Node.js Backend && cd backend && npm run dev"

echo [3/3] Starting React Frontend...
start cmd /k "title React Frontend && cd frontend && npm run dev"

echo.
echo All three services are booting up in separate windows!
echo Please wait about 10 seconds for everything to load.
echo.
echo Once Vite is ready, open your browser to:
echo http://localhost:5173
echo.
pause
