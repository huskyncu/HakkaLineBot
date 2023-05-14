# 引入Line Messaging API相關模組
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import PostbackAction, URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import threading
from info import rebackinfo
from openfile import pickup, pickup2,pickup_img
from identify import identify
from webhook_mod import initial, verify
from open_ai import openai_api
from firebase_ import insert_ele,shop_ele
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
    if user_msg not in keywords:
        line_bot_api.push_message(event.source.user_id, TextSendMessage(
                text=openai_api(user_msg)))
    # else:
    #     if "我要" in user_msg:
    #         ans = insert_ele(event.message.userId,user_msg.replace('我要','\n'))
    #         txt = ""
    #         for i in ans:
    #             txt+=i
    #         line_bot_api.push_message(event.source.userId,TextSendMessage(text=txt))
    #     elif "拿取" in user_msg:
    #         shop_ele(event.message.userId,user_msg.replace('拿取','\n'))
            


# 定義處理收到非文字訊息的函式
def handle_non_text_message(event):
    print(event.message.type)
    if event.message.type == 'image':
        msgID = event.message.id
        message_content = line_bot_api.get_message_content(msgID)
        with open(f'{msgID}.jpg', 'wb') as fd:
            fd.write(message_content.content)
        # Disable scientific notation for clarity
        ans_text = identify(msgID)
        ans_text = ans_text.replace('\n','')
        list1 = pickup2()
        if ans_text in list1:
            print(ans_text,list1)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(
                    text=f'您拍的應該是{ans_text}'.replace('\n', ''))
            )
            line_bot_api.push_message(
                event.source.user_id, TemplateSendMessage(
                    alt_text='ButtonsTemplate',
                    template=ButtonsTemplate(
                    thumbnail_image_url=f'{pickup_img(ans_text)}',
                    title=f'{ans_text}',
                    text=f'請點選以下動作',
                    actions=[
                        # PostbackAction(
                        #     label='postback',
                        #     data='發送 postback'
                        # ),
                        MessageAction(
                            label=f'我想知道{ans_text}是什麼',
                            text=f'我想知道{ans_text}是什麼'
                        )
                        # URIAction(
                        #     label='前往 STEAM 教育學習網',
                        #     uri='https://steam.oxxostudio.tw'
                        # )
                    ]
                )
            ))
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(
                    text=f'{ans_text}'.replace('\n', ''))
            )
        os.remove(f'{msgID}.jpg')
    # 使用回覆模式回應使用者
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='收到非文字訊息'))

# 將收到的事件分類處理


@ handler.add(MessageEvent, message = TextMessage)
def handle_message(event):
    handle_text_message(event)


@ handler.add(MessageEvent, message = [ImageMessage, VideoMessage, AudioMessage])
def handle_message(event):
    handle_non_text_message(event)

def running():
    app.run("0.0.0.0", port = 80)


if __name__ == "__main__":
    driver=initial()
    # port = int(os.environ.get('PORT', 80))
    t1=threading.Thread(target = running)
    t=threading.Thread(target = verify, args = (driver,))
    t.start()
    t1.start()
