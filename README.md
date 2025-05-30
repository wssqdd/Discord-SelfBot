# Discord Selfbot

A customizable Discord selfbot written in Python using `discord.py`. It includes various commands such as utility tools, voice controls, status customization, fun commands, and server/user information display.

**Disclaimer:** Selfbots are against Discord's Terms of Service and can lead to account termination. Use at your own risk and only in test environments.

---

## Features

- Ping and latency check (API and VPS)
- User and server information
- Voice channel control (join, mute, unmute, camera)
- Fun commands (e.g., gay percentage, casino)
- Utility commands (e.g., get profile/server icons)
- Status customization (activity, presence)
- Language switcher (`fr` or `en`)
- Customizable prefix via `.env` file

---

## Requirements

- Python 3.8 or higher
- `discord.py==1.3.7` (Not new version)
- `python-dotenv`
Or 

Install dependencies using:

```bash
pip install -r requirements.txt
````

Or install manually:

```bash
pip install discord.py python-dotenv
```

---

## .env Configuration

Create a `.env` file in your project root directory with the following content:

```env
TOKEN=your_discord_token_here
PREFIX=.
LANG=fr
```

---

## Running the Bot

Run the bot with:

```bash
python bot.py
```

The bot will log in using your account token and respond to your own messages as a selfbot.

```

---

Souhaites-tu aussi une version en français ?
```
