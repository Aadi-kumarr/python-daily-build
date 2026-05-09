import os
import json

from dotenv import load_dotenv

from pydantic import BaseModel
from pydantic import ValidationError
from langchain_core.prompts import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI


# LOAD ENV VARIABLES

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found")


# LLM SETUP

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# PYDANTIC SCHEMA

class WorkflowStep(BaseModel):

    step: int
    component: str
    params: dict


# PROMPT TEMPLATE

prompt = PromptTemplate(
    input_variables=["command"],

    template="""
You are an AI workflow engine.

Convert the user command into workflow JSON.

Available components:
- email_reader
- excel_comparer
- sap_entry
- validator
- llm_extractor

Rules:
- Return ONLY valid JSON
- Output must be a JSON array
- Each step must contain:
    - step
    - component
    - params

Examples:

User Command:
Read latest emails

Output:
[
    {{
        "step": 1,
        "component": "email_reader",
        "params": {{
            "folder": "inbox",
            "limit": 10
        }}
    }}
]

User Command:
{command}
"""
)


# TEST COMMANDS

commands = [

    "Read latest emails from inbox",

    "Compare two excel sheets and find mismatches",

    "Enter invoice data into SAP"

]


# PROCESS COMMANDS

for command in commands:

    print("\n===================================")
    print("USER COMMAND:")
    print(command)

    # CREATE FINAL PROMPT

    final_prompt = prompt.format(
        command=command
    )

    # CALL LLM

    try:

        response = llm.invoke(
            final_prompt
        )

        raw_output = response.content

    except Exception as e:

        print("LLM Error:", e)
        continue

    # CLEAN JSON

    raw_output = raw_output.replace(
        "```json",
        ""
    )

    raw_output = raw_output.replace(
        "```",
        ""
    )

    raw_output = raw_output.strip()

    # PARSE JSON

    try:

        workflow = json.loads(
            raw_output
        )

    except Exception as e:

        print("JSON Parse Error:", e)
        continue

    # VALIDATE WORKFLOW

    validated_steps = []

    try:

        for step in workflow:

            validated_step = WorkflowStep(
                **step
            )

            validated_steps.append(
                validated_step.model_dump()
            )

    except ValidationError as e:

        print("Validation Error:", e)
        continue

    # FINAL OUTPUT

    print("\nWORKFLOW JSON:\n")

    print(
        json.dumps(
            validated_steps,
            indent=4
        )
    )