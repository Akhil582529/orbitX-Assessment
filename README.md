# AI Document Processing Pipeline

An end-to-end pipeline that accepts a folder of documents, extracts structured fields using Gemini LLM, generates a summary per document, and writes results to a structured JSON output.

## Architecture
React (Upload UI) → Express (multer) → docs/ → Python Pipeline → outputs/results.json
|
extractor.py (PyPDF2)
|
llm.py (Gemini API)
|
writer.py (JSON output)

## Tools & Libraries

**Backend (Node.js)**
- Express — HTTP server
- Multer — file upload handling
- CORS — cross-origin requests

**Pipeline (Python)**
- PyPDF2 — PDF text extraction
- google-genai — Gemini LLM API
- python-dotenv — environment variables

## How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Akhil582529/orbitX-Assessment
cd backend
```

### 2. Install Node dependencies
```bash
npm install
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Add your Gemini API key to .env
```

### 5. Start the server
```bash
npm run dev
```

### 6. Upload documents
Open `http://localhost:5173` in your browser, select a folder of documents and click Upload. The pipeline will trigger automatically.

### 7. Check results
Results are written to `outputs/results_<timestamp>.json`

## Sample Output
```json
{
  "processed_at": "20260403_151745",
  "summary": {
    "total": 4,
    "successful": 4,
    "failed": 0,
    "skipped": 0
  },
  "documents": [
    {
      "file": "dummy.pdf",
      "status": "success",
      "doc_type": "invoice",
      "extracted_fields": {
        "vendor_name": "Hilpert PLC",
        "invoice_date": "2024-09-30",
        "total_amount": 32100.45,
        "due_date": "2024-12-29",
        "line_items": []
      },
      "summary": "Invoice from Hilpert PLC dated September 30, 2024 for a total of 32,100.45 EUR.",
      "confidence": "high",
      "errors": []
    }
  ]
}
```

## Tradeoffs

- **PyPDF2 over pdfplumber** — lighter and simpler for basic text extraction. pdfplumber is better for tables but adds complexity.
- **Single pipeline trigger** — pipeline runs sequentially, not concurrently. Async batch processing would be faster for large folders but adds complexity.
- **Gemini field schema** — using a fixed schema for all doc types keeps the output consistent. Type-specific schemas would be more accurate but require more prompt engineering.
- **Free tier quota** — Gemini free tier has a limit of 20 requests/day. Enable billing for production use.

## Supported File Types

- `.pdf` — text-based PDFs
- `.txt` — plain text files
- All other types are skipped with a log message

## Edge Cases Handled

- Missing fields — returned as `null`
- Corrupt or unreadable files — logged, pipeline continues
- Empty documents — marked as skipped with reason
- LLM parsing failures — caught, logged, marked as failed
- Unsupported file types — skipped by multer with log message
