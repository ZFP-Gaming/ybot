import discord
import os
import requests
from discord.ext import commands

urlMarkets = 'https://www.buda.com/api/v2/markets'
responseMarket = requests.get(urlMarkets)

market_id = 'btc-clp' #response.name
urlTicker = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'
responseTicker = requests.get(urlTicker)



class Shark(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot  
        
    @commands.command()
    async def mercados(self, ctx):
        responseMarket = requests.get(urlMarkets)
        response = responseMarket.json()
        mercado = []
        for x in response:
            if x.quote_currency == 'CLP':
                mercado.append(x.name)

        await ctx.send(f'Mercado: {mercado}')
        
    @commands.command()
    async def valor(self, ctx, *, query):
        await ctx.message.add_reaction('🔍')
        urlTicker = f'https://www.buda.com/api/v2/markets/{query}/ticker'
        responseMarket = requests.get(urlTicker)
        response = responseMarket.json()
        
        await ctx.send(f'El ultimo precio fue $**{response.last_price[0]}** **{response.last_price[1]}**')
            
def setup(bot: commands.Bot):
    bot.add_cog(Shark(bot))
