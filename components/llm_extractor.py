import os
import json
import re
import time
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from logs.logger_config import logger

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic import ValidationError

from google import genai


load_dotenv()


API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


if not API_KEY:

    raise ValueError(
        "GEMINI_API_KEY not found"
    )


client = genai.Client(

    api_key=API_KEY
)


class InvoiceData(BaseModel):

    vendor: str | None
    invoice_no: str | None
    amount: float | None
    currency: str | None
    due_date: str | None
    line_items: list[str]


with open(
    "prompts/invoice_extract.txt",
    "r"
) as f:

    base_prompt = f.read()


def extract_invoice_data(
    invoice_text
):

    logger.info(

        "Started LLM extraction"
    )

    raw_output = "{}"

    for attempt in range(3):

        try:

            logger.info(

                f"Gemini API attempt {attempt+1}"
            )

            response = client.models.generate_content(

                model="gemini-2.5-flash",

                contents=
                base_prompt
                + "\n"
                + invoice_text
            )

            raw_output = response.text


            logger.info(

                "LLM extraction successful"
            )

            break


        except Exception as e:

            logger.error(

                f"Gemini failed attempt {attempt+1}: {e}"
            )

            time.sleep(2)


    if raw_output == "{}":

        logger.error(

            "LLM extraction failed after 3 retries"
        )

        return {

            "error":

            "Gemini API failed after retries"
        }


    raw_output = raw_output.replace(

        "```json",

        ""
    )


    raw_output = raw_output.replace(

        "```",

        ""
    )


    raw_output = raw_output.strip()


    try:

        parsed_json = json.loads(

            raw_output
        )


        logger.info(

            "JSON parsing successful"
        )


    except Exception as e:


        logger.error(

            f"Invalid JSON: {e}"
        )


        return {

            "error":

            f"Invalid JSON: {str(e)}"
        }


    try:

        invoice = InvoiceData(

            **parsed_json
        )


        logger.info(

            "Pydantic validation successful"
        )


    except ValidationError as e:


        logger.error(

            f"Pydantic validation failed: {e}"
        )


        invoice = InvoiceData(

            vendor=None,

            invoice_no=None,

            amount=None,

            currency=None,

            due_date=None,

            line_items=[]
        )


    if not invoice.currency:


        text_lower = invoice_text.lower()


        if (

            "₹" in invoice_text

            or "inr" in text_lower

            or "rupee" in text_lower
        ):

            invoice.currency = "INR"


        elif (

            "$" in invoice_text

            or "usd" in text_lower
        ):

            invoice.currency = "USD"


        elif (

            "€" in invoice_text

            or "eur" in text_lower
        ):

            invoice.currency = "EUR"


        else:

            invoice.currency = "INR"


    if not invoice.due_date:


        match = re.search(

            r"(Sun,\s*\d{1,2}\s*[A-Za-z]+,\s*\d{4})",

            invoice_text
        )


        if match:

            invoice.due_date = match.group(
                1
            )


    logger.info(

        "LLM extraction completed"
    )


    return invoice.model_dump()


if __name__ == "__main__":


    invoice_text = """

    Invoice issued by : BigTree Entertainment Pvt Ltd

    Invoice Number : TIN262701834202

    Date of issue : Sun, 5 Apr, 2026

    Total Amount after Tax : 63.72

    Product: Project Hail Mary

    """


    result = extract_invoice_data(

        invoice_text
    )


    print(

        "\nFinal Validated Output:\n"
    )


    print(
        result
    )