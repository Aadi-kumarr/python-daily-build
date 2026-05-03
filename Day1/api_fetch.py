import requests
import json

API_URL = "https://jsonplaceholder.typicode.com/posts"

# Fetch data
try:
    response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print("Error fetching data:", e)
    data = []

# Check if data is available
if not data:
    print("No data fetched. Exiting.")
else:
    # Filter data
    filtered = [post for post in data if post["userId"] < 10]

    print(f"\nTotal filtered records: {len(filtered)}\n")
    print("Filtered Data:\n")
    print(json.dumps(filtered, indent=4))