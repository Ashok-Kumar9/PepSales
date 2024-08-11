import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def process_transcripts():
    """Process all transcripts from the specified directory."""
    url = f"{BASE_URL}/process"
    data = {"transcript_dir": "transcripts"}
    response = requests.post(url, json=data)
    print("Process Transcripts Response:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    process_transcripts()