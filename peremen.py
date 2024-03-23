YA_TOKEN = """t1.9euelZqVyZnKks-Rzo6SnJCJl5LNle3rnpWak86VyJDIl5qJnJyRz42VlZPl8_doKARQ-e9ZdgMl_d3z9yhXAVD571l2AyX9zef1656VmpiMzM-NzZ2ZlMeQjZeMz46Q7_zF656Vmp
iMzM-NzZ2ZlMeQjZeMz46QveuelZrMk8iYxsrPip6Ky5KdmpLGnLXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.vcHapFf3m5W4Ss-eNkdfCrUCrzc4uVgdpYJLuZkxe81rBIbuQz0sZfyFpyY
BodEb9DAVSYis_LbtfloeRY2mDg"""

FOLDER_ID = """b1gde3s455bjvigr5njg"""

MAX_PROJECT_TOKENS = 15000 # макс. количество токенов на весь проект
MAX_USERS = 5 # макс. количество пользователей на весь проект
MAX_SESSIONS = 3 # макс. количество сессий у пользователя
MAX_TOKENS_IN_SESSION = 1000 # макс. количество токенов за сессию пользователя
MAX_MODEL_TOKENS = 100
GPT_MODEL = 'yandexgpt'
API = "6754279303:AAFcNoE1ZvLHgsFRe1w6Z7CiYyha5JlX_GY"
MODEL_TEMPERATURE = 0.6

cur_sen = {}

SYSTEM_PROMPT = (
    "Ты пишешь историю вместе с человеком. "
    "Историю вы пишете по очереди. Начинает человек, а ты продолжаешь. "
    "Если это уместно, ты можешь добавлять в историю диалог между персонажами. "
    "Диалоги пиши с новой строки и отделяй тире. "
    "Не пиши никакого пояснительного текста в начале, а просто логично продолжай историю."
)

CONTINUE_STORY = 'Продолжи сюжет в 1-3 предложения и оставь интригу. Не пиши никакой пояснительный текст от себя'
END_STORY = 'Напиши завершение истории c неожиданной развязкой. Не пиши никакой пояснительный текст от себя'