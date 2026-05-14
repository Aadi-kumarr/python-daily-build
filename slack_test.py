import os

import requests

from dotenv import load_dotenv


load_dotenv()


SLACK_WEBHOOK_URL = os.getenv(
    "SLACK_WEBHOOK_URL"
)


message = {

    "text": "Hello from AI Invoice Pipeline"
}


response = requests.post(

    SLACK_WEBHOOK_URL,

    json=message
)


print("\nStatus Code:\n")

print(response.status_code)

print("\nResponse:\n")

print(response.text)