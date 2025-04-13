import requests
from bs4 import BeautifulSoup
import os
from telegram import Bot
from telegram.constants import ParseMode
import datetime
import sys

URL = "https://freecloud.ltd/register"
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def check_registration_status():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        if "注册" in response.text and "暂未开放" not in response.text:
            return "🟢 注册开放"
        elif "暂未开放" in response.text:
            return "🔴 注册关闭"
        return "🟡 状态未知"
    except Exception as e:
        return f"⚠️ 错误: {str(e)}"

def send_notification(message):
    bot = Bot(token=BOT_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text=f"""<b>🏠 注册状态检查</b>
🔗 页面: <code>{URL}</code>
📊 状态: {message}
⏰ 时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}""",
        parse_mode=ParseMode.HTML
    )

if __name__ == "__main__":
    status = check_registration_status()
    print(f"status={status}")  # 关键输出格式
    send_notification(status)
