# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Нет",
                "Не правда",
                "Врут",
            ]
        }

        res['response']['text'] = 'Привет! Ты красавчик!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'да',
        'ага',
        'спасибо',
        'правда',
        'согласен',
        'хорошо',
        'так и есть',
    ]:
        # Пользователь согласился, прощаемся.
        res['response']['text'] = 'На самом деле я наврал! Это просто мнение бездушного робота, но это не точно...'
        return

    # Если нет, то убеждаем его купить слона!
    res['response']['text'] = 'Все говорят "%s", а ты красавчик!' % (
        req['request']['original_utterance']
    )
    res['response']['buttons'] = get_suggests(user_id)

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "стать краше",
            "url": "https://market.yandex.ru/catalog--pomada/57332/list?text=%D0%BF%D0%BE%D0%BC%D0%B0%D0%B4%D0%B0%20%D0%B7%D0%B0%20%D1%81%D0%BE%D1%82%D0%BA%D1%83&hid=4748057&rt=9&was_redir=1&srnum=2380&rs=eJwzWspotICRay4jFy9H72FWASYJBlXWtdz7gNypJ1gFWIBcL7Xg_UDudCCXEcg9dnPdXi4-jqOLJ7MLMAP5Iv_U9nPxc8x8tpBJgEHiL6_qXgZ_e6CCuataWQQ4gQp-8JsfAPKPrQbyWSWUVJ2fHweZtw5oHhtQ2mWBMkh6R-cKNgF2IF__hT6I_w_E55BgVnXONjwQwAgAgoItSw%2C%2C&suggest_history=1",
            "hide": True
        })

    return suggests
