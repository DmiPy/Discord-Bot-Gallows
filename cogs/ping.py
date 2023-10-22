import discord
from discord.ext import commands


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send('Pong!')

    @commands.command()
    async def pong(self, ctx):
        """Ping"""
        await ctx.send("Ping!")

async def setup(bot):
    await bot.add_cog(Ping(bot))
