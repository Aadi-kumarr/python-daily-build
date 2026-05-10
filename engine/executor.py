import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import json

from datetime import datetime

from components.pdf_parser import parse_invoice

from components.llm_extractor import extract_invoice_data

from components.validator import validate_invoice

workflow = [

    {
        "step": 1,

        "component": "pdf_parser",

        "params": {

            "pdf_path": "day3/sample3.pdf"
        }
    },

    {
        "step": 2,

        "component": "llm_extractor",

        "params": {}
    },

    {
        "step": 3,

        "component": "validator",

        "params": {}
    }

]


execution_log = []

shared_data = {}


for step in workflow:

    step_number = step["step"]

    component = step["component"]

    params = step["params"]

    print("\n===================================")

    print(f"Running Step {step_number}")

    print(f"Component: {component}")

    if component == "pdf_parser":

        result = parse_invoice(
            params["pdf_path"]
        )

        shared_data["invoice_data"] = result

    elif component == "llm_extractor":

        invoice_text = str(
            shared_data["invoice_data"]
        )

        result = extract_invoice_data(
            invoice_text
        )

        shared_data["invoice_data"] = result

    elif component == "validator":

        result = validate_invoice(
            shared_data["invoice_data"]
        )

        shared_data["validation_result"] = result

    else:

        result = {

            "error": "Unknown component"
        }

    log_entry = {

        "step": step_number,

        "component": component,

        "result": result
    }

    execution_log.append(
        log_entry
    )

    print("\nResult:\n")

    print(result)


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


print("\n===================================")

print("Workflow Execution Completed")

print(f"\nExecution log saved to:\n{log_file}")