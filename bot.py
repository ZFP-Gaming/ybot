import os
import random
import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_PREFIX = os.getenv('BOT_PREFIX')
YOLI_URL = os.getenv('YOLI_URL')
COVID_URL = os.getenv('COVID_URL')
ANIME_URL = os.getenv('ANIME_URL')

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
    await covid_data.add_reaction('\U0001F1EB')
    covid_data = await ctx.send(f'Confirmados: {confirmed} :facepalm:\nRecuperados: {recovered} :tada:\nMuertitos: {deaths} :regional_indicator_f:')

@bot.command()
async def otaku(ctx, *, query):
    req = requests.get(url = ANIME_URL + query)
    response = req.json()

    title = response['results'][0]['title']
    title1 = response['results'][1]['title']
    score = response['results'][0]['score']
    score1 = response['results'][1]['score']
    message = f'''Título: {title}\nPuntuacion: {score}
    \nTitulo: {title1}\nPuntuacion: {score1}
    '''
    await ctx.send(message)

print('CHORIZA ONLINE')


bot.run(TOKEN)
