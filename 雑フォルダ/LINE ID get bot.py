# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 14:31:12 2025

@author: PC_User
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ご自身のLINEチャネルアクセストークン・チャネルシークレットに置き換えてください
LINE_CHANNEL_ACCESS_TOKEN = "K8zU1TzCE83lgdIblvZT21+lbPu+HGl6wLbrGxXBAGPHAcuXGP7A40/1qTuJfSRwuMkKNEF/YR7mqhFY3iJZsH4l9c31li7xwBZdKnAQjBecgl1Wm9uuLKJJ1+IK8wb9jboJsj8tda4/dUAhEGm+zAdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "654ac08e8968540fb196b088872e4582"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')

    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type == 'group':
        group_id = event.source.group_id
        # グループIDをログに表示
        print(f"グループID: {group_id}")

        # グループに返信
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"このグループIDは {group_id} です。")
        )
    else:
        # 個人トークやルームの場合
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="このBotはグループでのみグループIDを取得します。")
        )

if __name__ == "__main__":
    app.run(port=8000)