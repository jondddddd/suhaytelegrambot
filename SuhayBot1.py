import requests
import os, signal

from flask import Flask
from flask import request
from flask import Response
import openai

openai.api_key = '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'

TOKEN = "6225221230:AAFZQzUzCF22VdijA74ZksYJneOlKVC5Nls"

app = Flask(__name__)

conversations = {}


def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("Text :", txt)
    return chat_id, txt


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': {
            'keyboard': [['Help me make a Resume']],
            'one_time_keyboard': True,
            'resize_keyboard': True
        }
    }

    response = requests.post(url, json=payload)
    return response


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        chat_id, txt = parse_message(msg)

        if chat_id not in conversations:
            conversations[chat_id] = [
                {"role": "system", "content": "you are Suhay a Resume bot that will help you organize your work Experience. You will help the user organize their work experience. You will be asking at most 3 work experiences they have had. Ask these questions one by one. You should ask individual questions. Do not dump multiple questions. Once they reply with their answer, return that answer in a organized format for a resume. Ask questions one by one. Add flair to the job descriptions when sending it back to them."}]

        conversations[chat_id].append({"role": "user", "content": txt})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversations[chat_id]
        )
        response = completion['choices'][0]['message']['content']
        print("ChatGPT response: ", response)
        tel_send_message(chat_id, response)

        conversations[chat_id].append({"role": "assistant", "content": response})

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
