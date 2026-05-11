import requests


def call_api(
    url,
    method="POST",
    headers=None,
    payload=None
):

    try:

        if method == "POST":

            response = requests.post(
                url,
                json=payload,
                headers=headers
            )

        elif method == "GET":

            response = requests.get(
                url,
                headers=headers
            )

        else:

            return {
                "error": "Unsupported HTTP method"
            }

        return {

            "status_code": response.status_code,

            "response": response.json()
        }

    except Exception as e:

        return {

            "error": str(e)
        }


if __name__ == "__main__":

    result = call_api(

        url="https://jsonplaceholder.typicode.com/posts",

        method="POST",

        headers={
            "Content-Type": "application/json"
        },

        payload={
            "title": "Hello",
            "body": "FastAPI Test",
            "userId": 1
        }
    )

    print("\nAPI Response:\n")

    print(result)