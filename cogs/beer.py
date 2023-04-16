import discord
import os
import requests
from discord.ext import commands

UNTAPPD_URL = os.getenv('UNTAPPD_URL')
UNTAPPD_ID = os.getenv('UNTAPPD_ID')
UNTAPPD_SECRET = os.getenv('UNTAPPD_SECRET')

class Beer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['pilsen', 'chela', 'xela', 'untappd'])
    async def beer(self, ctx, *, query):
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

async def setup(bot: commands.Bot):
    await bot.add_cog(Beer(bot))
