import os
import time
import random
import datetime
import tempfile, os

from linebot.models import *
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)


app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
Channel_Access_Token = ''
line_bot_api    = LineBotApi(Channel_Access_Token)
Channel_Secret  = ''
handler = WebhookHandler(Channel_Secret)

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '嗨' in msg:
        message = TextSendMessage(text="你好")
        line_bot_api.reply_message(event.reply_token, message)
    elif '你好' in msg:
        message = TextSendMessage(text="嗨")
        line_bot_api.reply_message(event.reply_token, message)

    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
