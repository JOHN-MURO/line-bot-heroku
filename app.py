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
    group_id = getattr(event.source, "group_id", None)
    if group_id:
        print(f"💬 メッセージ受信時のグループID: {group_id}")
        reply_text = f"あなたのメッセージ：{event.message.text}\nグループIDは {group_id} です"
    else:
        reply_text = f"あなたのメッセージ：{event.message.text}\nこのトークにはグループIDはありません。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)