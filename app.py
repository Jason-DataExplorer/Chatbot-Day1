import os

from linebot.models import *
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError


app = Flask(__name__)

Channel_Access_Token = ''
line_bot_api    = LineBotApi(Channel_Access_Token)
Channel_Secret  = ''
handler = WebhookHandler(Channel_Secret)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
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
