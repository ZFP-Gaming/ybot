import discord
from discord.ext import commands

class RoleManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['contratar'])
    async def hire(self, ctx):
        if ctx.message.author.id == 121417708469223428:
            role = discord.utils.get(ctx.message.guild.roles, name = "recorrido")
            channel = discord.utils.get(ctx.guild.channels, name="recorrido")
            member = ctx.message.mentions[0]
            await member.add_roles(role)
            await channel.send(f'🚌 {member.mention} 🤗')

    @commands.command(aliases=['despedir'])
    async def fire(self, ctx):
        if ctx.message.author.id == 121417708469223428:
            role = discord.utils.get(ctx.message.guild.roles, name = "recorrido")
            channel = discord.utils.get(ctx.guild.channels, name="recorrido")
            member = ctx.message.mentions[0]
            await member.remove_roles(role)
            await channel.send(f'🥾💥 {member.mention}')

    @commands.command(aliases=['magia'])
    async def tcg_add(self, ctx):
        if ctx.message.author.id == 364613350623281164:
            role = discord.utils.get(ctx.message.guild.roles, name = "tcg-flip")
            member = ctx.message.mentions[0]
            await member.add_roles(role)

    @commands.command(aliases=['antimagia'])
    async def tcg_remove(self, ctx):
        if ctx.message.author.id == 364613350623281164:
            role = discord.utils.get(ctx.message.guild.roles, name = "tcg-flip")
            member = ctx.message.mentions[0]
            await member.remove_roles(role)

    @commands.command(aliases=['sixtosas'])
    async def pocado_add(self, ctx):
        if ctx.message.author.id == 655116194562703390:
            role = discord.utils.get(ctx.message.guild.roles, name = "pocaditos")
            member = ctx.message.mentions[0]
            await member.add_roles(role)

    @commands.command(aliases=['rer'])
    async def pocado_delete(self, ctx):
        if ctx.message.author.id == 655116194562703390:
            role = discord.utils.get(ctx.message.guild.roles, name = "pocaditos")
            member = ctx.message.mentions[0]
            await member.remove_roles(role)

    @commands.command(aliases=['ficha'])
    async def summon_bot(self, ctx):
        member = ctx.message.author
        role = discord.utils.get(ctx.message.guild.roles, name = "ficha")
        channel = discord.utils.get(ctx.guild.channels, name="general")
        await member.add_roles(role)
        await channel.send(f'{member.mention} se cree ficha')

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleManagement(bot))
