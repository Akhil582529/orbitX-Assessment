const express = require('express');
const multer = require('multer');
const path = require('path');
const { spawn } = require('child_process');
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
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:5173');

  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ message: 'No valid files uploaded' });
  }

  console.log(`Uploaded ${req.files.length} files`);

  setImmediate(() => {
    const python = spawn('python3', ['src/pipeline/main.py']);

    python.stdout.on('data', (data) => {
      console.log(`Pipeline: ${data}`);
    });

    python.stderr.on('data', (data) => {
      console.error(`Pipeline error: ${data}`);
    });

    python.on('close', (code) => {
      console.log(`Pipeline exited with code ${code}`);
    });
  });

  const python = spawn('python3', ['src/pipeline/main.py']);

  python.stdout.on('data', (data) => {
    console.log(`Pipeline: ${data}`);
  });

  python.stderr.on('data', (data) => {
    console.error(`Pipeline error: ${data}`);
  });

  python.on('close', (code) => {
    console.log(`Pipeline exited with code ${code}`);
  });

  res.status(200).json({
    message: 'Files uploaded successfully, pipeline started',
    files: req.files.map(f => f.originalname)
  });
});


module.exports = router;