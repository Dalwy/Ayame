import json
import asyncio
import discord
from discord.ext import commands
import aiohttp
import requests
import discord.abc
import sqlite3


def is_owner():
    return commands.is_owner()


class Moderation(commands.Cog):
    """Moderation"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["k", "kick"])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def Kick(self, ctx, member: discord.Member, *, reason=''):
        """Aliases: 'k', 'kick'. Example: Ayame kick @user#0001 Being Disrespectful"""
        if commands.is_owner():
            return await ctx.send("Cant do that")
        else:
            db = sqlite3.connect('Main.sqlite')
            cursor = db.cursor()
            cursor.execute("SELECT user_id, KickedOrBanned, guild_id FROM Moderation WHERE user_id = ? AND guild_id = ?"
                           , (member.id, member.guild.id,))
            print(member.guild.id)
            print(member.id)
            result = cursor.fetchone()
            if result is None:
                sql = (f"INSERT OR IGNORE INTO Moderation (user_id, KickedOrBanned, reason, Staff, guild_id) "
                       f"VALUES (?, ?, ?, ?, ?)")
                val = (member.id, "Kicked", reason, ctx.author.id, member.guild.id)
                cursor.execute(sql, val)
                result = cursor.fetchone()
                print(result)
                db.commit()
            embed = discord.Embed(title="Kicked", description="Reason: " + str(reason))
            embed.add_field(name='User Kicked: ', value=str(member.mention))
            embed.add_field(name='Kicked by: ', value=str(ctx.author.mention))
            embed.set_footer(text=str(member) + ' UID: ' + str(member.id))
            await ctx.send(embed=embed)
            await member.kick(reason=reason)
            msg = ctx.message
            await msg.delete()

    @commands.command(aliases=["b", "ban"])
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def Ban(self, ctx, member: discord.Member, *, reason=''):
        """Aliases: 'b', 'ban'. Example: Ayame ban @user#0001 Being Disrespectful"""
        if commands.is_owner():
            return await ctx.send("Cant do that")
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, KickedOrBanned, guild_id FROM Moderation WHERE user_id = ? AND guild_id = ?",
            (member.id, member.guild.id,))
        print(member.guild.id)
        print(member.id)
        result = cursor.fetchone()
        if result is None:
            sql = (
                f"INSERT OR IGNORE INTO Moderation (user_id, KickedOrBanned, reason, Staff, guild_id) "
                f"VALUES (?, ?, ?, ?, ?)")
            val = (member.id, "Banned", reason, ctx.author.id, member.guild.id)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            print(result)
            db.commit()
        user = member
        embed = discord.Embed(title="Banned", description="Reason: " + str(reason))
        embed.add_field(name='User Banned: ', value=str(member.mention))
        embed.add_field(name='Banned by: ', value=str(ctx.author.mention))
        embed.set_footer(text=str(user) + ' UID: ' + str(user.id))
        await ctx.send(embed=embed)
        await member.ban(reason=reason)
        msg = ctx.message
        await msg.delete()

    # @commands.command()
    # async def Suggestion(self, ctx, member: discord.Member, songName, *, artistName):
    #     userID = str(member.id)
    #     with(open("JSON_Files/Suggestions.json", 'r')) as f:
    #         suggestions = json.load(f)
    #     if userID not in suggestions:
    #         suggestions[userID] = {}
    #         suggestions[userID]['Discord Name: '] = str(member.display_name)
    #         suggestions[userID]['Song: '] = songName
    #         suggestions[userID]['Artist: '] = artistName
    #         await ctx.send('Added successfully')
    #     elif userID in suggestions:
    #         await ctx.send('You have already added a song suggestion for this week!')
    #     with(open("JSON_Files/Suggestions.json", 'w')) as f:
    #         json.dump(suggestions, f, indent=3)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def HB(self, ctx):
        astroSigns = ["aquarius", "pisces", "aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio",
                      "sagittarius", "capricorn"]
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            for s in astroSigns:
                async with aiohttp.ClientSession() as session:
                    signResp = requests.post('https://aztro.sameerkumar.website/?sign='+s+'&day=today')
                    data = json.loads(signResp.text)
                    signEmbed = discord.Embed(description=data['description'])
                    signEmbed.set_author(name=s.title() + ' - ' + data['current_date'],
                                         icon_url='https://www.astrology.com/images-US/'+s+'.jpg')
                    await ctx.send(embed=signEmbed)
            await asyncio.sleep(86400)



    # @commands.command()
    # @commands.has_permissions(administrator=True)
    # @commands.is_owner()
    # async def SS(self, ctx, member: discord.Member):
    #     await ctx.send("You will Receive the suggestions file in a week!")
    #     await self.bot.wait_until_ready()
    #     while not self.bot.is_closed():
    #         x = discord.File('JSON_Files/Suggestions.json', filename='Suggestions.json')
    #         await member.send("Heres the suggestions for the week!", file=x)
    #         await asyncio.sleep(806400)

    @commands.command(aliases=["w", "warn"])
    @commands.has_permissions(kick_members=True)
    async def Warn(self, ctx, member: discord.Member, *, reason=''):
        """Aliases: 'w', 'warn'. Example: Ayame warn @user#0001 Being Disrespectful"""
        if ctx.author == self.bot:
            await ctx.send("bitch wtf are you doing")

        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, Warnings, guild_id FROM Moderation WHERE user_id = ? AND guild_id = ?",
            (member.id, member.guild.id,))
        result = cursor.fetchone()
        if result is None:
            sql = (
                f"INSERT OR IGNORE INTO Moderation (user_id, Warnings, reason, Staff, guild_id) "
                f"VALUES (?, ?, ?, ?, ?)")
            val = (member.id, "Warned", reason, ctx.author.id, member.guild.id)
            cursor.execute(sql, val)
            result = cursor.fetchone()
            print(result)
            db.commit()
        embed = discord.Embed(title="Warning", description="Reason: " + str(reason))
        embed.add_field(name='User Warned: ', value=str(member.mention))
        embed.add_field(name='Warned by: ', value=str(ctx.author.mention))
        embed.set_footer(text=str(member) + ' UID: ' + str(member.id))
        await ctx.send(embed=embed)
        msg = ctx.message
        await msg.delete()




        # with open("JSON_Files/warnings.json", 'r') as f:
        #     warned = json.load(f)
        #
        # warnedid = str(member.id)
        # name = str(member.display_name)
        # print(warnedid)
        # if warnedid not in warned:
        #     warned[warnedid] ={}
        #     warned[warnedid]['Disc Name'] = name
        #     warned[warnedid]['Warned'] = 1
        #     warned[warnedid]['Reason'] = reason
        #     await member.add_roles(role, reason=reason)
        #     embed.add_field(name='Muted', value='Time: 10 Minutes')
        #     await ctx.send(embed=embed)
        #     with open('JSON_Files/warnings.json', 'w') as f:
        #         json.dump(warned, f, indent=3)
        #     await asyncio.sleep(600)
        # elif warnedid in warned:
        #     warned[warnedid]['Warned'] += 1
        #     warned[warnedid]['Reason2'] = reason
        #     warned[warnedid]['Reason3'] = reason
        #     if warned[warnedid]['Warned'] == 2:
        #         await member.add_roles(role, reason=reason)
        #         embed.add_field(name='Muted', value='Time: 3 Days')
        #         await ctx.send(embed=embed)
        #         with open('JSON_Files/warnings.json', 'w') as f:
        #             json.dump(warned, f, indent=3)
        #         await asyncio.sleep(259200)
        #     if warned[warnedid]['Warned'] == 3:
        #         await member.add_roles(role, reason=reason)
        #         embed.add_field(name='Muted', value='Time: 1 Week')
        #         await ctx.send(embed=embed)
        #         with open('JSON_Files/warnings.json', 'w') as f:
        #             json.dump(warned, f, indent=3)
        #         await asyncio.sleep(604800)
        #     if warned[warnedid]['Warned'] == 4:
        #         await member.ban(reason=reason)
        #         await ctx.send("User Banned, Begone Thot!")
        # await member.remove_roles(role, reason='Times up')
        #
        # # with open('JSON_Files/warnings.json', 'w') as f:
        # #     json.dump(warned, f, indent=3)

    @commands.command(aliases=["ws", "warnings"])
    @commands.has_permissions(kick_members=True)
    async def Warnings(self, ctx, member: discord.Member, *, reason=''):
        """Aliases: 'ws', 'warnings'. Example: Ayame warn @user#0001 Being Disrespectful"""
        if commands.is_owner():
            return await ctx.send("Cant do that")

        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id, Warnings, guild_id FROM Moderation WHERE user_id = ? AND guild_id = ?",
            (member.id, member.guild.id,))
        result = cursor.fetchone()
        if result is None:
            await ctx.send(member.mention + "has no warnings")
        else:

            embed = discord.Embed(title="Warnings", description="Reasons: " + str(reason))
            embed.add_field(name='User Warned: ', value=str(member.mention))
            embed.add_field(name='Warned by: ', value=str(ctx.author.mention))
            embed.set_footer(text=str(member) + ' UID: ' + str(member.id))
def setup(bot):
    bot.add_cog(Moderation(bot))
