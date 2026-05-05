import pdfplumber
from pdfminer.high_level import extract_text
import re

pdf_path = "day3/sample3.pdf"

data = {
    "vendor": None,
    "invoice_no": None,
    "amount": None,
    "currency": "INR",
    "due_date": None,
    "line_items": []
}

try:
    text = extract_text(pdf_path)
    text = text.replace("\t", " ")

    # VENDOR
    match = re.search(r"BigTree\s+Entertainment\s+Pvt\s+Ltd", text)
    if match:
        data["vendor"] = match.group(0)

    # INVOICE NUMBER
    match = re.search(r"TIN\d+", text)
    if match:
        data["invoice_no"] = match.group(0)

    # DATE (SPECIFIC FORMAT)
    match = re.search(r"(Sun,\s*\d{1,2}\s*[A-Za-z]+,\s*\d{4})", text)
    if match:
        data["due_date"] = match.group(1)

    # AMOUNT 
    amounts = re.findall(r"\d+\.\d{2}", text)
    if amounts:
        data["amount"] = float(amounts[-1])  

    # LINE ITEMS
    items = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            if tables:
                for table in tables:
                    for row in table:
                        if row and row[0] and "Project Hail Mary" in row[0]:
                            items.append(row)

    data["line_items"] = items

except Exception as e:
    print("Error:", e)

print("\nParsed Invoice Data:\n")
print(data)