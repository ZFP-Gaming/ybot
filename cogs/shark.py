import discord
import requests
from discord.ext import commands

market_url = 'https://www.buda.com/api/v2/markets'

class Shark(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def mercados(self, ctx):
        response_markets = requests.get(market_url)
        parsed_markets = response_markets.json()
        names_array = []
        for market in parsed_markets:
            if market.quote_currency == 'CLP':
                names_array.append(market.name)

        await ctx.send(f'Mercado: {names_array}')

    @commands.command()
    async def valor(self, ctx, *, query):
        await ctx.message.add_reaction('🔍')
        ticker_url = f'https://www.buda.com/api/v2/markets/{query}/ticker'
        response_ticker = requests.get(ticker_url)
        parsed_info = response_ticker.json()

        await ctx.send(f'El ultimo precio fue $**{parsed_info.last_price[0]}** **{parsed_info.last_price[1]}**')

async def setup(bot: commands.Bot):
    await bot.add_cog(Shark(bot))
