import os
import random
import discord
import json
import requests
import pdb # pdb.set_trace()
import pymongo
import wikipedia
import time
import youtube_dl
import validators
import urllib.request
import shutil
import praw
import matplotlib.pyplot as plt
import redis
import asyncio
import glob
import subprocess
import i18n

from os import path
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from datetime import date
from discord.ext import commands
from PIL import Image
from io import BytesIO
from gtts import gTTS
from bs4 import BeautifulSoup
from faker import Faker

load_dotenv()
KARMA_COOLDOWN = 30
BAN_TIMEOUT = 10
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')
YOLI_URL = os.getenv('YOLI_URL')
GSE_KEY = os.getenv('GSE_KEY')
GSE_ID = os.getenv('GSE_ID')
GSE_ID_NSFW = os.getenv('GSE_ID_NSFW')
GSE_KEY_NSFW = os.getenv('GSE_KEY_NSFW')
SEARCH_URL = os.getenv('SEARCH_URL')
YOUTUBE_URL = os.getenv('YOUTUBE_URL')
IMDB_URL = os.getenv('IMDB_URL')
IMDB_KEY = os.getenv('IMDB_KEY')
LOL_URL = os.getenv('LOL_URL')
LOL_APIKEY = os.getenv('LOL_APIKEY')
CHAMP_URL = os.getenv('CHAMP_URL')
MONGO_URL = os.getenv('MONGO_URL')
DDRAGON_URL = os.getenv('DDRAGON_URL')
UNTAPPD_URL = os.getenv('UNTAPPD_URL')
UNTAPPD_ID = os.getenv('UNTAPPD_ID')
UNTAPPD_SECRET = os.getenv('UNTAPPD_SECRET')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
ACCESS_DENIED = 'https://media.giphy.com/media/3ohzdYt5HYinIx13ji/giphy.gif'
PIKASEN_URL = os.getenv('PIKASEN_URL')
PIKASEN_CDN = os.getenv('PIKASEN_CDN')
REDIS = os.getenv('REDIS')
REDIS_URL = os.getenv('REDIS_URL')

i18n.load_path.append('./translations')
i18n.set('locale', 'es')

db = MongoClient(MONGO_URL)
exp = db.bot.exp
members = db.bot.members
uncles = db.bot.uncles
inv = db.bot.inv
objetos = db.bot.objetos
actions = db.bot.actions
intros = db.bot.intros
settings = db.bot.settings
wikipedia.set_lang("es")
if REDIS:
    r = redis.Redis(host=REDIS_URL, port=6379, db=0)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=f'{BOT_PREFIX} ', intents=intents)
bot.volume = 0.2

reddit = praw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="ybot"
)

# Cogs loading sequence
bot.load_extension("cogs.role_management")
bot.load_extension("cogs.utilities")
bot.load_extension("cogs.money")
bot.load_extension("cogs.otaku")
bot.load_extension("cogs.info")
bot.load_extension("cogs.recruitment")

queue = []

def manage_karma(id, amount):
    member = members.find_one({'id': id})
    value = 0 + amount
    if member:
        points = int(member['karma']) if 'karma' in member else 0
        new_points = points + amount
        members.update_one({'id': id}, {'$set': {'karma': new_points}})
        value = new_points
    else:
        members.insert_one({'id': id, 'description': '', 'karma': value})
    return value

def last_interaction(author, user):
    last_action = actions.find_one({'author': author, 'user': user})
    if last_action:
        diff = datetime.now() - last_action['updated_at']
        return round(diff.seconds / 60)
    else:
        return 100

def check_queue(voice_client):
    if queue != []:
        sound_effect = queue.pop(0)
        voice_client.play(discord.FFmpegPCMAudio(sound_effect), after=lambda x: check_queue(voice_client))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
        voice_client.source.volume = bot.volume

def youtube_search(query):
    params = {
        'q': query,
        'key': GSE_KEY,
        'part': 'id',
        'type': 'video',
        'order': 'relevance',
        'maxResults': 15
    }

    print(f'Searching: {query}')

    data = requests.get(YOUTUBE_URL, params=params).json()
    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        return f'https://youtu.be/{video_id}'

def check_ban(id):
    if not REDIS:
        return False
    data = r.get(str(id))
    output = True if data else False
    return output

def generate_zalgo(input):
    char_codes = list(map(chr, range(768, 815)))
    random_variation = int(random.normalvariate(10, 5))
    return ''.join(
        [v, v + ''.join(
            random.choice(char_codes) for i in range(random_variation))
        ][v.isalpha()] for v in input
        )

@bot.event
async def on_member_join(member):
    if member.bot == False:
        toque = Image.open('./images/toque.png')
        avatar = member.avatar_url_as(format='png', size=128)
        data = BytesIO(await avatar.read())
        img = Image.open(data)
        img = img.resize((295,271))
        toque.paste(img, (790, 133))
        toque.save("profile.png", 'PNG')
        channel = discord.utils.get(member.guild.channels, name="bienvenida")
        await channel.send(f"Bienvenido, {member.mention}, al mundo de ZFP!")
        await channel.send(file = discord.File("profile.png"))

@bot.event
async def on_ready():
    viendo = [
        i18n.t('base.statuses.a'),
        i18n.t('base.statuses.b'),
        i18n.t('base.statuses.c'),
        i18n.t('base.statuses.d'),
        i18n.t('base.statuses.e'),
        i18n.t('base.statuses.f')
    ]
    actividad = [
        '1',
        '2'
    ]
    escuchar = [
        'Rock pesado lml',
        'Marcianeke',
        'chinos cochinos',
        'openings de animes',
        'como retan a Flipito'
    ]
    elegir = random.choice(actividad)
    if elegir == '1':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(viendo)))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(escuchar)))

@bot.event
async def on_message(message):
    if check_ban(message.author.id):
        return
    msg = message.content.split(' ')

    otaku_commands = ['$waifu', '$wa', '$husbando', '$wg', '$w']
    if (msg[0] in otaku_commands) and message.channel.name == 'general':
        await message.channel.send('Acá no, perkin')
        await message.channel.send('https://i.kym-cdn.com/photos/images/newsfeed/001/214/706/171.png')
        value = manage_karma(message.author.id, -1)
        await message.channel.send(f'{message.author.name} tiene {value} karma')
    if ('++' in msg  or '--' in msg  ) and message.mentions:
        user = message.mentions[0].id
        author = message.author.id
        modifier = 1 if '++' in msg  else - 1
        minutes = last_interaction(author, user)
        if modifier > 0 and user == author:
            await message.channel.send('No seai fresco, -- por pao')
            value = manage_karma(user, -1)
            await message.channel.send(f'{message.mentions[0].name} tiene {value} karma')
        elif minutes < KARMA_COOLDOWN:
            await message.channel.send(f'Inténtalo en {KARMA_COOLDOWN - minutes} minuto(s)')
        else:
            value = manage_karma(user, modifier)
            actions.replace_one({'author': author, 'user': user}, {'author': author, 'user': user, 'updated_at': datetime.now()}, upsert=True)
            await message.channel.send(f'{message.mentions[0].name} tiene {value} puntos de karma')
    else:
        await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if check_ban(member.id):
            return
        if before.channel is None and after.channel is not None and member.bot == False:
            if voice_client and voice_client.channel == after.channel:
                id = member.id
                data = intros.find_one({'id': id})
                if data and data['effect'] != '' and path.exists(f'sound_effects/{data["effect"]}.mp3'):
                    voice_client.play(discord.FFmpegPCMAudio(f'sound_effects/{data["effect"]}.mp3'))
                    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                    voice_client.source.volume = bot.volume
                else:
                    print(f'{member.name} no tiene un sonido registrado')
            else:
                if voice_client is None:
                    roles = [o.name for o in member.roles]
                    if ('ficha' in roles):
                        channel = after.channel
                        await channel.connect()
        if voice_client and voice_client.channel == before.channel:
            connected_users = voice_client.channel.members
            if len(connected_users) == 1 and connected_users[0].bot:
                print('Voice channel empty, leaving...')
                await voice_client.disconnect()
    except Exception as e:
        print(e)

@bot.event
async def on_reaction_add(reaction, member):
    try:
        user = reaction.message.author.id
        author = member.id
        modifier = 1 if reaction.emoji in ['➕', '💯', '⬆️', '😂', '😆', '👍'] else 0
        if modifier != 0 and user != author:
            minutes = last_interaction(author, user)
            if minutes < KARMA_COOLDOWN:
                print(f'On cooldown: {member.name} -> {reaction.message.author.name}')
            else:
                value = manage_karma(user, modifier)
                actions.replace_one({'author': author, 'user': user}, {'author': author, 'user': user, 'updated_at': datetime.now()}, upsert=True)
                print(f'{member.name} reacted on {reaction.message.author.name} ++')
    except Exception as e:
        print(e)

@bot.command(aliases = ['karma', 'ranking'])
async def karma_ranking(ctx):
    sorted_members = list(members.find().sort('karma', pymongo.DESCENDING))
    filtered_members = []
    for member in sorted_members:
        if 'karma' not in member:
            continue

        user = bot.get_user(member['id'])
        if user and not user.bot:
            filtered_members.append({
                'name': user.name,
                'karma': member['karma']
            })
    embed = discord.Embed(color=0xffffff)
    ranking = ''
    medals = {
        0: '🥇',
        1: '🥈',
        2: '🥉'
    }
    medals[len(filtered_members) - 1] = '💩'
    for i in range(len(filtered_members)):
        formatted_counter = medals[i] if i in medals else '🏅'
        formatted_karma = str(int(filtered_members[i]['karma'])).rjust(3)
        ranking = ranking + f'{formatted_counter} {filtered_members[i]["name"]}: {formatted_karma}\n'
    embed.add_field(name='Ranking de karma', value=ranking, inline=False)
    await ctx.send(embed=embed)

@bot.command(name='habla')
async def say(ctx, *, message):
    print(f'{ctx.message.author.name} >> {ctx.message.content}')
    channel = discord.utils.get(ctx.guild.text_channels, name='general')
    await channel.send(message)

@bot.command()
async def putea(ctx, *, name):
    lista = [
        'eri puro wn',
        'tu mamá es el vitoco',
        'puro perro logi ql',
        'deja de dar dislikes tonto wn',
        'maldito sapo conchetumare',
        'chupala meando',
        'prepara las nalgas porque te voy a dejar como bambi',
        'a tu mamá le quedan malas las cazuelas'
    ]
    await ctx.send(f'oe {name.replace("a ", "")} {random.choice(lista)}')

@bot.command(aliases=['hola', 'ola', 'holas', 'olas', 'wenas', 'wena', 'holanda'])
async def greet(ctx):
    greetings = [
        'olas :ocean:',
        'wena wena',
        'kiu majaji',
        'que queri ahora ql',
        f'hola po {ctx.message.author.name}'
    ]
    await ctx.send(random.choice(greetings))

@bot.command()
async def pregunta(ctx):
    answer = [
        'En mi opinión, sí',
        'Es cierto',
        'Es decididamente así',
        'Probablemente',
        'Buen pronóstico',
        'Todo apunta a que sí',
        'Sin duda',
        'Sí',
        'Sí - definitivamente',
        'Debes confiar en ello',
        'Respuesta vaga, vuelve a intentarlo',
        'Pregunta en otro momento',
        'Será mejor que no te lo diga ahora',
        'No puedo predecirlo ahora',
        'Concéntrate y vuelve a preguntar',
        'No cuentes con ello',
        'Mi respuesta es no',
        'Mis fuentes me dicen que no',
        'Las perspectivas no son buenas',
        'Muy dudoso',
        'Yo no volveria a confiar'
    ]
    await ctx.send(random.choice(answer))

@bot.command(name='horoscopo')
async def fortune(ctx, sign):
    req = requests.get(url = YOLI_URL)
    prediction = req.json()['horoscopo']
    response = 'A que wea le está haciendo hermanito, no cacho ese signo'
    if sign in prediction:
        prediction_data = {
            "love": prediction[sign]['amor'],
            "health": prediction[sign]['salud'],
            "money": prediction[sign]['dinero'],
            "number": prediction[sign]['numero'],
            "color": prediction[sign]['color']
        }
        template = '❤️ {love}\n🤒 {health}\n💰 {money}\n🔢 {number}\n🎨 {color}\n'
        response = template.format(**prediction_data)
    await ctx.send(response)

@bot.command()
async def id(ctx):
    await ctx.send(ctx.message.mentions[0].id)

@bot.command(name='tio', aliases=['tia'])
async def uncle(ctx, *, params):
    if ctx.message.author.id == 134688787002425344:
        id = ctx.message.mentions[0].id
        data = uncles.find_one({'id': id})
        value = int(params.split(' ')[-1])
        if data:
            points = int(data['points'])
            new_points = points + value
            uncles.update_one({'id': id}, {'$set': {'points': new_points}})
            value = new_points
        else:
            uncles.insert_one({'id': id, 'points': value, 'name': ctx.message.mentions[0].name})
        await ctx.send(f'{ctx.message.mentions[0].name} tiene {value} puntos')
    else:
        await ctx.send('Este comando sólo está disponible para Martinolix')

@bot.command(name='tios')
async def uncles_ranking(ctx):
    sorted = list(uncles.find().sort('points', pymongo.DESCENDING))
    embed = discord.Embed(color=0xff66cf)
    ranking = ''
    for i in range(len(sorted)):
        ranking = ranking + f'{i+1}) {sorted[i]["name"]}\n'
    embed.add_field(name='Ranking de tíos', value=ranking, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def soy(ctx, *, description):
    id = ctx.message.author.id
    data = members.find_one({'id': id})
    if data:
        name = ctx.message.author.nick or ctx.message.author.name
        members.update_one({'id': id}, {'$set':{"description" : description, 'name': name } })
    else:
        members.insert_one({'id': id, 'description': description, 'karma': 0})

@bot.command()
async def quien(ctx):
    id = ctx.message.mentions[0].id
    data = members.find_one({'id': id})
    name = ctx.message.mentions[0].nick or ctx.message.mentions[0].name
    if data and data['description'] != '':
        await ctx.send(f'{name} es {data["description"]}')
    else:
        await ctx.send(f'No conozco a ese culiao que se hace llamar {name}')

@bot.command(aliases=['fotos', 'foto', 'img'])
async def image(ctx, *, query):
    setting = settings.find_one({'name': 'mode'})
    cx = GSE_ID
    key = GSE_KEY
    safe = 'high'
    if setting and setting['value'] == 'nsfw':
        cx = GSE_ID_NSFW
        key = GSE_KEY_NSFW
        safe = 'off'
    params = {
        'q': query,
        'searchType': 'image',
        'safe': safe,
        'fields': 'items(link)',
        'cx': cx,
        'key': key
    }
    data = requests.get(SEARCH_URL, params=params).json()
    if 'items' in data and len(data['items']) > 0:
        embed = discord.Embed(color=0x00ff2a)
        image_link = random.choice(data['items'])['link']
        print(f'requested image for {query}: {image_link}')
        embed.set_image(url=image_link)
        await ctx.send(embed=embed)
    else:
        await ctx.send('No encontré resultados')

@bot.command(aliases=['jif'])
async def gif(ctx, *, query):
    params = {
        'q': query,
        'searchType': 'image',
        'safe': 'high',
        'fileType': 'gif',
        'hq': 'animated',
        'tbs': 'itp:animated',
        'fields': 'items(link)',
        'cx': GSE_ID,
        'key': GSE_KEY
    }
    data = requests.get(SEARCH_URL, params=params).json()
    if 'items' in data and len(data['items']) > 0:
        embed = discord.Embed(color=0x00fffb)
        embed.set_image(url=data['items'][0]['link'])
        await ctx.send(embed=embed)
    else:
        await ctx.send('No encontré resultados')

@bot.command(aliases=['yt', 'yutu'])
async def youtube(ctx, *, query):
    video_url = youtube_search(query)
    if video_url:
        await ctx.send(video_url)
    else:
        await ctx.send('No encontré resultados')

@bot.command(description='Traduce al idioma de Guru Guru')
async def guru(ctx, *, text):
    output = []
    letters = {
        'a': 'a',
        'b': 'g',
        'c': 'c',
        'd': 'g',
        'e': 'e',
        'f': 'j',
        'g': 'g',
        'h': 'h',
        'i': 'i',
        'j': 'j',
        'k': 'k',
        'l': 'g',
        'm': 'ñ',
        'n': 'gn',
        'ñ': 'ggni',
        'o': 'o',
        'p': 'c',
        'q': 'q',
        'r': 'cggg',
        's': 'j',
        't': 'c',
        'u': 'u',
        'v': 'g',
        'w': 'w',
        'x': 'kj',
        'y': 'y',
        'z': 'j'
    }

    for element in text:
        char = letters[element] if element in letters else element
        output.append(char)

    await ctx.send(''.join(output))

@bot.command(aliases=['peli', 'serie'])
async def imdb(ctx, *, query):
    url = f'{IMDB_URL}{query}'
    args = query.split(',')
    if args[-1].isnumeric():
        url = f'{IMDB_URL}{args[0]}&y={args[-1]}'
    data = requests.get(f'{url}&apikey={IMDB_KEY}').json()
    if data['Response'] == 'True':
        embed = discord.Embed(title=data['Title'], color=0xffea00)
        if data['Poster'] != 'N/A':
            embed.set_thumbnail(url=data['Poster'])
        if data['Ratings']:
            found = next(item for item in data['Ratings'] if item['Source'] == 'Internet Movie Database' or item['Source'] == 'Rotten Tomatoes')
            embed.add_field(name="⭐️", value=found['Value'], inline=False)
        embed.add_field(name="Director", value=data['Director'], inline=False)
        embed.add_field(name="Año", value=data['Year'], inline=False)
        embed.add_field(name="Género", value=data['Genre'], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send('No encontré resultados')

@bot.command()
async def wiki(ctx, *, query):
    try:
        page = wikipedia.page(query)
        embed = discord.Embed(color=0x00ffe1)
        data = page.summary
        info = (data[:1000] + '...') if len(data) > 75 else data
        embed.add_field(name=page.title, value=info, inline=False)
        if page.images:
            embed.set_thumbnail(url=page.images[1])
        embed.add_field(name="Link", value=page.url, inline=False)
        await ctx.send(embed=embed)
    except:
        await ctx.send('No encontré resultados')

@bot.command()
async def play(ctx, *, query):
    id = ctx.message.author.id
    data = members.find_one({'id': id})
    roles = [o.name for o in ctx.message.author.roles]
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if ('💻 dev' in roles) or ('DJ' in roles and data['karma'] > 10):
        if not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        if ctx.author.voice and ctx.voice_client:
            url = query if validators.url(query) else youtube_search(query)
            if url:
                song_there = os.path.isfile("song.mp3")
                try:
                    if song_there:
                        os.remove("song.mp3")
                        print("Removed old song file")
                except PermissionError:
                    print("Trying to delete song file, but it's being played")
                    return

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                try:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print("Downloading audio now\n")
                        ydl.download([url])
                except:
                    print('Error in song download')

                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        name = file
                        print(f"Renamed File: {file}\n")
                        os.rename(file, "song.mp3")

                vc = ctx.voice_client
                if not vc.is_playing():
                    vc.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda x: check_queue(vc))
                    vc.source = discord.PCMVolumeTransformer(vc.source)
                    vc.source.volume = 0.07
                    await ctx.send(f'Reproduciendo {url}')
            else:
                await ctx.send('No encontré resultados')
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command(aliases = ['join'])
async def join_channel(ctx):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    except Exception as e:
        print(e)
        print('Error al conectarse al canal de voz')

@bot.command()
async def leave(ctx):
    try:
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()
    except Exception as e:
        print(e)
        print('Error al desconectarse del canal de voz')

@bot.command()
async def stop(ctx):
    id = ctx.message.author.id
    data = members.find_one({'id': id})
    roles = [o.name for o in ctx.message.author.roles]
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if ('💻 dev' in roles) or ('DJ' in roles and data['karma'] > 10):
        if ctx.author.voice and ctx.voice_client:
            vc = ctx.voice_client
            if vc.is_playing():
                queue = []
                vc.stop()

@bot.command(aliases=['s'])
async def sound(ctx, effect):
    sound_effect = list(glob.glob(f'sound_effects/{effect}*.mp3'))[0]
    print(f'{ctx.message.author} > {sound_effect}')
    try:
        if sound_effect and path.exists(sound_effect):
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            if not voice_client:
                channel = ctx.message.author.voice.channel
                await channel.connect()
            if ctx.author.voice and ctx.voice_client:
                vc = ctx.voice_client
                await ctx.message.delete()
                if not vc.is_playing():
                    print('Empty queue, playing...')
                    vc.play(discord.FFmpegPCMAudio(sound_effect), after=lambda x: check_queue(vc))
                    vc.source = discord.PCMVolumeTransformer(vc.source)
                    vc.source.volume = bot.volume
                else:
                    print(f'Added to queue: {sound_effect}')
                    queue.append(sound_effect)
            else:
                await ctx.send('No estás conectado a un canal de audio')
        else:
            await ctx.send('No tengo ese sonido compare, envía un correo a soporte@ybot.com')
    except Exception as e:
        print(e)
        await ctx.send('Exploté 💣')

@bot.command(name='sonidos')
async def sound_list(ctx):
    files_path = f'{os.getcwd()}/sound_effects'
    files_directory = os.listdir(files_path)

    files = sorted(files_directory)
    page_size = 20

    pages = [files[i: i + page_size] for i in range(0, len(files), page_size)]
    paginated_content = []

    for page in pages:
        embed = discord.Embed()
        sounds_list = '```\n'
        for file in page:
            sounds_list += f'- {file.split(".")[0]}\n'
        sounds_list += '```'
        embed.add_field(name='🔈 Lista de sonidos disponibles', value=sounds_list, inline=False)
        paginated_content.append(embed)

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    current = 0
    msg = await ctx.send(embed=paginated_content[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except Exception as e:
            return print(e)

        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0

            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1

            elif reaction.emoji == u"\u27A1":
                if current < len(paginated_content)-1:
                    current += 1

            elif reaction.emoji == u"\u23E9":
                current = len(paginated_content)-1

            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if current != previous_page:
                await msg.edit(embed=paginated_content[current])

@bot.command()
async def king(ctx):
    frase = [
        'Maricones chupenme la raja con caca',
        'Mysterion lo más grande',
        'Tu conoces el sexo? Tu no conoces el sexo',
        'Mi destino ya esta trazao y se llama éxito',
        'Nunca hay chupao zorra',
        'viska spilli fudbar',
        'vilus spille memey?',
        'obisnake'
    ]
    await ctx.send(random.choice(frase))

@bot.command()
async def intro(ctx):
    roles = [o.name for o in ctx.message.author.roles]
    if '💻 dev' in roles:
        id = ctx.message.mentions[0].id
        effect = ctx.message.content.split(' ')[-1]
        data = intros.find_one({'id': id})
        if data:
            intros.update_one({'id': id}, {'$set':{'effect' : effect}})
        else:
            intros.insert_one({'id': id, 'effect': effect})
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command()
async def lol(ctx, *, usuario):
    f = open('champions.json',"r",encoding='utf-8')
    data = json.load(f)
    req = requests.get(url = f'{LOL_URL}{usuario}{LOL_APIKEY}')
    response = req.json()
    id = response['id']
    nombre = response['name']
    lvl = response['summonerLevel']
    req = requests.get(url = f'{CHAMP_URL}{id}{LOL_APIKEY}')
    champ = req.json()
    campeon = champ[0]['championId']
    mastery_points = champ[0]['championPoints']
    formatted_points = '{0:,}'.format(mastery_points).replace(",", ".")
    found = next(item for item in data if int(item['key']) == campeon)
    id_champ = int(found['key'])
    if id_champ == campeon:
        nombre_champ = found['name']

    embed = discord.Embed(
        colour = discord.Colour.blue()
    )

    embed.set_thumbnail(url=f'{DDRAGON_URL}{nombre_champ}_0.jpg')
    embed.add_field(name=('Nombre'), value=nombre, inline=False)
    embed.add_field(name=('Nivel'), value=lvl, inline=False)
    embed.add_field(name=('Main'), value=nombre_champ, inline=True)
    embed.add_field(name=('Puntos de maestría'), value=formatted_points, inline=True)

    await ctx.send(embed=embed)

@bot.command(name='modo')
async def mode(ctx, name):
    roles = [o.name for o in ctx.message.author.roles]
    if '💻 dev' in roles:
        setting = settings.find_one({'name': 'mode'})
        if setting:
            if name in ['diablo', 'sexo']:
                settings.update_one({'name': 'mode'}, {'$set': {'value': 'nsfw'}})
                await ctx.message.add_reaction('😈')
            else:
                settings.update_one({'name': 'mode'}, {'$set': {'value': 'safe'}})
                await ctx.message.add_reaction('😇')
        else:
            settings.insert_one({'name': 'mode', 'value': 'safe'})
            await ctx.message.add_reaction('😇')
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command()
async def add(ctx):
    roles = [o.name for o in ctx.message.author.roles]
    if '💻 dev' in roles:
        url = ctx.message.attachments[0].url
        print(url)
        filename = url.split('/')[-1]
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, filename)
        shutil.move(filename, 'sounds')
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command(aliases=['pilsen', 'chela', 'xela', 'untappd'])
async def beer(ctx, *, query):
    url = f'{UNTAPPD_URL}search/beer?q={query}&client_secret={UNTAPPD_SECRET}&client_id={UNTAPPD_ID}'
    data = requests.get(url).json()
    if data['response']['beers']['count'] == 0:
        await ctx.send('No encontré resultados')
    else:
        beer = data['response']['beers']['items'][0]['beer']
        bid = beer['bid']
        ibu = beer['beer_ibu'] if beer['beer_ibu'] != 0 else '❓'
        brewery = data['response']['beers']['items'][0]['brewery']
        info_url = f'{UNTAPPD_URL}beer/info/{bid}?client_secret={UNTAPPD_SECRET}&client_id={UNTAPPD_ID}&compact=true'
        info = requests.get(info_url).json()
        rating = round(info['response']['beer']['rating_score'], 2)
        embed = discord.Embed(color=0xffe229)
        if 'brewery_label' in brewery:
            embed.set_thumbnail(url=brewery['brewery_label'])
        embed.add_field(name="Nombre", value=beer['beer_name'], inline=False)
        embed.add_field(name="Cervecería", value=brewery['brewery_name'], inline=False)
        embed.add_field(name="⭐️", value=rating, inline=False)
        embed.add_field(name="País", value=brewery['country_name'], inline=False)
        embed.add_field(name="Graduación alcohólica", value=beer['beer_abv'], inline=False)
        embed.add_field(name="IBU", value=ibu, inline=False)
        embed.add_field(name="Estilo", value=beer['beer_style'], inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def item(ctx):
    subreddit = reddit.subreddit("ItemShop")
    posts = subreddit.hot(limit=50)
    items = []
    for post in posts:
        if post.url.endswith('.jpg'):
            items.append(post)
    if items:
        item = random.choice(items)
        embed=discord.Embed(title=item.title)
        embed.set_image(url=item.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('No encontré resultados')

@bot.command()
async def boss(ctx):
    subreddit = reddit.subreddit("Bossfight")
    posts = subreddit.hot(limit=50)
    items = []
    for post in posts:
        if post.url.endswith('.jpg'):
            items.append(post)
    if items:
        item = random.choice(items)
        embed=discord.Embed(title=item.title)
        embed.set_image(url=item.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send('No encontré resultados')

@bot.command()
async def clase(ctx):
    await ctx.send('Puedes elegir tu clase con el comando "y elegir".\n1. Guerrero\n2. Arquero\n3. Huaso')

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def monedas(ctx):
    id = ctx.message.author.id
    data = inv.find_one({'id':id})
    moneda = random.randint(1,3)
    if ctx.message.channel.name == 'farmeo':
        if data:
            if 'monedas' in data:
                nueva_moneda = data['monedas'] + moneda
                inv.update_one({'id':id}, {'$set': {'monedas':nueva_moneda}})
                moneda = nueva_moneda
            else:
                inv.update_one({'id':id}, {'$set': {'monedas':moneda}})
        else:
            inv.insert_one({'id':id, 'monedas':moneda})
        await ctx.send(f'Tienes {moneda} monedas en tu inventario')
    else:
        await ctx.send('No estas en el canal de farmeo. Vira de aqui larva')

@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def robar(ctx):
    ladron = ctx.message.author.id
    vistima = ctx.message.mentions[0].id
    data = inv.find_one({'id':ladron})
    data2 = members.find_one({'id':ladron})
    data3 = inv.find_one({'id':vistima})
    if data2['karma'] < -5:
        await ctx.send(f'Sorry compare, no puedes ocupar este comando porque tienes {data2["karma"]} de karma.')
    else:
        if random.randint(0,100) < 26:
            if random.randint(0,100) == 1:
                monedas = data3['monedas']
                nueva_moneda = monedas - monedas
                inv.update_one({'id':vistima}, {'$set': {'monedas':nueva_moneda}})
                monedas_robadas = monedas + data['monedas']
                inv.update_one({'id':ladron}, {'$set': {'monedas':monedas_robadas}})

                await ctx.send(f'Chaaa hermanito vo eri vio, le robaste todo al otro lokito. Ahora tienes {monedas_robadas} monedas')
            else:
                monedita = data3['monedas']
                money20 = (monedita*20)/100
                money20 = int(money20)
                monea = data3['monedas'] - money20
                inv.update_one({'id':vistima}, {'$set': {'monedas':monea}})
                saldoFinal = data['monedas'] + money20
                inv.update_one({'id':ladron}, {'$set': {'monedas':saldoFinal}})

                await ctx.send(f'Ya choro bomba, pudiste robarle al otro pajaron. Tienes {saldoFinal} monedas')
        else:
            manage_karma(ladron, -1)

            await ctx.send(f'Robar es malo compare, piensa lo que haces. Te quito karma por pao. Tienes {data2["karma"]} karma.')

@bot.command(name='bot')
async def bot_avatar(ctx, *word):
    bot_name = urllib.parse.quote_plus(ctx.message.author.nick)
    if word:
        bot_name = ''.join(word).strip()
    print(f'Creating {bot_name} bot...')
    embed=discord.Embed(title=f'Hola, soy el bot {bot_name} 🤖')
    embed.set_image(url=f'https://robohash.org/{bot_name}.png?size=300x300&set=set1')
    await ctx.send(embed=embed)

@bot.command(name='traduce')
async def translate(ctx, *, query):
    try:
        values = query.split(' ')
        origin = values[0]
        destination = values[1]
        message = ' '.join(values[2:])
        url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl={origin}&tl={destination}&dt=t&q={message}'
        print(url)
        data = requests.get(url).json()
        await ctx.send(f'🌐 {data[0][0][0]}')
    except Exception as e:
        print(e)
        await ctx.send('No cacho ¯\_(ツ)_/¯')

@bot.command()
@commands.cooldown(1, 7200, commands.BucketType.user)
async def rezar(ctx):
    catolico = ctx.message.author.id
    data = members.find_one({'id':catolico})
    if random.randint(0,100) < 6:
        manage_karma(catolico, 1)

        await ctx.send(f'Lo lograste, eres un pan de Dios. Te ilumino con 1 karma. Tienes {data["karma"]} de karma.')
    else:
        await ctx.send('Te falta fe hijo del diaulo, vuelve cuando aprendas a rezar.')

@bot.command()
async def volume(ctx, value):
    try:
        bot.volume = int(value)/100
        await ctx.send(f'El volumen actual es {value}%')
    except Exception as e:
        print(e)
        await ctx.send('')

@bot.command(name='busca')
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    wanted = Image.open("./images/wanted.png")

    user_avatar = user.avatar_url_as(format='png', size=128)
    data = BytesIO(await user_avatar.read())
    avatar = Image.open(data).convert('RGBA')
    avatar = avatar.resize((807, 669))
    wanted.paste(avatar, (219, 521), mask=avatar)
    wanted.save("profile.png", 'PNG')
    await ctx.send(file = discord.File("profile.png"))

@bot.command()
async def drake(ctx, evitado, elegido):
    if evitado and elegido:
        preferencia = Image.open("./images/drake.png")

        evitado_avatar = ctx.message.mentions[0].avatar_url_as(format='png', size=128)
        elegido_avatar = ctx.message.mentions[1].avatar_url_as(format='png', size=128)
        data = BytesIO(await evitado_avatar.read())
        data2 = BytesIO(await elegido_avatar.read())
        evitado = Image.open(data).convert('RGBA')
        elegido = Image.open(data2).convert('RGBA')
        evitado = evitado.resize((225, 200))
        elegido = elegido.resize((225, 190))
        preferencia.paste(evitado, (244, 10), mask=evitado)
        preferencia.paste(elegido, (243, 233), mask=elegido)
        preferencia.save("profile.png", 'PNG')
        await ctx.send(file=discord.File("profile.png"))

@bot.command()
async def rip(ctx):
    tombstone = Image.open('./images/tombstone.png')
    avatar = ctx.message.mentions[0].avatar_url_as(format='png', size=128)
    data = BytesIO(await avatar.read())
    img = Image.open(data).convert('RGBA')
    img_bw = img.copy()
    img_bw = img_bw.convert('L')
    tombstone.paste(img_bw, (180, 320), mask=img)
    tombstone.save("profile.png", 'PNG')
    await ctx.send(file = discord.File("profile.png"))

@bot.command()
async def wolverine(ctx):
    wolverine_base = Image.open('./images/wolverine1.png')
    wolverine_hands = Image.open('./images/wolverine2.png')
    avatar = ctx.message.mentions[0].avatar_url_as(format='png', size=128)
    data = BytesIO(await avatar.read())
    user = Image.open(data).convert('RGBA')
    user = user.resize((300, 400))
    wolverine_base.paste(user, (170, 460), mask=user)
    wolverine_base.paste(wolverine_hands, (0, 434), mask=wolverine_hands)
    wolverine_base.save("profile.png", 'PNG')
    await ctx.send(file = discord.File("profile.png"))

@bot.command()
async def tts(ctx, *, msg):
    id = ctx.message.author.id
    data = members.find_one({'id': id})
    roles = [o.name for o in ctx.message.author.roles]
    message = msg.split('/')
    text_to_speech = message[0]
    language = message[1] if len(message) > 1 else 'es'
    if ('💻 dev' in roles) or data['karma'] > 10:
        tts = gTTS(text=text_to_speech, lang=language)
        tts.save("tts.mp3")
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        vc = ctx.voice_client
        vc.play(discord.FFmpegPCMAudio('tts.mp3'), after=lambda x: check_queue(vc))
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = bot.volume
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command(name='chiste')
async def joke(ctx):
    id = ctx.message.author.id
    data = members.find_one({'id': id})
    roles = [o.name for o in ctx.message.author.roles]
    if ('💻 dev' in roles) or data['karma'] > 20:
        url = 'http://www.chistes.com/chistealazar.asp?n=4'
        data = urllib.request.urlopen(url)
        soup = BeautifulSoup(data, 'html.parser')
        divs = soup.findAll('div', {'class': 'chiste'})
        tts = gTTS(text=divs[0].text, lang='es')
        tts.save("tts.mp3")
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            channel = ctx.message.author.voice.channel
            await channel.connect()
        vc = ctx.voice_client
        vc.play(discord.FFmpegPCMAudio('tts.mp3'), after=lambda x: check_queue(vc))
        queue.append('sound_effects/drums.mp3')
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = bot.volume
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command()
async def shuffle(ctx, *, msg):
    ordered = msg.split(',')
    random.shuffle(ordered)

    await ctx.send(','.join(ordered))

@bot.command()
async def forbes(ctx):
    money_list = list(inv.find())
    money_users = []
    for member in money_list:
        if 'monedas' not in member:
            continue

        user = bot.get_user(member['id'])
        if user and not user.bot:
            money_users.append({
                'name': user.name,
                'coins': member['monedas']
            })
    names = [x['name'] for x in money_users]
    coins = [x['coins'] for x in money_users]

    size = len(money_users)
    plt.bar(range(size), coins, edgecolor='black')

    plt.xticks(range(size), names, rotation=60)
    plt.title("Distribución de dinero en ZFP Gaming")
    plt.ylim(min(coins) - 1, max(coins) + 1)
    plt.tight_layout()
    plt.savefig("coins_graph.png")
    await ctx.send(file = discord.File("coins_graph.png"))

@bot.command()
async def update_record(ctx, *, options):
    if ctx.message.author.guild_permissions.administrator:
        args = options.split(' ')
        user_id = int(args[0])
        operation = args[1]
        amount = int(args[2])
        if operation == 'karma':
            member = members.find_one({'id': user_id})
            if member:
                members.update_one({'id': user_id}, {'$set': {'karma': amount}})
            else:
                members.insert_one({'id': user_id, 'description': '', 'karma': amount})
        else:
            member = inv.find_one({'id': user_id})
            if member:
                inv.update_one({'id': user_id}, {'$set': {'monedas': amount}})
            else:
                inv.insert_one({'id': user_id, 'monedas': amount})
    else:
        await ctx.send('🤖 Actualizado')

@bot.command()
async def pikasen(ctx, *, query):
    try:
        await ctx.message.add_reaction('😏')
        url = f'{PIKASEN_URL}{query.replace(" ", "_")}'
        req = requests.get(url = url)
        response = req.json()
        if response:
            item = random.choice(response)
            await ctx.author.send(f'{PIKASEN_CDN}/{item["directory"]}/{item["image"]}')
        else:
            await ctx.author.send('No encontré nada (por suerte 😰)')
    except Exception as e:
        print(e)
        await ctx.author.send('No encontré nada (por suerte 😰)')

@bot.command()
async def seba(ctx, effect):
    sound_effect = f'sound_effects/{effect}.mp3'
    try:
        if ctx.message.author.id == 121417708469223428:
            if path.exists(sound_effect):
                voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                if not voice_client:
                    channel = ctx.message.author.voice.channel
                    await channel.connect()
                if ctx.author.voice and ctx.voice_client:
                    vc = ctx.voice_client
                    if not vc.is_playing():
                        print('Empty queue, playing...')
                        for i in range(9):
                            queue.append(sound_effect)
                        vc.play(discord.FFmpegPCMAudio(sound_effect), after=lambda x: check_queue(vc))
                        vc.source = discord.PCMVolumeTransformer(vc.source)
                        vc.source.volume = bot.volume
                    else:
                        print(f'Added to queue: {sound_effect}')
                        for i in range(10):
                            queue.append(sound_effect)
                else:
                    await ctx.send('No estás conectado a un canal de audio')
            else:
                await ctx.send('No tengo ese sonido compare, envía un correo a soporte@ybot.com')
        else:
            reactions = [
                'https://media.giphy.com/media/3oFzmko6SiknmpR2NO/giphy.gif',
                'https://media.giphy.com/media/mcH0upG1TeEak/giphy.gif',
                'https://media.giphy.com/media/lTYXWBnuA4oFA5R3dp/giphy.gif',
                'https://media.giphy.com/media/3o7TKr3nzbh5WgCFxe/giphy.gif',
                'https://media.giphy.com/media/zMQcrvqjkC9d6/giphy.gif',
                'https://media.giphy.com/media/cr9vIO7NsP5cY/giphy.gif',
                'https://media.giphy.com/media/l1OgggMcFwPidLdjtJ/giphy.gif',
                'https://media.giphy.com/media/8gQR12M5d4kPMRYoC1/giphy.gif'
            ]
            await ctx.send(random.choice(reactions))
    except Exception as e:
        print(e)
        await ctx.send('Exploté 💣')

@bot.command()
async def password(ctx):
    special_character = ['!', '@', '#', '$', '%', '^', '&', '*']
    faker = Faker()
    word1 = faker.word()
    word2 = faker.word()
    number = str(random.randint(0,9))
    sc = random.choice(special_character)
    words = word1.title() + word2.title() + sc
    words = list(words)
    words.append(number)
    random.shuffle(words)

    await ctx.send(f'{"".join(words)}')

@bot.command()
async def ban(ctx):
    roles = [o.name for o in ctx.message.author.roles]
    if 'mod' in roles or ctx.message.author.guild_permissions.administrator:
        user = ctx.message.mentions[0]
        timeout = BAN_TIMEOUT * 60
        r.setex(str(user.id), timeout, "banned")
        reactions = [
            'https://media.giphy.com/media/Vh2c84FAPVyvvjZJNM/giphy.gif',
            'https://media.giphy.com/media/H99r2HtnYs492/giphy.gif',
            'https://media.giphy.com/media/xT5LMDzs9xYtHXeItG/giphy.gif',
            'https://media.giphy.com/media/LPHbzPcICc86EVte9C/giphy.gif',
            'https://media.giphy.com/media/3o751XbGLXpORSxtQY/giphy.gif',
            'https://media.giphy.com/media/CybZqG4etuZsA/giphy.gif',
            'https://media.giphy.com/media/QC7jsHJ9Nlrtxby57y/giphy.gif',
            'https://media.giphy.com/media/py07OYVelqRd6/giphy.gif',
            'https://media1.tenor.com/images/7c9c0e53ce31b154a0bd124b73dec1c4/tenor.gif',
            'https://media1.tenor.com/images/04a581ec0a3331f01406aa7d4ecb617b/tenor.gif',
            'https://media1.tenor.com/images/8f74ba73b7d6902d3bbded13a1d4fab7/tenor.gif',
            'https://media1.tenor.com/images/131d5164ac3ae13066370377cdb2e8ad/tenor.gif',
            'https://media1.tenor.com/images/2664115d11d75f5343767fefbce8c98d/tenor.gif',
            'https://media1.tenor.com/images/ab4216680a6edd2ac2fcea2587429343/tenor.gif',
            'https://media1.tenor.com/images/84e564a937adbaee45e0828f0fcb0e98/tenor.gif',
            'https://media.makeameme.org/created/llamada-para-elba.jpg'
        ]
        await ctx.send(random.choice(reactions))
        await ctx.send(f'No voy a pescar a {user.name} por {BAN_TIMEOUT} minutos')
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command(name='diario')
async def newspaper(ctx, news_source):
    today = date.today()
    date_with_slashes = today.strftime('%Y/%m/%d')
    newspapers = {
        'segunda': {
            'url': f'http://img.kiosko.net/{date_with_slashes}/cl/cl_segunda.750.jpg'
        },
        'lun': {
            'url': f'http://img.kiosko.net/{date_with_slashes}/cl/cl_ultimas_noticias.750.jpg'
        },
        'mercurio': {
            'url': f'http://img.kiosko.net/{date_with_slashes}/cl/cl_mercurio.750.jpg'
        },
        'tercera': {
            'url': f'http://img.kiosko.net/{date_with_slashes}/cl/cl_tercera.750.jpg'
        },
        'cuarta': {
            'url': f'http://img.kiosko.net/{date_with_slashes}/cl/cl_cuarta.750.jpg'
        }
    }
    if news_source in newspapers:
        target_url = newspapers[news_source]['url']
        response = requests.get(target_url)
        if response.status_code == 200:
            await ctx.send(target_url)
        else:
            await ctx.send('No encontré la portada de hoy 😅')
    else:
        await ctx.send('No tengo ese diario, las opciones actuales son:')
        await ctx.send(f'{", ".join(newspapers.keys())}')

@bot.command()
async def cachipun(ctx, monedas, objeto):
    id = ctx.message.author.id
    user = ctx.message.author
    data = inv.find_one({'id':id})
    moneda_data = data['monedas']
    monedas = int(monedas)
    moneda_data = int(moneda_data)
    if data:
        if monedas > 0:
            if monedas <= moneda_data:
                if ctx.message.channel.name == "farmeo":
                    ppt = ['piedra', 'papel', 'tijera']
                    eleccion = random.choice(ppt)
                    if objeto.lower() == 'piedra':
                        if eleccion == 'piedra':
                            await ctx.send('Ah bueno, empatamos. Te quedas con las monedas que apostaste.')
                        if eleccion == 'papel':
                            await ctx.send('HAHAHA te gane. Me quedo con tus monedas 🤑')
                            moneda_final = moneda_data - monedas
                            inv.update_one({'id': id}, {'$set': {'monedas': moneda_final}})
                        if eleccion == 'tijera':
                            await ctx.send('NOOOOOOOOOO!! me has ganado. Te duplico las monedas que apostaste')
                            moneda_final = moneda_data + monedas
                            inv.update_one({'id': id}, {'$set': {'monedas': moneda_final}})
                    if objeto.lower() == 'papel':
                        if eleccion == 'piedra':
                            await ctx.send('Viejo curao 😠 ganaste, premio para ti.')
                            moneda_final = moneda_data + monedas
                            inv.update_one({'id': id}, {'$set': {'monedas': moneda_final}})
                        if eleccion == 'papel':
                            await ctx.send('Empatamos pero ya vas a ver chupetin.')
                        if eleccion == 'tijera':
                            await ctx.send('BOOM shakalaka, tus monedas son mias.')
                            moneda_final = moneda_data - monedas
                            inv.update_one({'id': id}, {'$set': {'monedas': moneda_final}})
                    if objeto.lower() == 'tijera':
                        if eleccion == 'piedra':
                            await ctx.send('Osi osi nena! las apuestas no son lo tuyo.')
                            moneda_final = moneda_data - monedas
                            inv.update_one({'id': id}, {'$set': {'monedas': moneda_final}})
                        if eleccion == 'papel':
                            await ctx.send('En serio?!?! ta chitado manito, monedas dobles para ti.')
                            moneda_final = moneda_data + monedas
                            inv.update_one({'id': id}, {'$set': {'monedas': moneda_final}})
                        if eleccion == 'tijera':
                            await ctx.send('Ñee que fome empatar, chau.')
                else:
                    await ctx.send('Intentalo en el canal de farmeo, este no es un lugar muy bonito para hacer eso.')
            else:
                await ctx.send('Alto ahi vaca, estas apostando monedas que no tienes.')
        else:
            await ctx.send('En serio? monedas negativas? tonton.')
    else:
        await ctx.send('No tienes monedas 😔 usa el comando "monedas" para obtener unas pocas.')

@bot.command(aliases = ['inv'])
async def inventario(ctx):
    id = ctx.message.author.id
    data = inv.find_one({'id':id})
    if data:
        if 'monedas' and 'madera' and 'roca' in data:
            await ctx.send(f'Tienes:\n-{data["monedas"]} monedas 💰\n-{data["madera"]} maderas 🪓\n-{data["roca"]} rocas')
        else:
            await ctx.send('Cuando tengas monedas, madera y rocas en tu inventario, te mostrare todo.')
    else:
        await ctx.send('Creo que no tienes nada en tu bolsa.')

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def talar(ctx):
    id = ctx.message.author.id
    data = inv.find_one({'id':id})
    numero = random.randint(1,3)
    if ctx.message.channel.name == 'farmeo':
        if data:
            if 'madera' in data:
                nueva_madera = data['madera'] + numero
                inv.update_one({'id':id}, {'$set': {'madera':nueva_madera}})
                madera = nueva_madera
            else:
                inv.update_one({'id':id}, {'$set': {'madera':numero}})
        else:
            inv.insert_one({'id': id, 'madera': numero})
        await ctx.send(f'Talaste {numero} madera normal')
    else:
        await ctx.send('No estas en el canal de farmeo, ve ahi y reintentalo.')

@bot.command()
@commands.cooldown(1, 300, commands.BucketType.user)
async def minar(ctx):
    id = ctx.message.author.id
    data = inv.find_one({'id':id})
    numero = random.randint(1,3)
    if ctx.message.channel.name == 'farmeo':
        if data:
            if 'roca' in data:
                nueva_roca = data['roca'] + numero
                inv.update_one({'id':id}, {'$set': {'roca':nueva_roca}})
                roca = nueva_roca
            else:
                inv.update_one({'id':id}, {'$set': {'roca':numero}})
        else:
            inv.insert_one({'id': id, 'roca': numero})
        await ctx.send(f'Minaste {numero} rocas ⛏️')
    else:
        await ctx.send('No estas en el canal de farmeo, ve ahi y reintentalo.')

@bot.command(name='thisman')
async def thisman(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    thisman = Image.open("./images/thisman.jpeg")

    user_avatar = user.avatar_url_as(format='png', size=128)
    data = BytesIO(await user_avatar.read())
    avatar = Image.open(data).convert('RGBA')
    avatar = avatar.resize((175, 210))
    img_bw = avatar.copy()
    img_bw = img_bw.convert('L')
    thisman.paste(img_bw, (175, 210), mask=avatar)

    thisman.save("profile.png", 'PNG')
    await ctx.send(file = discord.File("profile.png"))

@bot.command()
async def mimic(ctx, member: discord.Member, *, message=None):
    print(f'{ctx.author.name} is impersonating {member.name}')
    webhook = await ctx.channel.create_webhook(name=member.name)
    await webhook.send(str(message), username=member.name, avatar_url=member.avatar_url)

    webhooks = await ctx.channel.webhooks()
    for webhook in webhooks:
        await webhook.delete()

@bot.command(aliases=['zalgo', 'nicomen', 'inframundo'])
async def zalgofy(ctx, *, message):
    await ctx.send(generate_zalgo(message))

@bot.command()
async def activity(ctx, *, message):
    print(f'{ctx.message.author.name} >> {ctx.message.content}')
    options = message.split(',')
    activities = {
        'viendo': discord.ActivityType.watching,
        'jugando': discord.ActivityType.playing,
        'escuchando': discord.ActivityType.listening
    }
    await bot.change_presence(activity=discord.Activity(type=activities[options[0]], name=options[1]))

@bot.command(aliases=['recuerdame', 'recuérdame', 'recordatorio'])
async def remind(ctx, *, message):
    words = message.split(' ')
    time_unit = words[-1]
    amount = words[-2]
    if time_unit == 'segundos':
        seconds = int(amount)
    elif time_unit == 'minutos':
        seconds = int(amount) * 60
    elif time_unit == 'horas':
        seconds = int(amount) * 60 * 60
    else:
        seconds = 0
        await ctx.send('🤔 no entendí')

    if seconds != 0:
        await ctx.message.add_reaction('🆗')
        await asyncio.sleep(seconds)
        await ctx.send(f'oye {ctx.author.mention}, recuerda {" ".join(words[:-3])}')

@bot.command(aliases=['ficha'])
async def summon_bot(ctx):
    member = ctx.message.author
    role = discord.utils.get(ctx.message.guild.roles, name = "ficha")
    channel = discord.utils.get(ctx.guild.channels, name="general")
    await member.add_roles(role)
    await channel.send(f'{member.mention} se cree ficha')

@bot.command()
async def restart(ctx):
    roles = [o.name for o in ctx.message.author.roles]
    if '💻 dev' in roles:
        subprocess.run(["systemctl", "restart", "ybot"])
        await ctx.send("🆗")
    else:
        await ctx.send(ACCESS_DENIED)

print(i18n.t('base.start'))
bot.run(TOKEN)
