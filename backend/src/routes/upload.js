const express = require('express');
const multer = require('multer');
const path = require('path');
const router = express.Router();

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, './docs');
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  }
});

const fileFilter = (req, file, cb) => {
  const allowedTypes = ['.pdf', '.txt'];
  const ext = path.extname(file.originalname).toLowerCase();

  if (allowedTypes.includes(ext)) {
    cb(null, true);
  } else {
    console.log(`Skipped unsupported file: ${file.originalname}`);
    cb(null, false);
  }
};

const upload = multer({ storage, fileFilter });

router.post('/', upload.array('documents'), (req, res) => {

  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: 'No valid files uploaded' });
  }

  console.log(`Uploaded ${req.files.length} files`);

  res.status(200).json({
    message: 'Files uploaded successfully',
    files: req.files.map(f => f.originalname)
  });
});


module.exports = router;