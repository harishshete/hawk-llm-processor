import os
import requests

def push_to_db(data):
    print("Pushing processed documents to the database...")
    print("API_SERVER", os.getenv("API_SERVER"))
    api_server = os.getenv("API_SERVER", "hawk-apiserver-svc:3000")
    url = f"http://{api_server}/api/document/create"
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        json=data,
        headers=headers
    )

    if response.status_code == 201:
        print("Processed documents successfully pushed to the database.")
    else:
        print(f"Failed to push data. Status Code: {response.status_code}, Response: {response.text}")