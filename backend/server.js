const express = require('express');
const cors = require('cors');
const uploadRoute = require('./src/routes/upload.js');

const app = express();

app.use(cors());

app.use(express.json());
app.use('/upload', uploadRoute);

const PORT = process.env.PORT || 8000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));