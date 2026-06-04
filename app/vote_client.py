import requests
import os


VM2_URL = os.environ.get("VM2_URL")
INTERNAL_API_KEY = os.environ.get("INTERNAL_API_KEY")


def send_vote(global_id: str, party: str):

    r = requests.post(
        f"{VM2_URL}/vote",
        json={
            "global_id": global_id,
            "party": party
        },
        headers={
            "x-api-key": INTERNAL_API_KEY
        }
    )

    return r.json()
