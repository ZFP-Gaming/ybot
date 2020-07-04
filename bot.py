import os
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
    print('Buena cabros kls')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')



bot.run(TOKEN)
