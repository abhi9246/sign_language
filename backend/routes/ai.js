const express = require('express');
const axios = require('axios');
const router = express.Router();

// Forward image payload to Python Flask AI backend
router.post('/predict', async (req, res) => {
  try {
    const { image } = req.body;
    if (!image) {
      return res.status(400).json({ error: 'Image is required' });
    }

    const aiServiceUrl = process.env.AI_SERVICE_URL || 'http://127.0.0.1:5001';
    
    const response = await axios.post(`${aiServiceUrl}/predict`, {
      image: image
    });

    res.json(response.data);
  } catch (err) {
    if (err.code === 'ECONNREFUSED') {
      res.status(503).json({ error: 'AI Prediction Service is offline. Please start predict_service.py' });
    } else {
      console.error('AI Proxy Error:', err.message);
      if (err.response && err.response.data) {
        require('fs').writeFileSync('error.txt', JSON.stringify(err.response.data));
      }
      res.status(500).json({ error: 'Failed to communicate with AI Service' });
    }
  }
});

// Forward suggestion request to Python Flask AI backend
router.post('/suggest', async (req, res) => {
  try {
    const { word } = req.body;
    if (!word) {
      return res.status(400).json({ error: 'Word is required' });
    }

    const aiServiceUrl = process.env.AI_SERVICE_URL || 'http://127.0.0.1:5001';
    
    const response = await axios.post(`${aiServiceUrl}/suggest`, {
      word: word
    });

    res.json(response.data);
  } catch (err) {
    if (err.code === 'ECONNREFUSED') {
      res.status(503).json({ error: 'AI Prediction Service is offline. Please start predict_service.py' });
    } else {
      console.error('AI Suggest Proxy Error:', err.message);
      res.status(500).json({ error: 'Failed to communicate with AI Service for suggestions' });
    }
  }
});

module.exports = router;
