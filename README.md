# 🤖 Discord SelfBot - Python

A multi-purpose selfbot built with Python, using `discord.py 1.3.7`. It provides fun, admin, utility, and voice-related commands directly from your user account.

---

## ⚙️ Features

### 📄 General Commands
- `.help` — Shows the list of categories
- `.setprefix [prefix]` — Changes the bot's prefix
- `.set_lang [fr|en]` — Changes the bot's language

### 📊 Info
- `.ping` — Shows the bot's latency
- `.userinfo [@user]` — Displays user information
- `.serverinfo` — Displays server information

### 🔊 Voice
- `.joinvc [channel_id]` — Joins a voice channel
- `.mute` / `.unmute` — Mute or unmute the microphone
- `.cam` — Activates the camera
- `.voice` — Shows available voice commands

### 🎮 Fun
- `.gay [@user]` — Shows how gay someone is (in % 🏳️‍🌈)
- `.casino` — Mini slot machine game
- `.fun` — Displays fun commands

### 🛠 Utility
- `.pp [@user]` — Displays a user's avatar
- `.servericon` — Shows the server's icon
- `.utility` — Displays utility commands

### 🎯 Status
- `.set_status [online|idle|dnd|invisible]` — Changes your online status
- `.set_activity [playing|watching|listening|streaming] [text] [url?]` — Sets custom activity

---

## 🧪 Dependencies

`requirements.txt`:

```

discord.py==1.3.7
python-dotenv

```

---

## 🚀 Installation

1. **Clone the project**:
   ```bash
   git clone https://github.com/youruser/yourrepo.git
   cd yourrepo
``

2. **Create a `.env` file**:
   Example:

   ```env
   TOKEN=your_discord_token
   PREFIX=.
   LANG=en
   ```

3. **Install dependencies**:

   ```bash
   pip uninstall -y discord.py && pip install -r requirements.txt
   ```

4. **Run the bot**:

   ```bash
   python main.py
   ```

---

## ⚠️ Disclaimer

> ❗ **Using a selfbot violates Discord's Terms of Service.** Your account can be **banned**. This project is for **educational purposes only**.

---

## 📄 License

Open-source project licensed under the MIT License.


