import discord
import os
import requests
from discord.ext import commands

EXCHANGE_APP_ID = os.getenv('EXCHANGE_APP_ID')
EXCHANGE_URL = os.getenv('EXCHANGE_URL')
UTM_URL = os.getenv('UTM_URL')

class Money(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['convierte', 'convertir', 'plata', '$'])
    async def convert(self, ctx, *, query):
        values = query.split(' ')
        amount = int(values[0])
        currency = values[1].upper()
        data = requests.get(f'{EXCHANGE_URL}{EXCHANGE_APP_ID}').json()
        usd = data['rates']['USD']
        base = data['rates']['CLP']
        target = data['rates'][currency]
        in_usd = amount / target
        final = round(base * in_usd)
        formatted = '{0:,}'.format(final)
        await ctx.send(f'🏦 {amount} {currency} → ${formatted} CLP')

    @commands.command()
    async def uf(self, ctx, *, query):
        req = requests.get(url = UTM_URL)
        response = req.json()
        values = query.split(' ')
        amount = int(values[0])
        values_uf = response['uf']['valor']
        total = amount*values_uf
        total_entero = int(total)
        formatted = '{0:,}'.format(total_entero)

        await ctx.send(f'🏦 {amount} UF son ${formatted} pesos')

    @commands.command()
    async def utm(self, ctx, *, query):
        req = requests.get(url = UTM_URL)
        response = req.json()
        values = query.split(' ')
        amount = int(values[0])
        values_utm = response['utm']['valor']
        total = amount*values_utm
        total_entero = int(total)
        formatted = '{0:,}'.format(total_entero)

        await ctx.send(f'🏦 {amount} UTM son ${formatted} pesos')

def setup(bot: commands.Bot):
    bot.add_cog(Money(bot))