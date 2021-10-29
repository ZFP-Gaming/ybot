import discord
import os
import requests
from discord.ext import commands

RECRUITING_URL = os.getenv('RECRUITING_URL')

class Recruitment(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['estado'])
    async def recruiting_status(self, ctx, *, query):
        await ctx.message.add_reaction('🔍')
        req = requests.get(url = RECRUITING_URL)
        response = req.json()
        found = next(item for item in response if query in item['Nombre'])
        if found:
            await ctx.send(f'La postulación de **{found["Nombre"]}** se encuentra en el estado: **{found["status"]}**')
        else:
            await ctx.send("No se encontraron resultados")

    @commands.command(aliases=['postulaciones'])
    async def applications_list(self, ctx):
        req = requests.get(url = RECRUITING_URL)
        response = req.json()
        application_requests = ''
        embed = discord.Embed(color=0xffffff)
        for i in range(len(response)):
            application_requests = application_requests + f'{i+1}) {response[i]["Nombre"]} ({response[i]["status"]})\n'
        embed.add_field(name='Listado de postulaciones', value=application_requests, inline=False)
        await ctx.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(Recruitment(bot))
