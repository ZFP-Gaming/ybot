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
BASE_GREETINGS = [
    'olas :ocean:',
    'wena wena',
    'kiu majaji',
    'que queri ahora ql'
]
PROFANITIES = [
    'eri puro wn',
    'tu mamá es el vitoco',
    'puro perro logi ql',
    'deja de dar dislikes tonto wn',
    'maldito sapo conchetumare',
    'chupala meando',
    'prepara las nalgas porque te voy a dejar como bambi',
    'a tu mamá le quedan malas las cazuelas'
]
KING_PRHASES = [
    'Maricones chupenme la raja con caca',
    'Mysterion lo más grande',
    'Tu conoces el sexo? Tu no conoces el sexo',
    'Mi destino ya esta trazao y se llama éxito',
    'Nunca hay chupao zorra',
    'viska spilli fudbar',
    'vilus spille memey?',
    'obisnake'
]

class Speech(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def pregunta(self, ctx):
        await ctx.send(random.choice(ANSWERS))

    @commands.command(aliases=['hola', 'ola', 'holas', 'olas', 'wenas', 'wena', 'holanda'])
    async def greet(ctx):
        ctx_greetings = [
            f'hola po {ctx.message.author.name}'
        ]
        await ctx.send(random.choice(BASE_GREETINGS + ctx_greetings))

    @commands.command()
    async def putea(ctx, *, name):
        victim = name.replace("a ", "")
        await ctx.send(f'oe {victim} {random.choice(PROFANITIES)}')

    @commands.command()
    async def king(ctx):
        await ctx.send(random.choice(KING_PRHASES))

async def setup(bot: commands.Bot):
    await bot.add_cog(Speech(bot))