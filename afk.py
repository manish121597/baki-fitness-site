import discord

from discord.ext import commands

import datetime

# Dictionary to store AFK users and their AFK times

afk_users = {}

@commands.command()

@commands.cooldown(1, 5, commands.BucketType.user)

async def afk(ctx, *, message: str = "I am currently AFK."):

    # Mark the user as AFK with the provided message

    afk_users[ctx.author.id] = {'time': datetime.datetime.utcnow(), 'message': message}

    await ctx.reply("**__You have been marked as AFK__**")

@commands.command()

@commands.cooldown(1, 5, commands.BucketType.user)

async def removeafk(ctx):

    if ctx.author.id in afk_users:

        del afk_users[ctx.author.id]

        await ctx.reply("**__Your AFK has been removed.__**")

    else:

        await ctx.reply("**__You are not AFK.__**")

@commands.Cog.listener()

async def on_message(message):

    # Ignore messages from bots

    if message.author.bot:

        return

    # Check if someone mentioned an AFK user

    if message.mentions:

        for user in message.mentions:

            if user.id in afk_users and user.id != message.author.id:

                afk_message = afk_users[user.id]['message']

                await message.channel.send(f"**{user.display_name} is AFK.**\n Message: {afk_message}")

def setup(bot):

    bot.add_command(afk)

    bot.add_command(removeafk)

    bot.add_listener(on_message)

