name: Check Registration Status

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  check-registration:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4 python-telegram-bot

      - name: Run registration check
        id: check
        shell: bash
        run: |
          cat << 'EOF' > check_registration.py
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
                  return f"⚠️ 检查注册状态时出错: {str(e)}"

          def send_telegram_notification(message):
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
              print(f"status={status}") >> $GITHUB_OUTPUT
              send_telegram_notification(status)
          EOF

          python check_registration.py
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}

      - name: Show result
        run: echo "检查结果: ${{ steps.check.outputs.status }}"
