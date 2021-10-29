import discord
import os
import requests
from discord.ext import commands

urlMarkets = 'https://www.buda.com/api/v2/markets'
response = requests.get(urlMarkets)

market_id = 'btc-clp' """ response.name """
urlTicker = f'https://www.buda.com/api/v2/markets/{market_id}/ticker'
response = requests.get(urlTicker)



class Shark(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

def setup(bot: commands.Bot):
    bot.add_cog(Shark(bot))