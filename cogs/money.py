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
        json_data = requests.get(f'{EXCHANGE_URL}{EXCHANGE_APP_ID}').json()
        values = query.split(' ')
        amount = int(values[0])
        currency = values[1].upper()
        base_rate = json_data['rates']['CLP']
        target_rate = json_data['rates'][currency]

        amount_in_usd = amount / target_rate
        final_value = round(base_rate * amount_in_usd)
        formatted_value = '{0:,}'.format(final_value)

        await ctx.send(f'🏦 {amount} {currency} → ${formatted_value} CLP')

    @commands.command()
    async def uf(self, ctx, *, query):
        json_data = requests.get(url = UTM_URL).json()
        values = query.split(' ')
        amount = int(values[0])
        uf_value = json_data['uf']['valor']

        total = int(amount * uf_value)
        formatted_total = '{0:,}'.format(total)

        await ctx.send(f'🏦 {amount} UF son ${formatted_total} pesos')

    @commands.command()
    async def utm(self, ctx, *, query):
        json_data = requests.get(url = UTM_URL).json()
        values = query.split(' ')
        amount = int(values[0])
        utm_value = json_data['utm']['valor']

        total = int(amount * utm_value)
        formatted_total = '{0:,}'.format(total)

        await ctx.send(f'🏦 {amount} UTM son ${formatted_total} pesos')

def setup(bot: commands.Bot):
    bot.add_cog(Money(bot))