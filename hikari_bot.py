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
    bot.add_cog(cog(bot, database))


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
async def add_reminder(ctx, timestamp):
    reminder = database.get(ctx).add_reminder(ctx, timestamp).get_countdown()

    msg = None
    if reminder:
        msg = await ctx.reply(f"Countdown until raid {reminder.days} days, {int(reminder.total_seconds()%(24*3600)//3600)} "
                              f"hours")
    else:
        msg = await ctx.reply(f"Reminder already added!")

    await asyncio.sleep(5)
    await msg.delete()

@bot.command()
@sent_from_guild()
@commands.has_role("Raid Leader")
async def remove_reminder(ctx, timestamp):
    database.get(ctx).remove_reminder(timestamp)

    msg = await ctx.reply(f"Removed reminder: {timestamp}")
    await asyncio.sleep(5)
    await msg.delete()


@add_reminder.error
async def add_reminder_error(ctx, error):
    msg = None
    if "get_countdown" in error.args[0]:
        msg = await ctx.reply("You've already added this reminder!")
    else:
        msg = await ctx.reply('E.g. Usage: +add_reminder "Mon 16:00 GMT+8". Duplicates aren\'t added.')

    await asyncio.sleep(5)
    await msg.delete()


@bot.command()
@sent_from_guild()
async def get_reminders(ctx):
    reminders = database.get(ctx).get_reminders()
    embed = discord.Embed(title="Reminders n Countdown")

    for key in reminders:
        print(key)
        countdown = reminders[key].get_countdown()
        print(countdown)
        days = countdown.days
        hours = int((countdown.total_seconds() - days * (24*3600)) // 3600)
        minutes = int(((countdown.total_seconds() - days * (24*3600)) % 3600) // 60)
        embed.add_field(name=key, value=f"{hours} hours, {minutes} minutes", inline=True)

    await ctx.send(embed=embed)


# +addloot @member [head/chest/glove/boot(s)/earrings/necklace/bracelet(s)/ring
@bot.command()
@sent_from_guild()
@commands.has_role("Raid Leader")
async def add_loot(ctx, member: discord.User, item: str):
    database.get(ctx).get_member(member.id).obtained_loot.add_gear(item)

    msg = await ctx.reply(f"*Added {item} loot for {member.display_name}*")
    await asyncio.sleep(5)
    await msg.delete()

@bot.command()
@sent_from_guild()
@commands.has_role("Raid Leader")
async def remove_loot(ctx, member: discord.User, item: str):
    database.get(ctx).get_member(member.id).obtained_loot.remove_gear(item)

    msg = await ctx.reply(f"*Removed {item} loot for {member.display_name}*")
    await asyncio.sleep(5)
    await msg.delete()


# +getloot @member
# +Print out loot
@bot.command()
@sent_from_guild()
async def get_loot(ctx, member: discord.Member):
    gear = database.get(ctx).get_member(member.id).obtained_loot.to_dict()

    embed = discord.Embed(title="Loot Goblin Status", description="Panda Lewds 1-4")
    embed.set_author(name=member.display_name)
    embed.set_thumbnail(url="https://c.tenor.com/c1VeLRFcWJAAAAAd/adventuretime-dungeon.gif")
    embed.add_field(name="Head", value=gear['head'], inline=True)
    embed.add_field(name="Earrings", value=gear['earring'], inline=True)
    embed.add_field(name="᲼᲼᲼", value="᲼᲼᲼", inline=True)
    embed.add_field(name="Chest", value=gear['chest'], inline=True)
    embed.add_field(name="Necklace", value=gear['necklace'], inline=True)
    embed.add_field(name="᲼᲼᲼", value="᲼᲼᲼", inline=True)
    embed.add_field(name="Gloves", value=gear['glove'], inline=True)
    embed.add_field(name="Bracelets", value=gear['bracelet'], inline=True)
    embed.add_field(name="᲼᲼᲼", value="᲼᲼᲼", inline=True)
    embed.add_field(name="Pants", value=gear['pant'], inline=True)
    embed.add_field(name="Ring", value=gear['ring'], inline=True)
    embed.add_field(name="᲼᲼᲼", value="᲼᲼᲼", inline=True)
    embed.add_field(name="Boots", value=gear['boot'], inline=True)
    embed.add_field(name="Total Received", value=sum(gear.values()), inline=False)
    embed.set_footer(text="Lewd Goblins Beware")
    await ctx.send(embed=embed)


@add_loot.error
async def raid_leaders_only(ctx, error):
    print(error)
    msg = await ctx.send("Only Raid Leaders can use this command!")
    await asyncio.sleep(5)
    await msg.delete()


bot.run(config['secrets']["api_key"])
