import sys
import os
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from fastapi import FastAPI

from pydantic import BaseModel

from components.pdf_parser import parse_invoice

from components.llm_extractor import extract_invoice_data

from components.validator import validate_invoice


app = FastAPI()
app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


class WorkflowRequest(BaseModel):

    workflow: list


@app.get("/")

def home():

    return {

        "message": "AI Workflow API Running"
    }


@app.post("/run-workflow")

def run_workflow(request: WorkflowRequest):

    execution_log = []

    shared_data = {}

    workflow = request.workflow

    for step in workflow:

        component = step["component"]

        params = step["params"]

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

        execution_log.append({

            "component": component,

            "result": result
        })

    return {

        "status": "success",

        "execution_log": execution_log
    }