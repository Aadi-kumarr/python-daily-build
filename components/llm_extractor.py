import os
import json
import re
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(" GEMINI_API_KEY not found. Check your .env file")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY)

# Pydantic Schema

class InvoiceData(BaseModel):
    vendor: str | None
    invoice_no: str | None
    amount: float | None
    currency: str | None
    due_date: str | None
    line_items: list[str]

# Load Prompt

with open("prompts/invoice_extract.txt", "r") as f:
    base_prompt = f.read()

# Sample invoice text (replace for testing)

invoice_text = """
Invoice issued by : BigTree Entertainment Pvt Ltd
Invoice Number : TIN262701834202
Date of issue : Sun, 5 Apr, 2026
Total Amount after Tax : 63.72
Product: Project Hail Mary
"""

# Gemini API call

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=base_prompt + "\n" + invoice_text
    )

    raw_output = response.text
    print("\n Raw LLM Output:\n", raw_output)

except Exception as e:
    print("\n Gemini API Error:", e)
    raw_output = "{}"

# Clean JSON (remove markdown if present)

raw_output = raw_output.replace("```json", "").replace("```", "").strip()

# Convert to JSON

try:
    parsed_json = json.loads(raw_output)
except Exception as e:
    print("\n Invalid JSON from LLM:", e)
    parsed_json = {}

# Validate with Pydantic

try:
    invoice = InvoiceData(**parsed_json)

except ValidationError as e:
    print("\n Validation Error:\n", e)
    invoice = InvoiceData(
        vendor=None,
        invoice_no=None,
        amount=None,
        currency=None,
        due_date=None,
        line_items=[]
    )

# Post-processing (fallback fixes)

# Currency fallback
if not invoice.currency:
    text_lower = invoice_text.lower()

    if "₹" in invoice_text or "inr" in text_lower or "rupee" in text_lower:
        invoice.currency = "INR"
    elif "$" in invoice_text or "usd" in text_lower:
        invoice.currency = "USD"
    elif "€" in invoice_text or "eur" in text_lower:
        invoice.currency = "EUR"
    else:
        invoice.currency = "INR"  # default

# Date fallback
if not invoice.due_date:
    match = re.search(r"(Sun,\s*\d{1,2}\s*[A-Za-z]+,\s*\d{4})", invoice_text)
    if match:
        invoice.due_date = match.group(1)

# Final Output

print("\nFinal Validated Output:\n")
print(invoice.model_dump())