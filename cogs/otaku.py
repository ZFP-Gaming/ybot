import discord
import os
import random
import requests
from discord.ext import commands

ANIME_URL = os.getenv('ANIME_URL')

class Otaku(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def pokimon(self, ctx):
        base = random.randint(1, 151)
        face = random.randint(1, 151)
        url = f'https://images.alexonsager.net/pokemon/fused/{base}/{base}.{face}.png'
        await ctx.send(url)

    @commands.command(aliases = ['anime'])
    async def otaku(self, ctx, *, query):
        req = requests.get(url = ANIME_URL + query)
        response = req.json()
        embed = discord.Embed(
            colour = discord.Colour.purple()
        )
        try:
            found = next(item for item in response['results'] if item['title'].lower() == query.lower())

            if found:
                embed.add_field(name=found['title'], value=f':star: {found["score"]}', inline=True)
                embed.add_field(name=('Capítulos'), value=found["episodes"], inline=True)
                embed.add_field(name=('Transmitiendo'), value=found["airing"], inline=False)
                embed.set_image(url=found['image_url'])

        except StopIteration as e:
            embed.add_field(name=response['results'][0]['title'], value=f':star: {response["results"][0]["score"]}', inline=True)
            embed.add_field(name=('Capítulos'), value=response['results'][0]["episodes"], inline=True)
            embed.add_field(name=('Transmitiendo'), value=response['results'][0]["airing"], inline=False)
            embed.set_image(url=response['results'][0]['image_url'])

        await ctx.send(embed=embed)

    @commands.command()
    async def nya(self, ctx):
        await ctx.send('nyanyame nyanyajyu nyanya-do no nyarabi de nyakunyaku inyanyaku nyanyahan nyanya-dai nyannyaku nyarabete nyaganyagame')
        await ctx.send('https://pa1.narvii.com/6151/7d3b92d97a9e694d2c7a3ea696eadeb79988821d_hq.gif')

async def setup(bot: commands.Bot):
    await bot.add_cog(Otaku(bot))