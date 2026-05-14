# AI Sign Language Translator (MERN + Python)

This project is a full-stack Web Application that performs real-time Sign Language Translation using a Custom CNN, MediaPipe, and the MERN stack.

## Architecture

1. **Python AI Service (Port 5001)**: A Flask server (`predict_service.py`) that processes webcam frames via MediaPipe and Keras.
2. **Node.js Backend (Port 5000)**: An Express API (`backend/server.js`) that manages MongoDB users, JWT authentication, translation history, and securely proxies webcam streams to the AI service.
3. **React Frontend (Port 5173)**: A modern, Vite+Tailwind web app (`frontend/`) capturing webcam frames and displaying live translations.

## Prerequisites

- **Python 3.11** (Your `venv311` environment is already configured)
- **Node.js** (Required to run the React and Express servers)
- **MongoDB** (Requires a local MongoDB database running on port `27017`. If using MongoDB Atlas, edit `backend/.env` and replace the `MONGODB_URI` string).

## First-Time Setup

Before running the app for the first time, you must install the Node.js packages for the backend and frontend.

Open a terminal in the root folder and run:
```powershell
cd backend
npm install
cd ../frontend
npm install
```

## How to Run the App

### Method 1: The Easy Way (Windows)
Simply double-click the **`start_app.bat`** file in the root directory!
It will automatically open three separate terminal windows and start all three services simultaneously. 

### Method 2: Manual Startup
You must run these three commands in **three separate terminal windows**.

**Terminal 1: Python AI Service**
```powershell
.\venv311\Scripts\activate
python predict_service.py
```

**Terminal 2: Node.js Backend**
```powershell
cd backend
npm run dev
```

**Terminal 3: React Frontend**
```powershell
cd frontend
npm run dev
```

Once all services are running, open your web browser and navigate to:
**http://localhost:5173**
