import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API"))

def call_gemini(text, filename):
    try:
        prompt = f"""
        You are a document processing assistant.
        Analyze the following document and return a JSON object with this exact structure:
        {{
            "doc_type": "invoice | contract | report | receipt | other",
            "extracted_fields": {{
                "vendor_name": null,
                "invoice_date": null,
                "total_amount": null,
                "due_date": null,
                "line_items": []
            }},
            "summary": "2-4 sentence summary of the document",
            "confidence": "high | medium | low"
        }}

        Rules:
        - Return ONLY valid JSON, no markdown, no backticks
        - Use null for missing fields, never "N/A" or empty strings
        - Amounts must be numbers, not strings
        - Dates must be ISO format (YYYY-MM-DD)
        - Detect the document type and extract relevant fields accordingly

        Document ({filename}):
        {text}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw = response.text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())

    except json.JSONDecodeError as e:
        print(f"Gemini returned invalid JSON for {filename}: {e}")
        return None
    except Exception as e:
        print(f"Gemini API call failed for {filename}: {e}")
        return None
    
def process_document(file):
    filename = file["file"]
    text = file["text"]

    if not text:
        print(f"Skipping {filename} — empty document")
        return {
            "file": filename,
            "status": "skipped",
            "reason": "empty document",  
            "doc_type": None,
            "extracted_fields": {},
            "summary": None,
            "confidence": None,
            "errors": []
        }

    print(f"Processing {filename} with Gemini")
    result = call_gemini(text, filename)

    if result is None:
        return {
            "file": filename,
            "status": "failed",
            "reason": "LLM call failed or returned invalid JSON",
            "doc_type": None,
            "extracted_fields": {},
            "summary": None,
            "confidence": "low",
            "errors": ["LLM processing failed"]
        }

    return {
        "file": filename,
        "status": "success",
        "doc_type": result.get("doc_type"),
        "extracted_fields": result.get("extracted_fields", {}),
        "summary": result.get("summary"),
        "confidence": result.get("confidence", "low"),
        "errors": []
    }