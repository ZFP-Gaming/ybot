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

from os import path
from os import listdir
from os.path import isfile, join
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
from discord.ext import commands
from PIL import Image
from io import BytesIO
from gtts import gTTS
from bs4 import BeautifulSoup

load_dotenv()
KARMA_COOLDOWN = 30
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')
YOLI_URL = os.getenv('YOLI_URL')
COVID_URL = os.getenv('COVID_URL')
ANIME_URL = os.getenv('ANIME_URL')
INUTIL_URL = os.getenv('INUTIL_URL')
GSE_KEY = os.getenv('GSE_KEY')
GSE_ID = os.getenv('GSE_ID')
GSE_ID_NSFW = os.getenv('GSE_ID_NSFW')
GSE_KEY_NSFW = os.getenv('GSE_KEY_NSFW')
SEARCH_URL = os.getenv('SEARCH_URL')
YOUTUBE_URL = os.getenv('YOUTUBE_URL')
EXCHANGE_APP_ID = os.getenv('EXCHANGE_APP_ID')
EXCHANGE_URL = os.getenv('EXCHANGE_URL')
UTM_URL = os.getenv('UTM_URL')
IMDB_URL = os.getenv('IMDB_URL')
IMDB_KEY = os.getenv('IMDB_KEY')
LOL_URL = os.getenv('LOL_URL')
LOL_APIKEY = os.getenv('LOL_APIKEY')
CHAMP_URL = os.getenv('CHAMP_URL')
MONGO_URL = os.getenv('MONGO_URL')
DDRAGON_URL = os.getenv('DDRAGON_URL')
SISMOS_URL = os.getenv('SISMOS_URL')
UNTAPPD_URL = os.getenv('UNTAPPD_URL')
UNTAPPD_ID = os.getenv('UNTAPPD_ID')
UNTAPPD_SECRET = os.getenv('UNTAPPD_SECRET')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
ACCESS_DENIED = 'https://media.giphy.com/media/3ohzdYt5HYinIx13ji/giphy.gif'

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

bot = commands.Bot(command_prefix=f'{BOT_PREFIX} ')
bot.volume = 1.0

reddit = praw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
    user_agent="ybot"
)

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

@bot.event
async def on_ready():
    viendo = [
        'manquear al Darío',
        'al número 1 del cba',
        'porno de enanos',
        'a la Coty haciendo origami',
        'al Nete trabajando',
        'al Fabián cornerchopeando'
    ]
    actividad = [
        '1',
        '2'
    ]
    escuchar = [
        'Rock pesado lml',
        'Bad Bunny',
        'chinos cochinos',
        'openings de animes',
        'cumbia villera'
    ]
    elegir = random.choice(actividad)
    if elegir == '1':
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(viendo)))
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=random.choice(escuchar)))

@bot.event
async def on_message(message):
    msg = message.content.split(' ')
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
        if before.channel is None and after.channel is not None and member.bot == False:
            voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
            if voice_client and voice_client.channel == after.channel:
                id = member.id
                data = intros.find_one({'id': id})
                if data and data['effect'] != '' and path.exists(f'sounds/{data["effect"]}.mp3'):
                    voice_client.play(discord.FFmpegPCMAudio(f'sounds/{data["effect"]}.mp3'))
                    voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
                    voice_client.source.volume = bot.volume
                else:
                    print(f'{member.name} no tiene un sonido registrado')
        if after.channel is None:
            voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
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

@bot.command()
async def ping(ctx):
    await ctx.send(f'pong {int(bot.latency * 1000)}ms')

@bot.command(name='random')
async def random_choice(ctx, options):
    selected = random.choice(options.split(','))
    await ctx.send(f':game_die: {selected}')

@bot.command()
async def info(ctx):
    await ctx.send(ctx.guild)

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
        'prepara las nalgas porque te voy a dejar como bambi'
    ]
    await ctx.send(f'oe {name.replace("a ", "")} {random.choice(lista)}')

@bot.command(aliases=['hola', 'ola', 'holas', 'olas', 'wenas', 'wena'])
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
        'Muy dudoso'
    ]
    await ctx.send(random.choice(answer))

@bot.command(name='horoscopo')
async def fortune(ctx, sign):
    req = requests.get(url = YOLI_URL)
    prediction = req.json()['horoscopo']
    response = 'Ese no es un signo válido'
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
async def covid(ctx):
    req = requests.get(url = COVID_URL)
    response = req.json()

    confirmed = response['confirmed']['value']
    recovered = response['recovered']['value']
    deaths = response['deaths']['value']
    covid_data = await ctx.send(f'Confirmados: {confirmed} :facepalm:\nRecuperados: {recovered} :tada:\nMuertitos: {deaths} :regional_indicator_f:')
    await covid_data.add_reaction('\U0001F1EB')

@bot.command(aliases = ['anime'])
async def otaku(ctx, *, query):
    req = requests.get(url = ANIME_URL + query)
    response = req.json()
    found = next(item for item in response['results'] if item['title'].lower() == query.lower())

    embed = discord.Embed(
        colour = discord.Colour.purple()
    )

    if found:
        embed.add_field(name=found['title'], value=f':star: {found["score"]}', inline=True)
        embed.add_field(name=('Capítulos'), value=found["episodes"], inline = True)
        embed.add_field(name=('Transmitiendo'), value=found["airing"], inline = False)
        embed.set_image(url=found['image_url'])
    else:
        embed.add_field(name=response['results'][0]['title'], value=f':star: {response["results"][0]["score"]}', inline=True)
        embed.add_field(name=('Capítulos'), value=response['results'][0]["episodes"], inline = True)
        embed.add_field(name=('Transmitiendo'), value= response['results'][0]["airing"], inline=False)
        embed.set_image(url=response['results'][0]['image_url'])

    await ctx.send(embed=embed)

@bot.command()
async def dato(ctx):
    req = requests.get(url = INUTIL_URL)
    response = req.json()

    dato = response['text']
    await ctx.send(dato)

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
        embed.set_image(url=random.choice(data['items'])['link'])
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

@bot.command(aliases=['convierte', 'convertir', 'plata', '$'])
async def convert(ctx, *, query):
    values = query.split(' ')
    amount = int(values[0])
    currency = values[1].upper()
    data = requests.get(f'{EXCHANGE_URL}{EXCHANGE_APP_ID}').json()
    usd = data['rates']['USD']
    base = data['rates']['CLP']
    target = data['rates'][currency]
    in_usd = amount / target
    final = round(base * in_usd)
    formatted = '{0:,}'.format(final)
    await ctx.send(f'🏦 {amount} {currency} → ${formatted} CLP')

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

@bot.command()
async def uf(ctx, *, query):
    req = requests.get(url = UTM_URL)
    response = req.json()
    values = query.split(' ')
    amount = int(values[0])
    values_uf = response['uf']['valor']
    total = amount*values_uf
    total_entero = int(total)
    formatted = '{0:,}'.format(total_entero)

    await ctx.send(f'🏦 {amount} UF son ${formatted} pesos')

@bot.command()
async def utm(ctx, *, query):
    req = requests.get(url = UTM_URL)
    response = req.json()
    values = query.split(' ')
    amount = int(values[0])
    values_utm = response['utm']['valor']
    total = amount*values_utm
    total_entero = int(total)
    formatted = '{0:,}'.format(total_entero)

    await ctx.send(f'🏦 {amount} UTM son ${formatted} pesos')

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
    sound_effect = f'sounds/{effect}.mp3'
    try:
        if path.exists(sound_effect):
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            if not voice_client:
                channel = ctx.message.author.voice.channel
                await channel.connect()
            if ctx.author.voice and ctx.voice_client:
                vc = ctx.voice_client
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
    sounds = '```Lista de sonidos disponibles:\n'
    files_path = f'{os.getcwd()}/sounds'
    files_directory = os.listdir(files_path)
    for file in sorted(files_directory):
        sounds += f'- {file.split(".")[0]}\n'
    sounds += '```'
    await ctx.send(sounds)

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
async def pokimon(ctx):
    base = random.randint(1, 151)
    face = random.randint(1, 151)
    url = f'https://images.alexonsager.net/pokemon/fused/{base}/{base}.{face}.png'
    await ctx.send(url)

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

@bot.command()
async def sismo(ctx):
    req = requests.get(url = SISMOS_URL)
    response = req.json()
    referencia1 = response['ultimos_sismos_chile'][0]['reference']
    hora1 = response['ultimos_sismos_chile'][0]['chilean_time']
    magnitud1 = response['ultimos_sismos_chile'][0]['magnitude']
    profundidad1 = response['ultimos_sismos_chile'][0]['depth']

    await ctx.send(f'Lugar: {referencia1}\nHora: {hora1}\nMagnitud: {magnitud1}\nProfundidad: {profundidad1}')

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
async def elegir(ctx, clase):
    id = ctx.message.author.id
    data = inv.find_one({'id':id})
    if data:
        await ctx.send('Ya tienes un personaje creado. Si quieres empezar uno nuevo, elimina tu personaje con el comando "y eliminar".')
    else:
        if clase.lower() == 'guerrero':
            inv.insert_one({'id':id, 'personaje':'Guerrero', 'cabeza':'yelmo nivel 1', 'cuerpo':'peto de malla nivel 1',  'manos':'brazales nivel 1', 'piernas':'grebas nivel 1', 'pies':'botas nivel 1', 'arma primaria':'espada de madera', 'arma secundaria':'escudo de madera'})
            await ctx.send(f'Felicidades! Ya eres un Guerrero.\nSe agregó a tu inventario lo siguiente:\n-Yelmo nivel 1\n-Peto de malla nivel 1\n-Brazales nivel 1\n-Grebas nivel 1\n-Botas nivel 1\n-Espada de madera\n-Escudo de madera')
        if clase.lower() == 'arquero':
            inv.insert_one({'id':id, 'personaje':'Arquero', 'cabeza':'capucha nivel 1', 'cuerpo':'peto de cuero nivel 1',  'manos':'guantes nivel 1', 'piernas':'piernas nivel 1', 'pies':'botas nivel 1', 'arma primaria':'arco nivel 1', 'arma secundaria':'carcaj nivel 1'})
            await ctx.send(f'Felicidades! Ya eres un Arquero.\nSe agregó a tu inventario lo siguiente:\n-Capucha nivel 1\n-Peto de cuero nivel 1\n-Guantes nivel 1\n-Piernas nivel 1\n-Botas nivel 1\n-Arco nivel 1\n-Carcaj nivel 1')
        if clase.lower() == 'huaso':
            inv.insert_one({'id':id, 'personaje':'Huaso', 'cabeza':'chupalla nivel 1', 'cuerpo':'manta de huaso nivel 1', 'manos':'pañuelo nivel 1', 'piernas':'pantalones de huaso nivel 1', 'pies':'botas de huaso nivel 1', 'arma primaria':'empanada', 'arma secundaria':'anticucho'})
            await ctx.send(f'Felicidades! Ya eres un Huaso.\nSe agrego a tu inventario lo siguiente:\n-Chupalla nivel 1\n-Manta de huaso nivel 1\n-Pañuelo nivel 1\n-Pantalones de huaso nivel 1\n-Botas de huaso nivel 1\n-Empanada\n-Anticucho')

@bot.command()
async def personaje(ctx):
    id = ctx.message.author.id
    data = inv.find_one({'id':id})
    if data:
        await ctx.send(f'Tu personaje es clase {data["personaje"]}')
    else:
        await ctx.send('No tienes ningun personaje. Crea uno con el comando "y elegir".')

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

@bot.command()
async def eliminar(ctx):
    id = ctx.message.author.id
    inv.delete_one({'id':id})

    await ctx.send('Tu personaje ha sido eliminado del mundo ZFP.')

objetos.remove()
objetos.insert_one({'nombre':'espada nivel 1', 'daño':5, 'elemento':'neutro'})
objetos.insert_one({'nombre':'arco', 'daño':6, 'elemento':'neutro'})
objetos.insert_one({'nombre':'escudo de madera', 'defensa':3, 'resistencia':'neutro'})
objetos.insert_one({'nombre':'carcaj', 'daño':2, 'elemento':'neutro'})

@bot.command()
async def arma(ctx, *nombre):
    data = objetos.find_one({'nombre':nombre})
    #await ctx.send(f'Daño: {data["daño"]}\nElemento: {data["elemento"]}')
    await ctx.send('Este comando aun esta en construccion. Recuerda que estas en la version Alpha de World of ZFP')

@bot.command()
async def armadura(ctx, *nombre):
    data = objetos.find_one({'nombre':nombre})
    #await ctx.send(f'Defensa: {data["defensa"]}\nResistencia: {data["resistencia"]}')
    await ctx.send('Este comando aun esta en construccion. Recuerda que estas en la version Alpha de World of ZFP')

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
async def comprar(ctx, cantidad, objeto):
    id = ctx.message.author.id
    dataMembers = members.find_one({'id':id})
    dataInv = inv.find_one({'id':id})
    cantidad = int(cantidad)
    if cantidad >= 0:
        if objeto.lower() == 'karma':
            precio = cantidad * 500
            if dataInv['monedas'] >= precio:
                nuevas_monedas = dataInv['monedas'] - precio
                inv.update_one({'id':id}, {'$set': {'monedas':nuevas_monedas}})
                nuevo_karma = dataMembers['karma'] + cantidad
                members.update_one({'id':id}, {'$set': {'karma':nuevo_karma}})

                await ctx.send(f'Tu compra ha sido un exito! te quedaron {nuevas_monedas} monedas y ahora tienes {nuevo_karma} puntos de karma.')
            else:
                await ctx.send(f'No tienes las monedas suficientes para comprar {cantidad} puntos de karma.')
        else:
            await ctx.send('Creo que no tengo ese objeto a la venta, pero se lo pedire a los chinos.')     
    else:
        await ctx.send('Numeros negativos? entero logi pao ql')          

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
        queue.append('sounds/drums.mp3')
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = bot.volume
    else:
        await ctx.send(ACCESS_DENIED)

@bot.command()
async def shuffle(ctx, *, msg):
    ordered = msg.split(',')
    random.shuffle(ordered)

    await ctx.send(','.join(ordered))

print('CHORIZA ONLINE')
bot.run(TOKEN)
