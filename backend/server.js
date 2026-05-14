require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const authRoutes = require('./routes/auth');
const historyRoutes = require('./routes/history');
const aiRoutes = require('./routes/ai');

const app = express();

// Middleware
const corsOptions = {
  origin: process.env.FRONTEND_URL ? process.env.FRONTEND_URL.split(',') : '*',
  credentials: true,
};
app.use(cors(corsOptions));
app.use(express.json({ limit: '50mb' })); // Increased limit for webcam frames

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/history', historyRoutes);
app.use('/api/ai', aiRoutes);

// MongoDB Connection
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('Connected to MongoDB'))
  .catch(err => console.error('MongoDB connection error:', err));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Node.js backend running on port ${PORT}`);
});
