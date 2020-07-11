import os
import random
import discord
import requests
import pdb # pdb.set_trace()
import pymongo
from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')
YOLI_URL = os.getenv('YOLI_URL')
COVID_URL = os.getenv('COVID_URL')
ANIME_URL = os.getenv('ANIME_URL')
INUTIL_URL = os.getenv('INUTIL_URL')

client = MongoClient()
members = client.bot.members
uncles = client.bot.uncles
bot = commands.Bot(command_prefix=f'{BOT_PREFIX} ')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="porno de enanos"))

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
        members.insert_one({'id': id, 'description': description})

@bot.command()
async def quien(ctx):
    id = ctx.message.mentions[0].id
    data = members.find_one({'id': id})
    name = ctx.message.mentions[0].nick or ctx.message.mentions[0].name
    if data:
        await ctx.send(f'{name} es {data["description"]}')
    else:
        await ctx.send(f'No conozco a {name}')

print('CHORIZA ONLINE')

bot.run(TOKEN)
