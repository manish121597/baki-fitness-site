import discord

from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.mute_role = None

    @commands.command()

    @commands.has_permissions(kick_members=True)

    async def kick(self, ctx, member: discord.Member, *, reason=None):

        await member.kick(reason=reason)

        await ctx.send(f"**{member}** has been kicked. Reason: {reason}")

    @commands.command()

    @commands.has_permissions(ban_members=True)

    async def ban(self, ctx, member: discord.Member, *, reason=None):

        await member.ban(reason=reason)

        await ctx.send(f"**{member}** has been banned. Reason: {reason}")

    @commands.command()

    @commands.has_permissions(ban_members=True)

    async def unban(self, ctx, *, member_name):

        banned_users = await ctx.guild.bans()

        for ban_entry in banned_users:

            user = ban_entry.user

            if (user.name + '#' + user.discriminator) == member_name:

                await ctx.guild.unban(user)

                await ctx.send(f"**{user}** has been unbanned.")

                return

        await ctx.send(f"**{member_name}** not found in ban list.")

    @commands.command()

    @commands.has_permissions(manage_roles=True)

    async def muterole(self, ctx, role: discord.Role):

        self.mute_role = role

        for channel in ctx.guild.channels:

            await channel.set_permissions(role, send_messages=False)

        await ctx.send(f"Mute role set to **{role.name}** and permissions updated for all channels.")

    @commands.command()

    @commands.has_permissions(manage_roles=True)

    async def mute(self, ctx, member: discord.Member, *, reason=None):

        if self.mute_role is None:

            await ctx.send("Mute role not set up. Use `+muterole @role` to set up the mute role.")

            return

        await member.add_roles(self.mute_role, reason=reason)

        await ctx.send(f"**{member}** has been muted. Reason: {reason}")

    @commands.command()

    @commands.has_permissions(manage_roles=True)

    async def unmute(self, ctx, member: discord.Member):

        if self.mute_role is None:

            await ctx.send("Mute role not set up. Use `+muterole @role` to set up the mute role.")

            return

        if self.mute_role in member.roles:

            await member.remove_roles(self.mute_role)

            await ctx.send(f"**{member}** has been unmuted.")

        else:

            await ctx.send(f"**{member}** is not muted.")

    @commands.command()

    @commands.has_permissions(manage_channels=True)

    async def lock(self, ctx):

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

        await ctx.send(f"**{ctx.channel}** has been locked.")

    @commands.command()

    @commands.has_permissions(manage_channels=True)

    async def unlock(self, ctx):

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

        await ctx.send(f"**{ctx.channel}** has been unlocked.")

    @commands.command()

    @commands.has_permissions(manage_channels=True)

    async def hide(self, ctx):

        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)

        await ctx.send(f"**{ctx.channel}** has been hidden.")

    @commands.command()

    @commands.has_permissions(manage_channels=True)

    async def unhide(self, ctx):

        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=True)

        await ctx.send(f"**{ctx.channel}** has been unhidden.")

    @commands.command()

    @commands.has_permissions(manage_nicknames=True)

    async def nick(self, ctx, member: discord.Member, *, nickname: str = None):

        await member.edit(nick=nickname)

        await ctx.send(f"**{member}'s** nickname has been changed to **{nickname}**")

    @commands.command()

    @commands.has_permissions(manage_roles=True)

    async def addrole(self, ctx, member: discord.Member, *, role: discord.Role):

        await member.add_roles(role)

        await ctx.send(f"**{role}** has been added to **{member}**")

    @commands.command()

    @commands.has_permissions(manage_roles=True)

    async def removerole(self, ctx, member: discord.Member, *, role: discord.Role):

        await member.remove_roles(role)

        await ctx.send(f"**{role}** has been removed from **{member}**")

    @commands.command()

    async def mod_help(self, ctx):

        help_message = (

            "# __S3LFB0Ƭ__\n"

            "**</>** __**MODERATION CMD. HELP**__\n\n"

            "`-` **KICK** : `+kick <user> [reason]`\n"

            "`-` **BAN** : `+ban <user> [reason]`\n"

            "`-` **UNBAN** : `+unban <user#discriminator>`\n"

            "`-` **MUTE ROLE SETUP** : `+muterole @role`\n"

            "`-` **MUTE** : `+mute <user> [reason]`\n"

            "`-` **UNMUTE** : `+unmute <user>`\n"

            "`-` **LOCK** : `+lock`\n"

            "`-` **UNLOCK** : `+unlock`\n"

            "`-` **HIDE** : `+hide`\n"

            "`-` **UNHIDE** : `+unhide`\n"

            "`-` **NICKNAME** : `+nick <user> <new nickname>`\n"

            "`-` **ADD ROLE** : `+addrole <user> @role`\n"

            "`-` **REMOVE ROLE** : `+removerole <user> @role`\n\n"

            "`-` **ASKED BY** : `spythen`"

        )

        await ctx.send(help_message)

def setup(bot):

    bot.add_cog(Moderation(bot))

