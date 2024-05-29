import json
import http.client

def generate_speech(api_key = '693df1c8c8f3456f0a9a113ebb579f66', text, voice_id, output_filename):
    conn = http.client.HTTPSConnection("api.elevenlabs.io")

    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
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
        print("Error:", response.status)

    conn.close()
