import os
import asyncio
import discord
from discord.ext import commands

token = "MTE2MzA1MzU0MzkwNTgzMzAwMA.GqxWv9.AbPCBmIL5EBWlpfZDB9VLsWtR-UFsK0bYLxz18"
prefix = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)


# create a simple example of COG in my bot

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)


@bot.group()
async def math(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Неверная подкоманда. Доступные подкоманды: add, sub, mul, div')


@math.command()
async def add(ctx, first: int, second: int):
    await ctx.send(first + second)


@math.command()
async def sub(ctx, first: int, second: int):
    await ctx.send(first - second)


@math.command()
async def mul(ctx, first: int, second: int):
    await ctx.send(first * second)


@math.command()
async def div(ctx, first: int, second: int):
    await ctx.send(first / second)


@bot.command()
async def time_joined(ctx, member: discord.Member):
    await ctx.send(f"{member.display_name} присоединился к серверу {member.joined_at}")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            "Один или несколько обязательных аргументов отсутствуют. Пожалуйста, укажите все необходимые аргументы.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Неверный формат аргумента. Пожалуйста, введите корректное значение.")


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await bot.start(token)


asyncio.run(main())


