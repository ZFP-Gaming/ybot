import discord
import os
import requests
from discord.ext import commands

COVID_URL = os.getenv('COVID_URL')
SISMOS_URL = os.getenv('SISMOS_URL')
INUTIL_URL = os.getenv('INUTIL_URL')

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def sismo(self, ctx):
        json_data = requests.get(url = SISMOS_URL).json()
        location = json_data['ultimos_sismos_chile'][0]['reference']
        time = json_data['ultimos_sismos_chile'][0]['chilean_time']
        magnitude = json_data['ultimos_sismos_chile'][0]['magnitude']
        depth = json_data['ultimos_sismos_chile'][0]['depth']

        await ctx.send(f'Lugar: {location}\nHora: {time}\nMagnitud: {magnitude}\nProfundidad: {depth}')

    @commands.command(help="Con este comando puedes revisar los contagiados, muertos y recuperados por Covid-19 en Chile.")
    async def covid(self, ctx):
        json_data = requests.get(url = COVID_URL).json()
        confirmed = json_data['confirmed']['value']
        recovered = json_data['recovered']['value']
        deaths = json_data['deaths']['value']

        covid_data = await ctx.send(f'Confirmados: {confirmed} :facepalm:\nRecuperados: {recovered} :tada:\nMuertitos: {deaths} :regional_indicator_f:')
        await covid_data.add_reaction('\U0001F1EB')

    @commands.command()
    async def dato(self, ctx):
        req = requests.get(url = INUTIL_URL)
        response = req.json()

        dato = response['text']
        await ctx.send(dato)

def setup(bot: commands.Bot):
    bot.add_cog(Info(bot))
