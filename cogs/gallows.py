import time
import discord
from discord.ext import commands
import random

game_words = ["Пидор", "Товар", "Кайсар", "Пинксквад", "Piggers", "Котик", "Украина", "Шмалькальден", "ГОЙДА"]

HANGMAN = (
    """
------
|    |
|
|
|
|
|
|
|
--------
""",
    """
------
|    |
|    O  |
|
|
|
|
|
|
--------
""",
    """
------
|    |
|    O
|   -+-
|
|
|
|
|
--------
""",
    """
------
|    |
|    O
|  /-+-/
|
|
|
|
|
--------
""",
    """
------
|    |
|    O
|  /-+-/
|    |
|
|
|
|
--------
""",
    """
------
|    |
|    O
|  /-+-/
|    |
|    |
|   |
|   |
|
--------
""",
    """
------
|    |
|    O
|  /-+-/
|    |
|    |
|   | |
|   | |
|
--------
"""
)


class Gallows(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_word = random.choice(game_words).upper()
        self.game_stage = 0
        self.USED_LETTERS = set()
        self.so_far = ["-"] * len(self.game_word)
        self.if_piggers_notified = False

    async def reset_game(self):
        self.USED_LETTERS = set()
        self.game_word = random.choice(game_words).upper()
        self.game_stage = 0
        self.USED_LETTERS = set()
        self.so_far = ["-"] * len(self.game_word)
        self.if_piggers_notified = False

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Вы не указали букву. Пожалуйста, укажите букву.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Неверный формат аргумента. Пожалуйста, введите корректное значение.")

    @commands.command()
    async def start_gallows(self, ctx):
        """Виселица"""
        await ctx.send("\t\tДобро пожаловать в игру 'Виселица'!")
        await ctx.send(
            """
            Сейчас я загадаю слово, а вы  должны будете по буквам его угадать.
            Вы будете предлагать по одной букве, если эта буква есть в моем слове, то
            я открою вам ее положение в слове. Если же нет, то я буду дорисовывать человечка
            на виселице.
            Игра будет длиться до тех пор, пока вы не отгадаете слово, либо пока человечек не
            полностью повешен.
            Итак, осталось, только пожелать вам удачи, ведь от вас зависит судьба, несчастного
            нарисованного человечка!

            Угадывать вы можете с помощью команды !guess <буква>
            Начинать новую игру вы можете с помощью команды !restart_game
            """
        )
        time.sleep(5)
        await ctx.send(HANGMAN[self.game_stage])
        await ctx.send(f"Новая игра началась! Слово состоит из {len(self.game_word)} букв:\n{' '.join(self.so_far)}")

    @commands.command()
    async def guess(self, ctx, letter: str):
        letter = letter.upper()

        piggers_notification = "Внимание! Слово написано на латинице!"
        if self.game_word == "PIGGERS" and not self.if_piggers_notified:
            self.if_piggers_notified = True
            await ctx.send(piggers_notification)

        if letter in self.USED_LETTERS:
            await ctx.send("Вы уже использовали эту букву")
            return

        self.USED_LETTERS.add(letter)

        if letter in self.game_word:
            indices = [index for index, ltr in enumerate(self.game_word) if ltr == letter]
            for index in indices:
                self.so_far[index] = letter
            await ctx.send(' '.join(self.so_far))
            await ctx.send("Вы угадали букву.")
        else:
            self.game_stage += 1
            await ctx.send(HANGMAN[self.game_stage])
            await ctx.send("Вы не угадали букву. Попробуйте еще раз!")
            if self.game_stage == 6:
                await ctx.send(f"Вы проиграли! Загаданное слово: {self.game_word}")
                self.USED_LETTERS = set()
            else:
                await ctx.send(f"Осталось {6 - self.game_stage} попыток.")

        if all(letter in self.USED_LETTERS for letter in self.game_word):
            await ctx.send("Вы выиграли!")
            await self.reset_game()

    @commands.command()
    async def restart_game(self, ctx):
        await self.reset_game()
        await ctx.send(HANGMAN[self.game_stage])
        await ctx.send(f"Новая игра началась! Слово состоит из {len(self.game_word)} букв:\n{' '.join(self.so_far)}")

    @commands.command()
    async def give_up(self, ctx):
        await ctx.send(f"*бать ты Лох, бро!: Вот твое несчастное слово: {self.game_word}.\n А человеку то...")
        await ctx.send(HANGMAN[6])
        await self.reset_game()


async def setup(bot):
    await bot.add_cog(Gallows(bot))
