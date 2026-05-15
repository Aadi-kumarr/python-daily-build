import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from logs.logger_config import logger

from datetime import datetime

from pydantic import BaseModel
from pydantic import ValidationError


class InvoiceData(BaseModel):

    vendor: str

    amount: float

    currency: str

    due_date: str


approved_vendors = [

    "BigTree Entertainment Pvt Ltd",

    "InterGlobe Aviation Limited",

    "Roppen Transportation Services Private Limited"
]


credit_limit = 10000


allowed_currencies = [

    "INR",

    "USD"
]


def validate_invoice(
    invoice_dict
):

    logger.info(

        "Started invoice validation"
    )


    errors = []


    try:

        invoice = InvoiceData(

            **invoice_dict
        )


    except ValidationError as e:


        logger.error(

            f"Pydantic validation failed: {e}"
        )


        return {

            "valid": False,

            "errors": [

                str(e)
            ]
        }


    if not invoice.vendor:


        errors.append(

            "Vendor is missing"
        )


    if invoice.vendor not in approved_vendors:


        errors.append(

            "Vendor not approved"
        )


    if invoice.amount > credit_limit:


        errors.append(

            "Amount exceeds credit limit"
        )


    if invoice.amount <= 0:


        errors.append(

            "Invalid invoice amount"
        )


    if invoice.currency not in allowed_currencies:


        errors.append(

            "Invalid currency"
        )


    try:


        try:


            due_date = datetime.strptime(

                invoice.due_date,

                "%Y-%m-%d"
            )


        except:


            due_date = datetime.strptime(

                invoice.due_date,

                "%a, %d %b, %Y"
            )


        today = datetime.today()


        if due_date.date() <= today.date():


            errors.append(

                "Due date is not in future"
            )


    except Exception as e:


        logger.error(

            f"Date parsing failed: {e}"
        )


        errors.append(

            "Invalid due date format"
        )


    if len(errors) == 0:


        logger.info(

            "Invoice validation successful"
        )


    else:


        logger.error(

            f"Validation errors: {errors}"
        )


    return {

        "valid":

        len(errors) == 0,

        "errors":

        errors
    }


if __name__ == "__main__":


    sample_invoice = {

        "vendor":

        "BigTree Entertainment Pvt Ltd",

        "amount":

        63.72,

        "currency":

        "INR",

        "due_date":

        "2027-05-10"
    }


    result = validate_invoice(

        sample_invoice
    )


    print(

        "\nValidation Result:\n"
    )


    print(
        result
    )