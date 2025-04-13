name: Check Registration Status

on:
  schedule:
    - cron: '*/5 * * * *'  # 每5分钟运行一次
  workflow_dispatch:  # 手动触发工作流

jobs:
  check-registration-status:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4

      - name: Run registration check
        run: |
          python from-freecloud/check_registration.py  # 指定正确的脚本路径
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
