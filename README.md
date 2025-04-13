# 基于freecloud的注册检测

## 默认cron: '*/5 * * * *'

*/5 表示 "每5分钟"（符合 GitHub 免费账户的最低限制）。

其他时间字段保持 *，表示 "每小时、每天、每月、每周" 都运行。


## 准备工作：

在 GitHub 仓库的 Settings > Secrets 中添加两个 secrets：

TELEGRAM_BOT_TOKEN: 你的 Telegram Bot Token

TELEGRAM_CHAT_ID: 你的 Telegram 聊天 ID

## 运行频率：

默认设置为每5分钟运行一次

首次需要手动触发工作流
