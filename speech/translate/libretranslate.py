import json

import requests


def translate_libretranslate(url, input_text, source, target, key='False'):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'gSpeech/1.0',
    }
    data = {"q": input_text, "source": source, "target": target}
    if key != 'False':
        data['api_key'] = key

    data = json.dumps(data)
    response = requests.request('POST', url, data=data, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content)["translatedText"]
    return "Could not be translated!"
