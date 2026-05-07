from datetime import datetime
from pydantic import BaseModel, ValidationError


# Pydantic Schema

class InvoiceData(BaseModel):
    vendor: str
    amount: float
    currency: str
    due_date: str


# Business Rules

approved_vendors = [
    "BigTree Entertainment Pvt Ltd",
    "InterGlobe Aviation Limited",
    "Roppen Transportation Services Private Limited"
]

credit_limit = 10000

allowed_currencies = ["INR", "USD"]


# Validator Function

def validate_invoice(invoice_dict):

    errors = []

    # Validate structure/types

    try:
        invoice = InvoiceData(**invoice_dict)

    except ValidationError as e:

        return {
            "valid": False,
            "errors": [str(e)]
        }

    # Vendor validation

    if invoice.vendor not in approved_vendors:
        errors.append("Vendor not approved")

    # Amount validation

    if invoice.amount > credit_limit:
        errors.append("Amount exceeds credit limit")

    # Currency validation

    if invoice.currency not in allowed_currencies:
        errors.append("Invalid currency")

    # Due date validation

    try:

        due_date = datetime.strptime(
            invoice.due_date,
            "%Y-%m-%d"
        )

        today = datetime.today()

        if due_date.date() <= today.date():
            errors.append("Due date is not in future")

    except:
        errors.append("Invalid due date format")

    # Final Result

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }