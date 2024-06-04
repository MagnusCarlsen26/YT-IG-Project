import json
import http.client
from dotenv import load_dotenv,dotenv_values
import os
load_dotenv()

def elevenlabs(text, voice_id, output_filename = 'audio'):
    conn = http.client.HTTPSConnection("api.elevenlabs.io")

    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": os.getenv('ELEVEN_LABS_API')
    }

    payload = {
        "text" : text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
    }

    conn.request("POST", f"/v1/text-to-speech/{voice_id}?optimize_streaming_latency=0", headers=headers, body=json.dumps(payload))

    response = conn.getresponse()

    if response.status == 200:
        with open(f"{output_filename}.mp3", "wb") as file:
            file.write(response.read())
        print("Speech generated successfully!")
    else:
        print("Error:", response.text)

    conn.close()
