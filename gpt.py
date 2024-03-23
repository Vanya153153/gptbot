import requests

from peremen import *


def count_tokens_in_dialogue(messages):
    headers = {
        'Authorization': f'Bearer {YA_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
       "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
       "maxTokens": MAX_MODEL_TOKENS,
       "messages": []
    }

    for row in messages:
        data["messages"].append(
            {
                "role": row["role"],
                "text": row["text"]
            }
        )

    return len(
        requests.post(
            "https://llm.api.cloud.yandex.net/foundationModels/v1/tokenizeCompletion",
            json=data,
            headers=headers
        ).json()["tokens"]
    )


def create_promt(data, user_id):
    promt = (f"Напиши историю в жанре {data[user_id]['genre']} про {data[user_id]['character']},"
             f"для которого действие происходит в {data[user_id]['setting']}.")

    if data[user_id]['additionally'] != '':
        promt += f"Также не забудь учесть эти детали: {data[user_id]['additionally']}"

    return promt


def ask_gpt(messages):
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
            'Authorization': f'Bearer {YA_TOKEN}',
            'Content-Type': 'application/json'
    }

    data = {
        "modelUri": f"gpt://{FOLDER_ID}/{GPT_MODEL}/latest",
        "completionOptions": {
            "stream": False,
            "temperature": MODEL_TEMPERATURE,
            "maxTokens": MAX_MODEL_TOKENS
        },
        "messages": []
    }

    for message in messages:
        data['messages'].append(message)

    status = False

    try:
        resp = requests.post(url, headers=headers, json=data)
        if resp.status_code != 200:
            err_text = f'Status code: {resp.status_code}'
            return err_text, status
        result = resp.json()['result']['alternatives'][0]['message']['text']
        status = True
    except Exception as e:
        result = f'Произошла непредвиденная ошибка во время выполнения запроса {e}'
        print(result)

    return result, status
