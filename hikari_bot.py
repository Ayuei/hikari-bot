import asyncio
from typing import Union

import discord
import toml
from discord.ext import commands
# from decryption library
from database import Database
from cogs import cogs

config = toml.load(open("config.toml", "r"))
bot = commands.Bot(command_prefix='+')
database = Database()
database.load()

for cog in cogs:
    bot.add_cog(cog(bot, cog))


def parse(msg: discord.Message):
    parts = msg.content.split()


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


# def is_raid_leader():
#    async def predicate(ctx: Union[discord.ext.commands.context, discord.Message]):
#        return "Raid Leader" in ctx.author.roles
#    return commands.check(predicate)

def sent_from_guild():
    async def predicate(ctx):
        return ctx.guild

    return commands.check(predicate)


# +addreminder "%A:%H:%M GMT+8
@bot.command()
@sent_from_guild()
@commands.has_role("Raid Leader")
async def add_reminder(ctx: Union[discord.ext.commands.context, discord.Message], timestamp):
    channel = ctx.channel
    database.raids.get(channel).add_reminder(ctx, timestamp)

    await ctx.reply(f"Countdown until raid {database.raids.get(channel).reminders[-1].countdown} seconds")


# +addloot @member [head/chest/glove/boot(s)/earrings/necklace/bracelet(s)/ring
@bot.command()
@sent_from_guild()
@commands.has_role("Raid Leader")
async def add_loot(ctx: Union[discord.ext.commands.context, discord.Message], member: discord.User, item: str):
    database.raids.get(ctx.channel).get_member(member.id).obtained_loot.add_gear(item)

    msg = await ctx.reply(f"Added loot!")
    await asyncio.sleep(10)
    await msg.delete()


# +getloot @member
# +Print out loot
@bot.command()
@sent_from_guild()
@commands.has_role("Raid Leader")
async def get_loot(ctx: Union[discord.ext.commands.context, discord.Message], member: discord.Member):
    gear = database.raids.get(ctx.channel).get_member(member.id).obtained_loot.to_dict()

    await ctx.reply(f"Member has {gear}")


bot.run(config.get("api_key"))
