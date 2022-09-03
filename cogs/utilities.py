import discord
import random
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong {int(self.bot.latency * 1000)}ms')

    @commands.command(name='random')
    async def random_choice(self, ctx, options):
        selected = random.choice(options.split(','))
        await ctx.send(f':game_die: {selected}')

    @commands.command()
    async def info(self, ctx):
        await ctx.send(ctx.guild)

    @commands.command()
    async def zoom(self, ctx):
        avatar = ctx.message.mentions[0].avatar_url_as(format='png', size=128)
        data = BytesIO(await avatar.read())
        img = Image.open(data)
        image.save("profile.png", 'PNG')
        await ctx.send(file = discord.File("profile.png"))

def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))