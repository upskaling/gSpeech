import json

import requests


def translate_requests(url, input_text, source, target):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'gSpeech/1.0',
    }
    data = json.dumps({"q": input_text, "source": source, "target": target})
    response = requests.request('POST', url, data=data, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content)["translatedText"]
    return "Could not be translated!"
