import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import pandas as pd

from components.validator import validate_invoice
from components.llm_extractor import extract_invoice_data


results = []


test_cases = [

    {
        "id": "TC001",

        "name": "Valid invoice",

        "invoice": {

            "vendor":
            "BigTree Entertainment Pvt Ltd",

            "amount":
            500,

            "currency":
            "INR",

            "due_date":
            "2027-05-20"
        }
    },


    {
        "id": "TC011",

        "name":
        "Missing vendor",

        "invoice": {

            "vendor":
            "",

            "amount":
            500,

            "currency":
            "INR",

            "due_date":
            "2027-05-20"
        }
    },


    {
        "id": "TC012",

        "name":
        "Negative amount",

        "invoice": {

            "vendor":
            "BigTree Entertainment Pvt Ltd",

            "amount":
            -500,

            "currency":
            "INR",

            "due_date":
            "2027-05-20"
        }
    },


    {
        "id": "TC013",

        "name":
        "Invalid currency",

        "invoice": {

            "vendor":
            "BigTree Entertainment Pvt Ltd",

            "amount":
            500,

            "currency":
            "EUR",

            "due_date":
            "2027-05-20"
        }
    },


    {
        "id": "TC014",

        "name":
        "Past due date",

        "invoice": {

            "vendor":
            "BigTree Entertainment Pvt Ltd",

            "amount":
            500,

            "currency":
            "INR",

            "due_date":
            "2020-05-20"
        }
    }

]


for tc in test_cases:

    try:

        result = validate_invoice(

            tc["invoice"]
        )


        results.append({

            "Test ID":

            tc["id"],


            "Name":

            tc["name"],


            "Result":

            str(result),


            "Status":

            "PASS"
        })


    except Exception as e:


        results.append({

            "Test ID":

            tc["id"],


            "Name":

            tc["name"],


            "Result":

            str(e),


            "Status":

            "FAIL"
        })


df = pd.DataFrame(
    results
)


df.to_excel(

    "qa/test_results.xlsx",

    index=False
)


print(

    "\nAll tests completed\n"
)

print(df)