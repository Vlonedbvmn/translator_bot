import json
import logging
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.picture_message import PictureMessage
from viberbot.api.messages.keyboard_message import KeyboardMessage
from viberbot.api.messages.video_message import VideoMessage
from viberbot.api.messages.url_message import URLMessage
from viberbot.api.messages.url_message import URLMessage
from viberbot.api.viber_requests import ViberFailedRequest, ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
import smtplib, ssl
from email.mime.text import MIMEText
import threading
import time
import sched
from threading import Thread
from googletrans import Translator

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='translator',
    avatar='',
    auth_token='c8b934dc6a366b467d06c-c8b93c83ac8b93ef1c3b9-c8b9316386a3db6f3e3a3'
))

info_user = {}


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

counter = 0
translator = Translator()

@app.route('/', methods=['POST'])
def incoming():
    # print("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())


    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        text = message.text
        text = text.split('|')
        text_type = text[0]
        text_message = ''

        tracking_data = message.tracking_data
        if tracking_data is None:
            tracking_data = {}
        else:
            tracking_data = json.loads(tracking_data)
        keyboarda = {
            "DefaultHeight": True,
            "Type": "keyboard",
            "Buttons": [
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "ActionType": 'reply',
                    "ActionBody": 'eng',
                    "ReplyType": "message",
                    "Text": 'english'
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "ActionType": 'reply',
                    "ActionBody": 'tochki',
                    "ReplyType": "message",
                    "Text": 'spanish'
                },
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "ActionType": 'reply',
                    "ActionBody": 'sales',
                    "ReplyType": "message",
                    "Text": 'french'
                }
            ]
        }
        if text_type == 'eng':
            gogo = viber_request.message
            keyboard = {
                "DefaultHeight": True,
                "Type": "keyboard",
                "Buttons": [
                    {
                        "Columns": 3,
                        "Rows": 1,
                        "BgColor": "#e6f5ff",
                        "ActionType": 'reply',
                        "ActionBody": 'menu',
                        "ReplyType": "message",
                        "Text": 'english'
                    },
                    {
                        "Columns": 3,
                        "Rows": 1,
                        "BgColor": "#e6f5ff",
                        "ActionType": 'reply',
                        "ActionBody": 'tochki',
                        "ReplyType": "message",
                        "Text": 'spanish'
                    },
                    {
                        "Columns": 6,
                        "Rows": 1,
                        "BgColor": "#e6f5ff",
                        "ActionType": 'reply',
                        "ActionBody": 'sales',
                        "ReplyType": "message",
                        "Text": 'french'
                    }
                ]
            }
            viber.send_messages(viber_request.sender.id, [
                TextMessage(text=str(translator.translate(gogo.text, dest='ja').text), keyboard=keyboard)
            ])





    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("client failed receiving message. failure: {0}".format(viber_request))
    elif isinstance(viber_request, ViberConversationStartedRequest):
        keyboard = {
            "DefaultHeight": True,
            "Type": "keyboard",
            "Buttons": [
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "ActionType": 'reply',
                    "ActionBody": 'eng',
                    "ReplyType": "message",
                    "Text": 'english'
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "ActionType": 'reply',
                    "ActionBody": 'tochki',
                    "ReplyType": "message",
                    "Text": 'spanish'
                },
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "ActionType": 'reply',
                    "ActionBody": 'sales',
                    "ReplyType": "message",
                    "Text": 'french'
                }
            ]
        }
        viber.send_messages(viber_request.user.id, [
            TextMessage(text='Hi its translation bot. Choose on which you prefer to translate', keyboard=keyboard)
        ])


    return Response(status=200)


def web_hook(viber):
    viber.set_webhook('https://e634cb462f5b.ngrok.io')
if __name__ == '__main__':
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, web_hook, (viber,))
    th = Thread(target=scheduler.run)
    th.start()
    print(threading.current_thread())
    infoh = []
    app.run(host='127.0.0.1', port=5000, debug=True, )
