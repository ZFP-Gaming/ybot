import discord
import subprocess
import time
import os

from discord.ext import commands
from os import path

ACCESS_DENIED = 'https://media.giphy.com/media/3ohzdYt5HYinIx13ji/giphy.gif'

class Management(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def restart(self, ctx):
        roles = [o.name for o in ctx.message.author.roles]
        if '💻 dev' in roles or 'zfp staff' in roles:
            await ctx.send("🆗")
            subprocess.run(["systemctl", "restart", "ybot"])
        else:
            await ctx.send(ACCESS_DENIED)

    @commands.command(name='respaldo')
    async def backup_database(self, ctx):
        roles = [o.name for o in ctx.message.author.roles]
        if '💻 dev' in roles:
            subprocess.run(["mongodump"])
            time.sleep(3)
            subprocess.run(["zip", "-r", "database.zip", "dump"])
            time.sleep(3)
            file = discord.File("database.zip")
            await ctx.send(file=file, content="Respaldo generado")
        else:
            await ctx.send(ACCESS_DENIED)

    @commands.command(name='mode')
    async def change_avatar(self, ctx, *, query):
        roles = [o.name for o in ctx.message.author.roles]
        if '💻 dev' in roles or 'zfp staff' in roles:
            img_route = f'./images/{query}.png'
            if path.exists(img_route):
                with open(img_route, 'rb') as image:
                    await self.bot.user.edit(avatar=image.read())
        else:
            await ctx.send(ACCESS_DENIED)

async def setup(bot: commands.Bot):
    await bot.add_cog(Management(bot))
