import requests
from bs4 import BeautifulSoup
import os
from telegram import Bot
from telegram.constants import ParseMode
import datetime

URL = "https://freecloud.ltd/register"
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def check_registration_status():
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        if "注册" in response.text and "暂未开放" not in response.text:
            return "🟢 注册页面开放中！"
        elif "暂未开放" in response.text:
            return "🔴 注册暂未开放"
        else:
            return "🟡 无法确定注册状态"
    except Exception as e:
        return f"⚠️ 检查出错: {str(e)}"

def send_notification(message):
    bot = Bot(token=BOT_TOKEN)
    html_message = f"""
    <b>🏠 FreeCloud 注册状态检查</b>
    🔗 <b>页面:</b> <code>{URL}</code>
    📊 <b>状态:</b> {message}
    ⏰ <b>时间:</b> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    bot.send_message(
        chat_id=CHAT_ID,
        text=html_message,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

if __name__ == "__main__":
    status = check_registration_status()
    print(f"status={status}")  # GitHub Actions 会自动捕获输出
    send_notification(status)
