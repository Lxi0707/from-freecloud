import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

URL = "https://freecloud.ltd/register"

# 添加更多的请求头，模拟真实浏览器行为
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://freecloud.ltd/",  # 确保 Referer 是正确的
}

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"  # 使用HTML格式来美化消息
    }
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print(f"Error sending message: {response.status_code}")
    else:
        print("Message sent successfully!")

def check_registration():
    session = requests.Session()  # 使用Session对象，可以保持会话，模拟浏览器行为
    try:
        response = session.get(URL, headers=HEADERS)  # 传入模拟的请求头
        if response.status_code != 200:
            send_telegram_message(f"<b>注册页面无法访问!</b>\n状态码: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 检查是否有"暂未开放注册"提示
        if "暂未开放注册" in soup.text:
            send_telegram_message("<b>注册页面暂未开放注册!</b>")
        elif "注册" in soup.text:  # 如果页面上有“注册”字样，说明注册开放
            send_telegram_message("<b>注册页面已开启注册!</b>")
        else:
            send_telegram_message("<b>无法识别注册状态</b>\n页面内容不符合预期")
    
    except Exception as e:
        send_telegram_message(f"<b>检测过程中出现错误:</b>\n{str(e)}")

if __name__ == "__main__":
    check_registration()
