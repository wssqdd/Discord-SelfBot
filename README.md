# 🤖 Discord SelfBot - Python

Un selfbot multifonctions développé en Python, compatible avec `discord.py 1.3.7`. Il permet d’exécuter diverses commandes utiles, amusantes et administratives directement depuis votre compte.

---

## ⚙️ Fonctions disponibles

### 📄 Commandes générales
- `.help` — Affiche la liste des catégories
- `.setprefix [préfixe]` — Change le préfixe du selfbot
- `.set_lang [fr|en]` — Change la langue du selfbot

### 📊 Info
- `.ping` — Mesure la latence entre le bot et Discord
- `.userinfo [@user]` — Affiche les infos d'un utilisateur
- `.serverinfo` — Affiche les infos du serveur

### 🔊 Voice
- `.joinvc [channel_id]` — Rejoint un salon vocal
- `.mute` / `.unmute` — (Dé)mute le micro
- `.cam` — Active la caméra
- `.voice` — Affiche les commandes vocales

### 🎮 Fun
- `.gay [@user]` — Montre à combien de % quelqu'un est gay 🏳️‍🌈
- `.casino` — Mini machine à sous
- `.fun` — Affiche les commandes fun

### 🛠 Utility
- `.pp [@user]` — Montre l’avatar de l’utilisateur
- `.servericon` — Montre l’icône du serveur
- `.utility` — Affiche les commandes utility

### 🎯 Status
- `.set_status [online|idle|dnd|invisible]` — Modifie le statut
- `.set_activity [playing|watching|listening|streaming] [texte] [url?]` — Modifie l’activité

---

## 🧪 Dépendances

Fichier `requirements.txt` :

```

discord.py==1.3.7
python-dotenv

````

---

## 🚀 Installation

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/tonuser/tonrepo.git
   cd tonrepo
````

2. **Créer un fichier `.env`** :
   Exemple :

   ```env
   TOKEN=ton_token_discord
   PREFIX=.
   LANG=fr
   ```

3. **Installer les dépendances** :

   ```bash
   pip uninstall -y discord.py && pip install -r requirements.txt
   ```

4. **Lancer le selfbot** :

   ```bash
   python main.py
   ```

---

## 🛡 Avertissement

> ❗ **L'utilisation des selfbots est contraire aux Conditions d'utilisation de Discord.** Ton compte peut être **banni**. Ce projet est à but éducatif uniquement.

---

## 📄 Licence

Projet open-source sous licence MIT.

