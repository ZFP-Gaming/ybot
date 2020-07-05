import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='ybot ')

@bot.event
async def on_ready():
	  game = discord.Game('Viendo porno')
	  await bot.change_presence(status=discord.Status.idle, activity=game)

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

@bot.command()
async def hola(ctx):
    greetings = [
      'ola',
      'olas :ocean:',
      'wena wena',
      'kiu majaji',
      'que queri ahora ql'
    ]
    await ctx.send(random.choice(greetings))

@bot.command()
async def pregunta(ctx):
    answer =[
        "En mi opinión, sí",
        "Es cierto",
        "Es decididamente así",
        "Probablemente",
        "Buen pronóstico",
        "Todo apunta a que sí",
        "Sin duda",
        "Sí",
        "Sí - definitivamente",
        "Debes confiar en ello",
        "Respuesta vaga, vuelve a intentarlo",
        "Pregunta en otro momento",
        "Será mejor que no te lo diga ahora",
        "No puedo predecirlo ahora",
        "Concéntrate y vuelve a preguntar",
        "No cuentes con ello",
        "Mi respuesta es no",
        "Mis fuentes me dicen que no",
        "Las perspectivas no son buenas",
        "Muy dudoso"
      ]
    await ctx.send(random.choice(answer))

bot.run(TOKEN)
