from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('lg/Q13LFEGZLNjHw/RhW2QL2ee3aEBZMkylvPci9s7iNr2AcX90M+VNBbkshTpEyPk5E1Ns9MIOEANMwX4J+kkVFRWGKsoBmBEKLqt50AW5drehe8tOvJcNibSY3WZ/1BvNW216SeS9K3UqgHDDqJgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('26841c849fb02dbab9650951c54689a6')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()