# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです。
"""

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, JoinEvent
import os

app = Flask(__name__)

# 環境変数から読み込み
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(JoinEvent)
def handle_join(event):
    group_id = event.source.group_id
    print(f"✅ Botがグループに参加しました。Group ID: {group_id}")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="こんにちは！Botが参加しました。よろしくお願いします！")
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"あなたのメッセージ：{event.message.text}")
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Heroku環境変数PORTを使用
    app.run(host="0.0.0.0", port=port)