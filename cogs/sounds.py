import os
import glob
import random
import discord

from os import path
from os import listdir
from os.path import isfile, join
from gtts import gTTS
from discord.ext import commands

ACCESS_DENIED = 'https://media.giphy.com/media/3ohzdYt5HYinIx13ji/giphy.gif'

class Sounds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def check_queue(bot, voice_client):
        if bot.queue != []:
            sound_effect = bot.queue.pop(0)
            voice_client.play(discord.FFmpegPCMAudio(sound_effect), after=lambda x: check_queue(bot, voice_client))
            voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
            voice_client.source.volume = bot.volume

    @commands.command(name='sonidos')
    async def sound_list(self, ctx):
        files_path = f'{os.getcwd()}/sounds'
        files_directory = os.listdir(files_path)

        files = sorted(files_directory)
        page_size = 20

        pages = [files[i: i + page_size] for i in range(0, len(files), page_size)]
        paginated_content = []

        for page in pages:
            embed = discord.Embed()
            sounds_list = '```\n'
            for file in page:
                sounds_list += f'- {file.split(".")[0]}\n'
            sounds_list += '```'
            embed.add_field(name='🔈 Lista de sonidos disponibles', value=sounds_list, inline=False)
            paginated_content.append(embed)

        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
        current = 0
        msg = await ctx.send(embed=paginated_content[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except Exception as e:
                return print(e)

            else:
                previous_page = current
                if reaction.emoji == u"\u23EA":
                    current = 0

                elif reaction.emoji == u"\u2B05":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == u"\u27A1":
                    if current < len(paginated_content)-1:
                        current += 1

                elif reaction.emoji == u"\u23E9":
                    current = len(paginated_content)-1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=paginated_content[current])

    @command.command(aliases=['s'])
    async def sound(self, ctx, effect):
        sound_effect = list(glob.glob(f'sounds/{effect}*.mp3'))[0]
        print(f'{ctx.message.author} > {sound_effect}')
        try:
            if sound_effect and path.exists(sound_effect):
                voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                if not voice_client:
                    channel = ctx.message.author.voice.channel
                    await channel.connect()
                if ctx.author.voice and ctx.voice_client:
                    vc = ctx.voice_client
                    await ctx.message.delete()
                    if not vc.is_playing():
                        print('Empty queue, playing...')
                        vc.play(discord.FFmpegPCMAudio(sound_effect), after=lambda x: check_queue(self.bot, vc))
                        vc.source = discord.PCMVolumeTransformer(vc.source)
                        vc.source.volume = self.bot.volume
                    else:
                        print(f'Added to queue: {sound_effect}')
                        queue.append(sound_effect)
                else:
                    await ctx.send('No estás conectado a un canal de audio')
            else:
                await ctx.send('No tengo ese sonido compare, envía un correo a soporte@ybot.com')
        except Exception as e:
            print(e)
            await ctx.send('Exploté 💣')

    @command.command()
    async def seba(self, ctx, effect):
        sound_effect = f'sounds/{effect}.mp3'
        try:
            if ctx.message.author.id == 121417708469223428:
                if path.exists(sound_effect):
                    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
                    if not voice_client:
                        channel = ctx.message.author.voice.channel
                        await channel.connect()
                    if ctx.author.voice and ctx.voice_client:
                        vc = ctx.voice_client
                        if not vc.is_playing():
                            print('Empty queue, playing...')
                            for i in range(9):
                                self.bot.queue.append(sound_effect)
                            vc.play(discord.FFmpegPCMAudio(sound_effect), after=lambda x: check_queue(self.bot, vc))
                            vc.source = discord.PCMVolumeTransformer(vc.source)
                            vc.source.volume = self.bot.volume
                        else:
                            print(f'Added to queue: {sound_effect}')
                            for i in range(10):
                                self.bot.queue.append(sound_effect)
                    else:
                        await ctx.send('No estás conectado a un canal de audio')
                else:
                    await ctx.send('No tengo ese sonido compare, envía un correo a soporte@ybot.com')
            else:
                reactions = [
                    'https://media.giphy.com/media/3oFzmko6SiknmpR2NO/giphy.gif',
                    'https://media.giphy.com/media/mcH0upG1TeEak/giphy.gif',
                    'https://media.giphy.com/media/lTYXWBnuA4oFA5R3dp/giphy.gif',
                    'https://media.giphy.com/media/3o7TKr3nzbh5WgCFxe/giphy.gif',
                    'https://media.giphy.com/media/zMQcrvqjkC9d6/giphy.gif',
                    'https://media.giphy.com/media/cr9vIO7NsP5cY/giphy.gif',
                    'https://media.giphy.com/media/l1OgggMcFwPidLdjtJ/giphy.gif',
                    'https://media.giphy.com/media/8gQR12M5d4kPMRYoC1/giphy.gif'
                ]
                await ctx.send(random.choice(reactions))
        except Exception as e:
            print(e)
            await ctx.send('Exploté 💣')

    @command.command()
    async def tts(self, ctx, *, msg):
        id = ctx.message.author.id
        data = self.bot.members.find_one({'id': id})
        roles = [o.name for o in ctx.message.author.roles]
        message = msg.split('/')
        text_to_speech = message[0]
        language = message[1] if len(message) > 1 else 'es'
        if ('💻 dev' in roles) or data['karma'] > 10:
            tts = gTTS(text=text_to_speech, lang=language)
            tts.save("tts.mp3")
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            if not voice_client:
                channel = ctx.message.author.voice.channel
                await channel.connect()
            vc = ctx.voice_client
            vc.play(discord.FFmpegPCMAudio('tts.mp3'), after=lambda x: check_queue(self.bot, vc))
            vc.source = discord.PCMVolumeTransformer(vc.source)
            vc.source.volume = self.bot.volume
        else:
            await ctx.send(ACCESS_DENIED)

def setup(bot: commands.Bot):
    bot.add_cog(Sounds(bot))
