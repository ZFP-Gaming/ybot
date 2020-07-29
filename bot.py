import os
import random
import discord
import requests
import pdb # pdb.set_trace()
import pymongo
import wikipedia
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

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
SEARCH_URL = os.getenv('SEARCH_URL')
YOUTUBE_URL = os.getenv('YOUTUBE_URL')
EXCHANGE_APP_ID = os.getenv('EXCHANGE_APP_ID')
EXCHANGE_URL = os.getenv('EXCHANGE_URL')
UTM_URL = os.getenv('UTM_URL')
IMDB_URL = os.getenv('IMDB_URL')
IMDB_KEY = os.getenv('IMDB_KEY')

db = MongoClient()
members = db.bot.members
uncles = db.bot.uncles
actions = db.bot.actions
wikipedia.set_lang("es")

bot = commands.Bot(command_prefix=f'{BOT_PREFIX} ')

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

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="porno de enanos"))

@bot.event
async def on_message(message):
    if ('++' in message.content or '--' in message.content) and message.mentions:
        user = message.mentions[0].id
        author = message.author.id
        modifier = 1 if '++' in message.content else - 1
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

@bot.command(aliases = ['karma', 'ranking'])
async def karma_ranking(ctx):
    sorted = list(members.find().sort('karma', pymongo.DESCENDING))
    embed = discord.Embed(color=0xffffff)
    ranking = ''
    medals = {
        0: '🥇',
        1: '🥈',
        2: '🥉'
    }
    medals[len(sorted) - 1] = '💩'
    for i in range(len(sorted)):
        if 'karma' not in sorted[i]:
            continue
        user = bot.get_user(sorted[i]["id"])
        if user.bot:
            continue
        formatted_counter = medals[i] if i in medals else '🏅'
        formatted_karma = str(int(sorted[i]['karma'])).rjust(3)
        ranking = ranking + f'{formatted_counter} {user.name}: {formatted_karma}\n'
    embed.add_field(name='Ranking de karma', value=ranking, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

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
    params = {
        'q': query,
        'searchType': 'image',
        'safe': 'high',
        'fields': 'items(link)',
        'cx': GSE_ID,
        'key': GSE_KEY
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
    params = {
        'q': query,
        'key': GSE_KEY,
        'part': 'id',
        'type': 'video',
        'order': 'relevance',
        'maxResults': 15
    }
    data = requests.get(YOUTUBE_URL, params=params).json()
    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        await ctx.send(f'https://youtu.be/{video_id}')
        embed = discord.Embed(color=0x00ff2a)
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
    page = wikipedia.page(query)
    embed = discord.Embed(color=0x00ffe1)
    data = page.summary
    info = (data[:1000] + '...') if len(data) > 75 else data
    embed.add_field(name=page.title, value=info, inline=False)
    if page.images:
        embed.set_thumbnail(url=page.images[0])
    embed.add_field(name="Link", value=page.url, inline=False)
    await ctx.send(embed=embed)

print('CHORIZA ONLINE')

bot.run(TOKEN)
