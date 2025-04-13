import requests
from bs4 import BeautifulSoup
import os

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

URL = "https://freecloud.ltd/register"

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
    try:
        response = requests.get(URL)
        if response.status_code != 200:
            send_telegram_message("<b>注册页面无法访问!</b>\n状态码: {response.status_code}")
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
