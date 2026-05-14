import os
import json
import traceback

from datetime import datetime

import requests

from dotenv import load_dotenv

from components.pdf_parser import parse_invoice
from components.llm_extractor import extract_invoice_data
from components.validator import validate_invoice


load_dotenv()


SLACK_WEBHOOK_URL = os.getenv(
    "SLACK_WEBHOOK_URL"
)


def send_slack_message(message):

    try:

        response = requests.post(

            SLACK_WEBHOOK_URL,

            json={
                "text": message
            }
        )

        return response.status_code

    except Exception as e:

        print("Slack Error:", e)

        return None


def run_pipeline(pdf_path):

    execution_log = []

    try:

        print("\nSTEP 1: PDF Parsing\n")

        parsed_data = parse_invoice(
            pdf_path
        )

        execution_log.append({

            "step": "pdf_parser",

            "result": parsed_data
        })


        print("\nSTEP 2: LLM Extraction\n")

        invoice_text = str(
            parsed_data
        )

        extracted_data = extract_invoice_data(
            invoice_text
        )

        execution_log.append({

            "step": "llm_extractor",

            "result": extracted_data
        })


        print("\nSTEP 3: Validation\n")

        if "error" in extracted_data:

            validation_result = {

                "valid": False,

                "errors": [
                    "LLM extraction failed"
                ]
            }

        else:

            validation_result = validate_invoice(
                extracted_data
            )

        execution_log.append({

            "step": "validator",

            "result": validation_result
        })


        print("\nSTEP 4: Save Logs\n")

        os.makedirs(
            "logs",
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        log_file = f"logs/run_{timestamp}.json"

        with open(log_file, "w") as f:

            json.dump(
                execution_log,
                f,
                indent=4
            )

        execution_log.append({

            "step": "logger",

            "result": log_file
        })


        print("\nSTEP 5: Slack Notification\n")

        slack_message = f"""
AI Invoice Pipeline Completed

Vendor: {parsed_data.get('vendor')}

Invoice Number: {parsed_data.get('invoice_no')}

Amount: {parsed_data.get('amount')}

Currency: {parsed_data.get('currency')}

Validation Status: {validation_result.get('valid')}

Log File: {log_file}
"""

        slack_status = send_slack_message(
            slack_message
        )

        execution_log.append({

            "step": "slack_notification",

            "result": slack_status
        })


        print("\nPipeline Completed Successfully\n")

        return execution_log


    except Exception as e:

        error_log = {

            "error": str(e),

            "traceback": traceback.format_exc()
        }

        execution_log.append(
            error_log
        )

        print("\nPipeline Failed\n")

        print(error_log)

        return execution_log


if __name__ == "__main__":

    result = run_pipeline(
        "day3/sample3.pdf"
    )

    print("\nFINAL EXECUTION LOG:\n")

    print(
        json.dumps(
            result,
            indent=4
        )
    )