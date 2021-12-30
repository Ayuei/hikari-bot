from typing import Union

import discord
import toml
from discord.ext import commands
# from decryption library
from database import Database

config = toml.load(open("config.toml", "r"))
bot = commands.Bot(command_prefix='+')
database = Database()
database.load()


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def add_reminder(ctx: Union[discord.ext.commands.context, discord.Message]):
    if ctx.author == 129310931312:
        pass


@bot.command()
async def add_loot(ctx: Union[discord.ext.commands.context, discord.Message]):
    pass


@bot.command()
async def get_loot(ctx: Union[discord.ext.commands.context, discord.Message]):
    pass


bot.run(config.get("api_key"))
