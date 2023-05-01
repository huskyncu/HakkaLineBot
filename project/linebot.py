# 引入Line Messaging API相關模組
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from info import rebackinfo
from openfile import pickup
from identify import identify

app = Flask(__name__)
# LINE BOT info
line_bot_api = LineBotApi(rebackinfo()['line_bot_api'])
handler = WebhookHandler(rebackinfo()['handler'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 定義處理收到文字訊息的函式
def handle_text_message(event):
    # 讀取收到的訊息內容
    keywords = pickup()
    user_msg = event.message.text
    if user_msg in keywords:
        # 如果使用者傳送的訊息符合內建回覆內容
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='這是內建的回覆：{}'.format(user_msg))
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='無法回覆')
        )
        # 如果使用者傳送的訊息不符合內建回覆內容
        # 這裡可以放您自己的回覆邏輯
        # openai回覆訊息
        # line_bot_api.push_message(event.source.user_id, TextSendMessage(text=openai_api(message_text)))



# 定義處理收到非文字訊息的函式
def handle_non_text_message(event):
    print(event.message.type)
    if event.message.type == 'image':
        msgID = event.message.id
        message_content = line_bot_api.get_message_content(msgID)
        with open(f'{msgID}.jpg', 'wb') as fd:
            fd.write(message_content.content)
        # Disable scientific notation for clarity
        text = identify(msgID)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=f'{text}'.replace('\n', '')))
        os.remove(f'{msgID}.jpg')
    # 使用回覆模式回應使用者
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='收到非文字訊息'))

# 將收到的事件分類處理


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    handle_text_message(event)


@handler.add(MessageEvent, message=[ImageMessage, VideoMessage, AudioMessage])
def handle_message(event):
    handle_non_text_message(event)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)

os.system('pause')
