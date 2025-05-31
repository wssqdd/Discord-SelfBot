import discord
import os
import time
from dotenv import load_dotenv
import asyncio
import datetime
from flask import Flask
from threading import Thread
import json
import random
import requests
import re
import aiohttp
import datetime

start_time = datetime.datetime.now()

intents = discord.Intents.all()

load_dotenv(dotenv_path="C:/Github/.env")
TOKEN = os.getenv("TOKEN")
current_prefix = os.getenv("PREFIX", ".")

client = discord.Client(intents=intents)

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
async def on_ready():
    print(f"✅ Connecté en tant que {client.user} (ID: {client.user.id})")
    print("🔧 Selfbot prêt à recevoir des commandes.")


@client.event
async def on_message(message):
    global current_prefix
    if message.author.id == client.user.id:
        msg = message.content

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
            parts = msg.split(maxsplit=4)
            if len(parts) < 3:
                await message.edit(content="Usage: `.set_activity [playing|watching|listening|streaming] [texte] [url si streaming] [image_url (optionnel)]`")
                await asyncio.sleep(5)
                await message.delete()
                return

            activity_type = parts[1].lower()
            activity = None
            image_url = None

            # Si une image est fournie
            if len(parts) == 5:
                image_url = parts[4]

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
                activity_text = parts[2] if len(parts) == 3 else parts[2]

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

            # Log Webhook
            try:
                with open("logs_webhook.txt", "r") as f:
                    urls = f.read().splitlines()
                    if not urls:
                        print("Aucun webhook trouvé dans logs_webhook.txt — Pense à lancer la commande .set_logs")
                        return
                    webhook_stream_url = urls[1]
            except FileNotFoundError:
                print("Fichier logs_webhook.txt introuvable — Pense à lancer la commande .set_logs")
                return

            embed = discord.Embed(
                title="Changement d'activité détecté",
                color=0xFFFFFF
            )

            if activity_type == "streaming":
                embed.add_field(name=" ", value=f"""
                > **Type d'activité:** `Streaming`
                > **Texte:** {stream_name}
                > **Lien:** {stream_url}
                """)
            else:
                embed.add_field(name=" ", value=f"""
                > **Type d'activité:** `{activity_type}`
                > **Texte:** {activity_text}
                """)

            if image_url:
                embed.set_thumbnail(url=image_url)

            now = datetime.datetime.now()
            formatted_time = now.strftime("%d/%m %H:%M")
            footer_icon = "https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png"
            footer_text = f"{client.user} | {formatted_time}"
            embed.set_footer(text=footer_text, icon_url=footer_icon)

            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(webhook_stream_url, adapter=discord.AsyncWebhookAdapter(session))
                await webhook.send(embed=embed, username="SelfLogs Activity", avatar_url=footer_icon)

            # Change l'activité
            if activity:
                await client.change_presence(activity=None)
                await client.change_presence(activity=activity)
                await message.edit(content=f"✅ Activité changée : **{activity_type}**")
            else:
                await message.edit(content="❌ Une erreur est survenue lors de la création de l'activité.")

            await asyncio.sleep(5)
            await message.delete()


        # Commande pour changer le préfixe
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
    > `{current_prefix}set_logs` - Active les logs (join, leave, nitro)
    """
            await message.edit(content=help_settings)
            await asyncio.sleep(5)
            await message.delete()

        if msg.startswith(f"{current_prefix}set_logs"):

            # Vérifie si la commande est utilisée dans un serveur
            if message.guild is None:
                await message.edit(content="Cette commande ne peut être utilisée qu’en serveur.")
                await asyncio.sleep(5)
                await message.delete()
                return

            guild = message.guild

            # Vérifie si l'auteur a la permission administrateur
            if not message.author.guild_permissions.administrator:
                await message.edit(content="Tu dois être administrateur pour utiliser cette commande.")
                await asyncio.sleep(5)
                await message.delete()
                return

            # Crée deux salons texte
            cat = await guild.create_category("SelfBot Logs")
            log_channel_1 = await guild.create_text_channel("🔒・join-server", category=cat)
            log_channel_2 = await guild.create_text_channel("🗽・activity", category=cat)
            log_channel_3 = await guild.create_text_channel("🔒・leave-server", category=cat)

            # Crée un webhook dans le premier salon
            webhook = await log_channel_1.create_webhook(name="join-server")
            webhook2 = await log_channel_2.create_webhook(name="nitro")
            webhook3 = await log_channel_3.create_webhook(name="leaveserver")

            # Sauvegarde l'URL dans un fichier
            with open("logs_webhook.txt", "w") as f:
                f.write(f"{webhook.url}\n")
                f.write(f"{webhook2.url}\n")
                f.write(f"{webhook3.url}\n")

            await message.edit(content=f"Logs inititialisé dans {cat}")
            await asyncio.sleep(5)
            await message.delete()


@client.event
async def on_guild_join(guild):
    print(f"on_guild_join triggered for guild: {guild.name}")

    # Lire les webhooks
    try:
        with open("logs_webhook.txt", "r") as f:
            urls = f.read().splitlines()
            if not urls:
                print("Aucun webhook trouvé dans logs_webhook.txt — Pense à lancer la commande .set_logs")
                return
            webhook_join_url = urls[0]
    except FileNotFoundError:
        print("Fichier logs_webhook.txt introuvable — Pense à lancer la commande .set_logs")
        return

    # Trouver un channel avec les permissions nécessaires
    channel = None
    for ch in guild.text_channels:
        perms = ch.permissions_for(guild.me)
        if perms.create_instant_invite and perms.send_messages:
            channel = ch
            print(f"Channel sélectionné pour l'invitation : {ch.name}")
            break

    invite_url = None
    if channel:
        try:
            invite = await channel.create_invite(max_age=3600, max_uses=1)
            invite_url = invite.url
        except Exception as e:
            print(f"Erreur en créant l'invitation : {e}")

    description = f"**Lien du serveur:** {invite_url}" if invite_url else "**Lien du serveur:** (impossible de créer une invitation)"

    embed = discord.Embed(
        title="📥 Nouveau serveur ajouté",
        description=description,
        color=0xFFFFFF
    )
    now = datetime.datetime.now()
    formatted_time = now.strftime("%d/%m %H:%M")  # Jour/Mois Heure:Minutes

    embed.add_field(
        name="Informations du serveur",
        value=f"""
            > **Nom du serveur:** `{guild.name}`
            > **ID du serveur:** `{guild.id}`
            > **Propriétaire:** `{guild.owner} ({guild.owner_id})`
            > **Membres:** `{guild.member_count}`
        """, inline=False)
    footer_icon ="https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png?ex=683c1904&is=683ac784&hm=281fbafa4dbbd7c7f88e84b8b70acdec2313990479020fa13e892a42873abb06&=&format=webp&quality=lossless"
    footer_text = f"{client.user} | {formatted_time}"
    embed.set_footer(text=footer_text, icon_url=footer_icon)



    # Envoi via webhook
    try:
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(webhook_join_url, adapter=discord.AsyncWebhookAdapter(session))
            await webhook.send(embed=embed, username="SelfLogs Join", avatar_url="https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png?ex=683c1904&is=683ac784&hm=281fbafa4dbbd7c7f88e84b8b70acdec2313990479020fa13e892a42873abb06&=&format=webp&quality=lossless")
        print("Message envoyé via webhook.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du webhook : {e}")

@client.event
async def on_guild_remove(guild):
    print(f"on_guild_remove triggered for guild: {guild.name}")

    # Lire les webhooks
    try:
        with open("logs_webhook.txt", "r") as f:
            urls = f.read().splitlines()
            if not urls:
                print("Aucun webhook trouvé dans logs_webhook.txt — Pense à lancer la commande .set_logs")
                return
            webhook_leave_url = urls[2]  # 3e webhook (index 2) pour leave-server
    except FileNotFoundError:
        print("Fichier logs_webhook.txt introuvable — Pense à lancer la commande .set_logs")
        return

    embed = discord.Embed(
        title="📤 Serveur quitté",
        color=0xFFFFFF
    )
    now = datetime.datetime.now()
    formatted_time = now.strftime("%d/%m %H:%M")  # Jour/Mois Heure:Minutes

    embed.add_field(
        name="Informations du serveur",
        value=f"""
            > **Nom du serveur:** `{guild.name}`
            > **ID du serveur:** `{guild.id}`
            > **Propriétaire:** `{guild.owner} ({guild.owner_id})`
            > **Membres:** `{guild.member_count}`
        """, inline=False)
    footer_icon ="https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png?ex=683c1904&is=683ac784&hm=281fbafa4dbbd7c7f88e84b8b70acdec2313990479020fa13e892a42873abb06&=&format=webp&quality=lossless"
    footer_text = f"{client.user} | {formatted_time}"
    embed.set_footer(text=footer_text, icon_url=footer_icon)

    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_leave_url, adapter=discord.AsyncWebhookAdapter(session))
        await webhook.send(embed=embed, username="SelfLogs Leave", avatar_url="https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png?ex=683c1904&is=683ac784&hm=281fbafa4dbbd7c7f88e84b8b70acdec2313990479020fa13e892a42873abb06&=&format=webp&quality=lossless")



@client.event
async def on_presence_update(before, after):
    print(f"Changement de statut détecté : {after.user.name}#{after.user.discriminator} est passé de {before.status} à {after.status}")
    try:
        with open("logs_webhook.txt", "r") as f:
            urls = f.read().splitlines()
            if not urls:
                print("Aucun webhook trouvé dans logs_webhook.txt — Pense à lancer la commande .set_logs")
                return
            webhook_leave_url = urls[1]  # 3e webhook (index 2) pour leave-server
    except FileNotFoundError:
        print("Fichier logs_webhook.txt introuvable — Pense à lancer la commande .set_logs")
        return

    embed=discord.Embed(
        title="Changements de Statut Détécter",
        color=0xFFFFFF
    )
    embed.add_field(name=" ", value=f"""
    > **Ancien statut:** {before.status}
    > **Nouveau statut:** {after.status}
    """)
    now = datetime.datetime.now()
    formatted_time = now.strftime("%d/%m %H:%M")  # Jour/Mois Heure:Minutes
    footer_icon ="https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png?ex=683c1904&is=683ac784&hm=281fbafa4dbbd7c7f88e84b8b70acdec2313990479020fa13e892a42873abb06&=&format=webp&quality=lossless"
    footer_text = f"{client.user} | {formatted_time}"
    embed.set_footer(text=footer_text, icon_url=footer_icon)
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_leave_url, adapter=discord.AsyncWebhookAdapter(session))
        await webhook.send(embed=embed, username="SelfLogs Statut", avatar_url="https://media.discordapp.net/attachments/1378295030363717733/1378299583716790355/images.png?ex=683c1904&is=683ac784&hm=281fbafa4dbbd7c7f88e84b8b70acdec2313990479020fa13e892a42873abb06&=&format=webp&quality=lossless")










# Lancement du serveur keep-alive + bot
client.run(TOKEN, bot=False)
