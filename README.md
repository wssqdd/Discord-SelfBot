# 🤖 Discord SelfBot - Python

Un selfbot polyvalent construit en Python, utilisant `discord.py 1.3.7`. Il propose des commandes amusantes, d’administration, utilitaires et liées à la voix directement depuis ton compte utilisateur.

---

## ⚙️ Fonctionnalités

### 📄 Commandes générales

* `.help` — Affiche la liste des catégories
* `.setprefix [prefix]` — Change le préfixe du bot

### 📊 Informations

* `.ping` — Affiche la latence du bot
* `.userinfo [@user]` — Affiche les informations d’un utilisateur
* `.serverinfo` — Affiche les informations du serveur

### 🔊 Voix

* `.joinvc [channel_id]` — Rejoint un salon vocal
* `.mute` / `.unmute` — Coupe ou réactive le micro
* `.cam` — Active la caméra
* `.voice` — Affiche les commandes vocales disponibles

### 🎮 Fun

* `.gay [@user]` — Montre à quel point quelqu’un est gay (en % 🏳️‍🌈)
* `.casino` — Mini jeu de machine à sous
* `.fun` — Affiche les commandes fun

### 🛠 Utilitaires

* `.pp [@user]` — Affiche l’avatar d’un utilisateur
* `.servericon` — Affiche l’icône du serveur
* `.utility` — Affiche les commandes utilitaires

### 🎯 Statut

* `.set_status [online|idle|dnd|invisible]` — Change ton statut en ligne
* `.set_activity [playing|watching|listening|streaming] [texte] [url?]` — Définit une activité personnalisée

---

## 🧪 Dépendances

`requirements.txt` :

```
discord.py==1.3.7
python-dotenv
```

---

## 🚀 Installation

1. **Cloner le projet** :

   ```bash
   git clone https://github.com/youruser/yourrepo.git
   cd yourrepo
   ```

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

4. **Lancer le bot** :

   ```bash
   python main.py
   ```

---

## ⚠️ Avertissement

> ❗ **Utiliser un selfbot enfreint les Conditions d’Utilisation de Discord.** Ton compte peut être **banni**. Ce projet est **uniquement à des fins éducatives**.

---

## 📄 Licence

Projet open-source sous licence MIT.

---




