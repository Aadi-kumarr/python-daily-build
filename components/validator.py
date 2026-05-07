from datetime import datetime

# Approved vendors
approved_vendors = [
    "BigTree Entertainment Pvt Ltd",
    "InterGlobe Aviation Limited",
    "Roppen Transportation Services Private Limited"
]

# Credit limit
credit_limit = 10000

# Allowed currencies
allowed_currencies = ["INR", "USD"]


def validate_invoice(invoice_data):

    errors = []

    # Vendor validation

    if invoice_data["vendor"] not in approved_vendors:
        errors.append("Vendor not approved")

    # Amount validation

    if invoice_data["amount"] > credit_limit:
        errors.append("Amount exceeds credit limit")

    # Currency validation

    if invoice_data["currency"] not in allowed_currencies:
        errors.append("Invalid currency")

    # Due date validation

    try:
        due_date = datetime.strptime(
            invoice_data["due_date"],
            "%Y-%m-%d"
        )

        today = datetime.today()

        if due_date.date() <= today.date():
            errors.append("Due date is not in future")

    except:
        errors.append("Invalid due date format")

    # Final result

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }