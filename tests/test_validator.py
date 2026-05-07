import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from components.validator import validate_invoice
# Test 1: Valid invoice

def test_valid_invoice():

    invoice = {
        "vendor": "BigTree Entertainment Pvt Ltd",
        "amount": 500,
        "currency": "INR",
        "due_date": "2027-05-10"
    }

    result = validate_invoice(invoice)

    assert result["valid"] == True
    assert result["errors"] == []


# Test 2: Invalid vendor

def test_invalid_vendor():

    invoice = {
        "vendor": "Fake Vendor",
        "amount": 500,
        "currency": "INR",
        "due_date": "2027-05-10"
    }

    result = validate_invoice(invoice)

    assert result["valid"] == False
    assert "Vendor not approved" in result["errors"]


# Test 3: Amount exceeds limit

def test_credit_limit():

    invoice = {
        "vendor": "BigTree Entertainment Pvt Ltd",
        "amount": 20000,
        "currency": "INR",
        "due_date": "2027-05-10"
    }

    result = validate_invoice(invoice)

    assert result["valid"] == False
    assert "Amount exceeds credit limit" in result["errors"]


# Test 4: Invalid currency

def test_invalid_currency():

    invoice = {
        "vendor": "BigTree Entertainment Pvt Ltd",
        "amount": 500,
        "currency": "EUR",
        "due_date": "2027-05-10"
    }

    result = validate_invoice(invoice)

    assert result["valid"] == False
    assert "Invalid currency" in result["errors"]


# Test 5: Past due date

def test_past_due_date():

    invoice = {
        "vendor": "BigTree Entertainment Pvt Ltd",
        "amount": 500,
        "currency": "INR",
        "due_date": "2020-01-01"
    }

    result = validate_invoice(invoice)

    assert result["valid"] == False
    assert "Due date is not in future" in result["errors"]