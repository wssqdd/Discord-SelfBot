import discord
import os
import time
from dotenv import load_dotenv
import asyncio
import datetime
import json
import random

start_time = datetime.datetime.now()

intents = discord.Intents.all()

load_dotenv(dotenv_path="C:/Github/.env")
TOKEN = os.getenv("TOKEN")
current_prefix = os.getenv("PREFIX", ".")
current_lang = os.getenv("LANG", "fr")

client = discord.Client(intents=intents)

current_lang = "fr"  # Langue par défaut

@client.event
async def on_ready():
    print(f"✅ Connecté en tant que {client.user} (ID: {client.user.id})")
    print("🔧 Selfbot prêt à recevoir des commandes.")

def update_env_lang(new_lang):
    lines = []
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("LANG="):
                lines.append(f"LANG={new_lang}\n")
            else:
                lines.append(line)
    with open(".env", "w") as f:
        f.writelines(lines)


def update_env_prefix(new_prefix):
    lines = []
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("PREFIX="):
                lines.append(f"PREFIX={new_prefix}\n")
            else:
                lines.append(line)
    with open(".env", "w") as f:
        f.writelines(lines)

@client.event
async def on_message(message):
    global current_prefix, current_lang

    if message.author.id != client.user.id:
        return

    msg = message.content

    # Commande pour changer la langue
    if msg.startswith(f"{current_prefix}set_lang"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Usage : `.set_lang [fr|en]`")
            await asyncio.sleep(5)
            await message.delete()
            return
        
        lang = parts[1].lower()
        if lang in ["fr", "en"]:
            current_lang = lang
            await message.edit(content=f"Langue changée en `{current_lang}`")
        else:
            await message.edit(content="Langue non supportée (seulement fr ou en).")
        await asyncio.sleep(5)
        await message.delete()
        return

    # Dispatcher selon la langue
    if current_lang == "fr":
        await handle_message_fr(message, current_prefix)
    elif current_lang == "en":
        await handle_message_en(message, current_prefix)


async def handle_message_fr(message, prefix):
    msg = message.content
    global current_prefix

    if msg == f"{current_prefix}ping":
        api_latency = round(client.latency * 1000)

        # Mesure latence VPS -> Discord
        start = time.perf_counter()
        async with message.channel.typing():
            pass
        end = time.perf_counter()
        vps_latency = round((end - start) * 1000)

        await message.edit(content=(
            f"> **API Discord** : {api_latency}ms\n"
            f"> **VPS** : {vps_latency}ms"
        ))
        await asyncio.sleep(5)
        await message.delete()
        await asyncio.sleep(10)
        await message.delete()
    if msg.startswith(f"{current_prefix}userinfo"):
        if len(message.mentions) > 0:
            user = message.mentions[0]  # premier utilisateur mentionné
        else:
            user = message.author  # si pas de mention, on prend l'auteur du message

        await message.edit(content=f"""
            > **Nom:** {user.name}
            > **ID:** {user.id}
            > **Date de création du compte:** {user.created_at}
        """)
        await asyncio.sleep(5)
        await message.delete()
    if msg.startswith(f"{current_prefix}serverinfo") or msg.startswith(f"{current_prefix}serverinfp"):
        guild = message.guild
        if guild is None:
            await message.edit(content="Cette commande doit être utilisée dans un serveur.")
            await asyncio.sleep(5)
            await message.delete()
            return

        name = guild.name
        id = guild.id
        owner = guild.owner
        member_count = guild.member_count
        created_at = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        region = getattr(guild, "region", "N/A")  # region est deprecated dans discord.py récents

        msg_content = (
            f"> **Infos du serveur :**\n"
            f"> **Nom :** {name}\n"
            f"> **ID :** {id}\n"
            f"> **Propriétaire :** {owner}\n"
            f"> **Membres :** {member_count}\n"
            f"> **Créé le :** {created_at}\n"
            f"> **Région :** {region}"
        )

        await message.edit(content=msg_content)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}joinvc"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Merci de fournir l'ID du salon vocal. Exemple : `.joinvc 123456789012345678`")
            await asyncio.sleep(5)
            await message.delete()
            return
        
        voice_channel_id = parts[1]
        try:
            channel = await client.fetch_channel(int(voice_channel_id))
            if not isinstance(channel, discord.VoiceChannel):
                await message.edit(content="L'ID donné ne correspond pas à un salon vocal.")
                await asyncio.sleep(5)
                await message.delete()
                return
            
            await channel.connect()
            await message.edit(content=f"Rejoint le salon vocal : {channel.name}")
            await asyncio.sleep(5)
            await message.delete()
        
        except Exception as e:
            await message.edit(content=f"Erreur : impossible de rejoindre le salon vocal.\n{e}")
            await asyncio.sleep(5)
            await message.delete()
    if msg.startswith(f"{current_prefix}help"):
        help_text = """
# ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__SELFBOT__**

> **FUN** - Commandes Amusantes
> **MOD** - Outils pour gérer efficacement votre serveur.
> **UTILITY** - Commandes pour améliorer vos interactions Discord.
> **INFO** - Commandes pour afficher des informations utiles.
> **STATUS** - Personnalisez votre statut Discord.
> **VOICE** - Commandes pour booster votre activité vocale.
> **SETTINGS** - Personnalisez les paramètres du selfbot.
"""
        await message.edit(content=help_text)
        await asyncio.sleep(5)
        await message.delete()
    if msg.startswith(f"{current_prefix}voice") or msg.startswith(f"{current_prefix}VOICE"):
        help_voice = f"""
# ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__VOICE SETTINGS__**
> `{current_prefix}joinvc [salon_ID]` - Permet de rejoindre un salon vocal par ID
> `{current_prefix}mute/unmute` - Permet de se mute / unmute dans un salon vocal
> `{current_prefix}cam` - Permet d'activer la caméra dans un salon vocal
"""
        await message.edit(content=help_voice)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}mute"):
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.edit(content="Tu doit être dans un salon vocal")
            await asyncio.sleep(5)
            await message.delete()
            return

        ws = client._connection._get_websocket(message.guild.id)

        payload = {
            "op": 4,
            "d": {
                "guild_id": str(message.guild.id),
                "channel_id": str(voice_state.channel.id),
                "self_mute": True,
                "self_deaf": True,
                "self_video": False,
                "self_stream": False
            }
        }

        await ws.send(json.dumps(payload))
        channel_voice = voice_state.channel.id
        await message.edit(content=f"Vous êtes maintenant mute dans le salon <#{channel_voice}>")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}unmute"):
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.edit(content="Tu doit être dans un salon vocal")
            await asyncio.sleep(5)
            await message.delete()
            return

        # Accès WebSocket "interne"
        ws = client._connection._get_websocket(message.guild.id)

        payload = {
            "op": 4,
            "d": {
                "guild_id": str(message.guild.id),
                "channel_id": str(voice_state.channel.id),
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
                "self_stream": False
            }
        }
        channel_voice = voice_state.channel.id
        await ws.send(json.dumps(payload))
        await message.edit(content=f"Vous êtes maintenant demute dans le salon <#{channel_voice}>")
        await asyncio.sleep(5)
        await message.delete()
    if msg.startswith(f"{current_prefix}cam"):
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.edit(content="Tu doit être dans un salon vocal")
            await asyncio.sleep(5)
            await message.delete()
            return

        ws = client._connection._get_websocket(message.guild.id)

        payload = {
            "op": 4,
            "d": {
                "guild_id": str(message.guild.id),
                "channel_id": str(voice_state.channel.id),
                "self_mute": False,
                "self_deaf": False,
                "self_video": True,
                "self_stream": True
            }
        }

        await ws.send(json.dumps(payload))
        channel_voice = voice_state.channel.id
        await message.edit(content=f"Vous avez maintenant la caméra activer dans le salon <#{channel_voice}>")
        await asyncio.sleep(5)
        await message.delete()
    if msg.startswith(f"{current_prefix}fun") or msg.startswith(f"{current_prefix}FUN"):
        help_fun = """
# ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__FUN COMMANDS__**
> `{current_prefix}gay [user]` - Permet de définir à combien de pourcent une personne est gay
> `{current_prefix}casino` - Permet de lancer une machine de casino
"""
        await message.edit(content=help_fun)
        await asyncio.sleep(5)
        await message.delete()
    if message.content.startswith(f"{current_prefix}gay"):
        target = message.mentions[0] if message.mentions else message.author
        rate = random.randint(0, 100)
        bar = "🏳️‍🌈" * (rate // 10) + "⬛" * (10 - rate // 10)
        await message.edit(
            content=f"{target.mention} est gay à **{rate}%** {bar}"
        )

    if msg.startswith(f"{current_prefix}casino"):
        emojis = ["🍒", "🍋", "🍊", "🍇", "💎"]
        result = [random.choice(emojis) for _ in range(3)]
        slot_display = " | ".join(result)
        
        # Petit effet "gagné/perdu"
        if len(set(result)) == 1:
            outcome = "> 🎉 JACKPOT ! Tu as gagné !"
        elif len(set(result)) == 2:
            outcome = "> ✨ Pas mal, 2 identiques !"
        else:
            outcome = "> 💀 Tu as perdu..."

        await message.edit(content=f"> 🎰 {slot_display}\n{outcome}")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}utility") or msg.startswith(f"{current_prefix}UTILITY"):
        help_uti = f"""
# ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__UTILITY__**
> `{current_prefix}pp [user]` - Permet de pic la pfp de la personne choisi
> `{current_prefix}servericon` - Permet de pic la pfp du serveur
"""
        await message.edit(content=help_uti)
        await asyncio.sleep(5)
        await message.delete()
    if msg.startswith(f"{current_prefix}pp"):
        # On prend la première mention, sinon l'auteur
        user = message.mentions[0] if message.mentions else message.author

        avatar_url = user.avatar_url  # display_avatar gère les avatars animés

        await message.edit(content=f"> Voici la photo de profil de **[{user.name}]({avatar_url})**")
        await asyncio.sleep(5)
        await message.delete()
    if msg.startswith(f"{current_prefix}servericon"):
        guild = message.guild
        if guild is None:
            await message.edit(content="Cette commande doit être utilisée dans un serveur.")
            await asyncio.sleep(5)
            await message.delete()
            return

        if not guild.icon:
            await message.edit(content="Ce serveur n'a pas d'icône.")
            await asyncio.sleep(5)
            await message.delete()
            return

    # Récupération du hash de l'icône
        icon_hash = guild.icon

    # Construction du lien (png par défaut)
        icon_url = f"https://cdn.discordapp.com/icons/{guild.id}/{icon_hash}.png"

    # Pour vérifier si c'est un gif (animé), le hash commence par "a_"
        if str(icon_hash).startswith("a_"):
            icon_url = f"https://cdn.discordapp.com/icons/{guild.id}/{icon_hash}.gif"

        await message.edit(content=f"> Voici l'icone du serveur **[{guild.name}]({icon_url})**")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}status") or msg.startswith(f"{current_prefix}STATUS"):
        help_status = f"""
# ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__STATUS__**
> `{current_prefix}set_activity [playing, watching, listening, streaming] [text] [lien](onlystreaming)` - Modifie l'activité afficher sur votre profile
"""
        await message.edit(content=help_status)
        await asyncio.sleep(5)
        await message.delete()


    if msg.startswith(f"{current_prefix}set_status"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Usage: `.set_status [online|idle|dnd|invisible]`")
            await asyncio.sleep(5)
            await message.delete()
            return

        status_str = parts[1].lower()   
        valid_status = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible
        }

        if status_str not in valid_status:
            await message.edit(content="Statut invalide. Choisis parmi: online, idle, dnd, invisible.")
            await asyncio.sleep(5)
            await message.delete()
            return

        await client.change_presence(status=valid_status[status_str])
        await message.edit(content=f"Statut changé en `{status_str}`")

    if msg.startswith(f"{current_prefix}set_activity"):
        parts = msg.split(maxsplit=3)
        if len(parts) < 3:
            await message.edit(content="Usage: `.set_activity [playing|watching|listening|streaming] [texte] [url si streaming]`")
            await asyncio.sleep(5)
            await message.delete()
            return

        activity_type = parts[1].lower()
        activity = None  # Définit la variable ici pour éviter l'erreur

        if activity_type == "streaming":
            if len(parts) < 4:
                await message.edit(content="Pour le streaming, mets un nom ET une url. Exemple : `.set_activity streaming MonStream https://twitch.tv/moncompte`")
                await asyncio.sleep(5)
                await message.delete()
                return
            stream_name = parts[2]
            stream_url = parts[3]
            if not (stream_url.startswith("http://") or stream_url.startswith("https://")):
                await message.edit(content="URL invalide. Doit commencer par http:// ou https://")
                await asyncio.sleep(5)
                await message.delete()
                return
            activity = discord.Streaming(name=stream_name, url=stream_url)

        else:
            activity_text = " ".join(parts[2:])

            if activity_type == "playing":
                activity = discord.Game(name=activity_text)
            elif activity_type == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=activity_text)
            elif activity_type == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=activity_text)
            else:
                await message.edit(content="Type d'activité invalide. Choisis parmi: playing, watching, listening, streaming.")
                await asyncio.sleep(5)
                await message.delete()
                return

    # On vérifie que l'activité a bien été définie
        if activity:
            await client.change_presence(activity=activity)
            await message.edit(content=f"Activité changée : **{activity_type}**")
            await asyncio.sleep(5)
            await message.delete()
        else:
            await message.edit(content="Une erreur est survenue lors de la création de l'activité.")
            await asyncio.sleep(5)
            await message.delete()
            
    if msg.startswith(f"{current_prefix}setprefix"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Usage : `.setprefix [nouveau préfixe]`")
            await asyncio.sleep(5)
            await message.delete()
            return

        new_prefix = parts[1]
        current_prefix = new_prefix
        update_env_prefix(new_prefix)

        await message.edit(content=f"Préfixe changé en `{current_prefix}`")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}settings") or msg.startswith(f"{current_prefix}SETTINGS"):
         help_settings = f"""
# ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__VOICE SETTINGS__**
> `{current_prefix}setprefix [new_prefix]` - Permet de changer le prefix du SelfBot
> `{current_prefix}set_lang` - Permet de changer la langue du SelfBot (IN DEV)
"""
         await message.edit(content=help_settings)
         await asyncio.sleep(5)
         await message.delete()


async def handle_message_en(message, prefix):
    msg = message.content
    global current_prefix

    if msg == f"{current_prefix}ping":
        api_latency = round(client.latency * 1000)

        # Measure latency VPS -> Discord
        start = time.perf_counter()
        async with message.channel.typing():
            pass
        end = time.perf_counter()
        vps_latency = round((end - start) * 1000)

        await message.edit(content=(
            f"> **Discord API** : {api_latency}ms\n"
            f"> **VPS** : {vps_latency}ms"
        ))
        await asyncio.sleep(5)
        await message.delete()
        await asyncio.sleep(10)
        await message.delete()

    if msg.startswith(f"{current_prefix}userinfo"):
        if len(message.mentions) > 0:
            user = message.mentions[0]  # first mentioned user
        else:
            user = message.author  # if no mention, use message author

        await message.edit(content=f"""
            > **Name:** {user.name}
            > **ID:** {user.id}
            > **Account creation date:** {user.created_at}
        """)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}serverinfo") or msg.startswith(f"{current_prefix}serverinfp"):
        guild = message.guild
        if guild is None:
            await message.edit(content="This command must be used in a server.")
            await asyncio.sleep(5)
            await message.delete()
            return

        name = guild.name
        id = guild.id
        owner = guild.owner
        member_count = guild.member_count
        created_at = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
        region = getattr(guild, "region", "N/A")  # region is deprecated in recent discord.py versions

        msg_content = (
            f"> **Server info:**\n"
            f"> **Name:** {name}\n"
            f"> **ID:** {id}\n"
            f"> **Owner:** {owner}\n"
            f"> **Members:** {member_count}\n"
            f"> **Created on:** {created_at}\n"
            f"> **Region:** {region}"
        )

        await message.edit(content=msg_content)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}joinvc"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Please provide the voice channel ID. Example: `.joinvc 123456789012345678`")
            await asyncio.sleep(5)
            await message.delete()
            return

        voice_channel_id = parts[1]
        try:
            channel = await client.fetch_channel(int(voice_channel_id))
            if not isinstance(channel, discord.VoiceChannel):
                await message.edit(content="The given ID does not correspond to a voice channel.")
                await asyncio.sleep(5)
                await message.delete()
                return

            await channel.connect()
            await message.edit(content=f"Joined the voice channel: {channel.name}")
            await asyncio.sleep(5)
            await message.delete()

        except Exception as e:
            await message.edit(content=f"Error: unable to join the voice channel.\n{e}")
            await asyncio.sleep(5)
            await message.delete()

    if msg.startswith(f"{current_prefix}help"):
        help_text = """
    # ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__SELFBOT__**

    > **FUN** - Fun commands
    > **MOD** - Tools to efficiently manage your server.
    > **UTILITY** - Commands to improve your Discord interactions.
    > **INFO** - Commands to display useful information.
    > **STATUS** - Customize your Discord status.
    > **VOICE** - Commands to boost your voice activity.
    > **SETTINGS** - Customize selfbot settings.
    """
        await message.edit(content=help_text)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}voice") or msg.startswith(f"{current_prefix}VOICE"):
        help_voice = f"""
    # ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__VOICE SETTINGS__**
    > `{current_prefix}joinvc [channel_ID]` - Join a voice channel by ID
    > `{current_prefix}mute/unmute` - Mute / unmute yourself in a voice channel
    > `{current_prefix}cam` - Enable camera in a voice channel
    """
        await message.edit(content=help_voice)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}mute"):
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.edit(content="You must be in a voice channel")
            await asyncio.sleep(5)
            await message.delete()
            return

        ws = client._connection._get_websocket(message.guild.id)

        payload = {
            "op": 4,
            "d": {
                "guild_id": str(message.guild.id),
                "channel_id": str(voice_state.channel.id),
                "self_mute": True,
                "self_deaf": True,
                "self_video": False,
                "self_stream": False
            }
        }

        await ws.send(json.dumps(payload))
        channel_voice = voice_state.channel.id
        await message.edit(content=f"You are now muted in the channel <#{channel_voice}>")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}unmute"):
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.edit(content="You must be in a voice channel")
            await asyncio.sleep(5)
            await message.delete()
            return

        ws = client._connection._get_websocket(message.guild.id)

        payload = {
            "op": 4,
            "d": {
                "guild_id": str(message.guild.id),
                "channel_id": str(voice_state.channel.id),
                "self_mute": False,
                "self_deaf": False,
                "self_video": False,
                "self_stream": False
            }
        }
        channel_voice = voice_state.channel.id
        await ws.send(json.dumps(payload))
        await message.edit(content=f"You are now unmuted in the channel <#{channel_voice}>")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}cam"):
        voice_state = message.author.voice
        if not voice_state or not voice_state.channel:
            await message.edit(content="You must be in a voice channel")
            await asyncio.sleep(5)
            await message.delete()
            return

        ws = client._connection._get_websocket(message.guild.id)

        payload = {
            "op": 4,
            "d": {
                "guild_id": str(message.guild.id),
                "channel_id": str(voice_state.channel.id),
                "self_mute": False,
                "self_deaf": False,
                "self_video": True,
                "self_stream": True
            }
        }

        await ws.send(json.dumps(payload))
        channel_voice = voice_state.channel.id
        await message.edit(content=f"Your camera is now enabled in the channel <#{channel_voice}>")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}fun") or msg.startswith(f"{current_prefix}FUN"):
        help_fun = f"""
    # ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__FUN COMMANDS__**
    > `{current_prefix}gay [user]` - Shows how gay a person is in percentage
    > `{current_prefix}casino` - Play a slot machine game
    """
        await message.edit(content=help_fun)
        await asyncio.sleep(5)
        await message.delete()

    if message.content.startswith(f"{current_prefix}gay"):
        target = message.mentions[0] if message.mentions else message.author
        rate = random.randint(0, 100)
        bar = "🏳️‍🌈" * (rate // 10) + "⬛" * (10 - rate // 10)
        await message.edit(
            content=f"{target.mention} is gay at **{rate}%** {bar}"
        )

    if msg.startswith(f"{current_prefix}casino"):
        emojis = ["🍒", "🍋", "🍊", "🍇", "💎"]
        result = [random.choice(emojis) for _ in range(3)]
        slot_display = " | ".join(result)

        # Small effect "won/lost"
        if len(set(result)) == 1:
            outcome = "> 🎉 JACKPOT! You won!"
        elif len(set(result)) == 2:
            outcome = "> ✨ Not bad, 2 identical!"
        else:
            outcome = "> 💀 You lost..."

        await message.edit(content=f"> 🎰 {slot_display}\n{outcome}")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}utility") or msg.startswith(f"{current_prefix}UTILITY"):
        help_uti = f"""
    # ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__UTILITY__**
    > `{current_prefix}pp [user]` - Show the profile picture of the chosen user
    > `{current_prefix}servericon` - Show the server's icon
    """
        await message.edit(content=help_uti)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}pp"):
        # Take first mention, else author
        user = message.mentions[0] if message.mentions else message.author

        avatar_url = user.avatar_url  # display_avatar handles animated avatars

        await message.edit(content=f"> Here is the profile picture of **[{user.name}]({avatar_url})**")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}servericon"):
        guild = message.guild
        if guild is None:
            await message.edit(content="This command must be used in a server.")
            await asyncio.sleep(5)
            await message.delete()
            return

        if not guild.icon:
            await message.edit(content="This server has no icon.")
            await asyncio.sleep(5)
            await message.delete()
            return

        # Retrieve the icon hash
        icon_hash = guild.icon

        # Construct the URL (png by default)
        icon_url = f"https://cdn.discordapp.com/icons/{guild.id}/{icon_hash}.png"

        # Check if gif (animated), the hash starts with "a_"
        if str(icon_hash).startswith("a_"):
            icon_url = f"https://cdn.discordapp.com/icons/{guild.id}/{icon_hash}.gif"

        await message.edit(content=f"> Here is the server icon **[{guild.name}]({icon_url})**")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}status") or msg.startswith(f"{current_prefix}STATUS"):
        help_status = f"""
    # ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__STATUS__**
    > `{current_prefix}set_activity [playing, watching, listening, streaming] [text] [link](onlystreaming)` - Change the activity shown on your profile
    """
        await message.edit(content=help_status)
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}set_status"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Usage: `.set_status [online|idle|dnd|invisible]`")
            await asyncio.sleep(5)
            await message.delete()
            return

        status_str = parts[1].lower()
        valid_status = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible
        }

        if status_str not in valid_status:
            await message.edit(content="Invalid status. Choose from: online, idle, dnd, invisible.")
            await asyncio.sleep(5)
            await message.delete()
            return

        await client.change_presence(status=valid_status[status_str])
        await message.edit(content=f"Status changed to `{status_str}`")

    if msg.startswith(f"{current_prefix}set_activity"):
        parts = msg.split(maxsplit=3)
        if len(parts) < 3:
            await message.edit(content="Usage: `.set_activity [playing|watching|listening|streaming] [text] [url if streaming]`")
            await asyncio.sleep(5)
            await message.delete()
            return

        activity_type = parts[1].lower()
        activity = None  # Define variable here to avoid errors

        if activity_type == "streaming":
            if len(parts) < 4:
                await message.edit(content="For streaming, provide a name AND a url. Example: `.set_activity streaming MyStream https://twitch.tv/myaccount`")
                await asyncio.sleep(5)
                await message.delete()
                return
            stream_name = parts[2]
            stream_url = parts[3]
            if not (stream_url.startswith("http://") or stream_url.startswith("https://")):
                await message.edit(content="Invalid URL. Must start with http:// or https://")
                await asyncio.sleep(5)
                await message.delete()
                return
            activity = discord.Streaming(name=stream_name, url=stream_url)

        else:
            activity_text = " ".join(parts[2:])

            if activity_type == "playing":
                activity = discord.Game(name=activity_text)
            elif activity_type == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=activity_text)
            elif activity_type == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=activity_text)
            else:
                await message.edit(content="Invalid activity type. Choose from: playing, watching, listening, streaming.")
                await asyncio.sleep(5)
                await message.delete()
                return

        # Check if activity was properly created
        if activity:
            await client.change_presence(activity=activity)
            await message.edit(content=f"Activity changed: **{activity_type}**")
            await asyncio.sleep(5)
            await message.delete()
        else:
            await message.edit(content="An error occurred while creating the activity.")
            await asyncio.sleep(5)
            await message.delete()

    if msg.startswith(f"{current_prefix}setprefix"):
        parts = msg.split()
        if len(parts) < 2:
            await message.edit(content="Usage: `.setprefix [new prefix]`")
            await asyncio.sleep(5)
            await message.delete()
            return

        new_prefix = parts[1]
        current_prefix = new_prefix
        update_env_prefix(new_prefix)

        await message.edit(content=f"Prefix changed to `{current_prefix}`")
        await asyncio.sleep(5)
        await message.delete()

    if msg.startswith(f"{current_prefix}settings") or msg.startswith(f"{current_prefix}SETTINGS"):
        help_settings = f"""
    # ‎‎‎‎‎‎‎‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎**__VOICE SETTINGS__**
    > `{current_prefix}setprefix [new_prefix]` - Change the prefix of the SelfBot
    > `{current_prefix}set_lang` - Change the SelfBot language (IN DEV)
    """
        await message.edit(content=help_settings)
        await asyncio.sleep(5)
        await message.delete()


# Lancement du client Discord
client.run(TOKEN, bot=False)
