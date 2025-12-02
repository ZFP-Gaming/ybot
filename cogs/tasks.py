import asyncio
import discord
import os
import random
import requests
import tweepy

from discord.ext import tasks, commands

class Tasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
      print("tweepy disabled for now")
      # self.meme_gatherer.start()

    @tasks.loop(hours=1)
    async def meme_gatherer(self):
        guild = next((item for item in self.bot.guilds if item.name == "ZFP Gaming"), None)
        if guild:
          consumer_key = os.getenv("TWITTER_API_KEY")
          consumer_secret = os.getenv("TWITTER_API_KEY_SECRET")
          access_token = os.getenv("TWITTER_ACCESS_TOKEN")
          access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
          channel = discord.utils.get(guild.channels, name="memes")
          auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
          auth.set_access_token(access_token, access_token_secret)
          api = tweepy.API(auth)
          username ="hourly_shitpost"
          tweets_list = api.user_timeline(screen_name=username, count=1)
          tweet = tweets_list[0]
          video_link = tweet.extended_entities["media"][0]["video_info"]["variants"][0]["url"]
          if ".m3u8" in video_link:
            channel = discord.utils.get(guild.channels, name="qa")
            await channel.send(video_link)
          else:
            r = requests.get(video_link, allow_redirects=True)
            open("videomeme.mp4", "wb").write(r.content)
            await channel.send(file=discord.File("videomeme.mp4"))
            os.remove("videomeme.mp4")

async def setup(bot: commands.Bot):
    await bot.add_cog(Tasks(bot))
