import discord
import random
from discord.ext import commands

ANSWERS = [
    'En mi opinión, sí',
    'Es cierto',
    'Es decididamente así',
    'Probablemente',
    'Buen pronóstico',
    'Todo apunta a que sí',
    'Sin duda',
    'Sí',
    'Sí - definitivamente',
    'Debes confiar en ello',
    'Respuesta vaga, vuelve a intentarlo',
    'Pregunta en otro momento',
    'Será mejor que no te lo diga ahora',
    'No puedo predecirlo ahora',
    'Concéntrate y vuelve a preguntar',
    'No cuentes con ello',
    'Mi respuesta es no',
    'Mis fuentes me dicen que no',
    'Las perspectivas no son buenas',
    'Muy dudoso',
    'Yo no volveria a confiar'
]

class Speech(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def pregunta(self, ctx):
        await ctx.send(random.choice(ANSWERS))

def setup(bot: commands.Bot):
    bot.add_cog(Speech(bot))