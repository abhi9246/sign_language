const express = require('express');
const History = require('../models/History');
const auth = require('../middleware/auth');
const router = express.Router();

// @route GET /api/history
// @desc Get user translation history
router.get('/', auth, async (req, res) => {
  try {
    const history = await History.find({ userId: req.user.id }).sort({ createdAt: -1 });
    res.json(history);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route POST /api/history
// @desc Save a new translation sentence
router.post('/', auth, async (req, res) => {
  try {
    const { sentence } = req.body;
    if (!sentence || sentence.trim().length === 0) {
      return res.status(400).json({ message: 'Sentence is required' });
    }

    const newHistory = new History({
      userId: req.user.id,
      sentence
    });

    const history = await newHistory.save();
    res.json(history);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

// @route DELETE /api/history/:id
// @desc Delete a translation record
router.delete('/:id', auth, async (req, res) => {
  try {
    const history = await History.findById(req.params.id);
    if (!history) {
      return res.status(404).json({ message: 'Record not found' });
    }

    if (history.userId.toString() !== req.user.id) {
      return res.status(401).json({ message: 'Not authorized' });
    }

    await history.deleteOne();
    res.json({ message: 'Record removed' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;
