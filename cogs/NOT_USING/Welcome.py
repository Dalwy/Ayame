import discord
from discord import utils
from discord.ext import commands
from sqlite3 import connect
import sqlite3
import json

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, Member):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        if Member.guild.id is None:
            cursor.execute("INSERT INTO Members (User_Name, guild_id) VALUES (?, ?)",
                           (Member.id, Member.display_name, Member.guild.id,))
            db.commit()
        else:
            cursor.execute("INSERT INTO Members (user_id, user_name, guild_id) VALUES (?, ?, ?)",
                           (Member.id, Member.display_name, Member.guild.id,))
            db.commit()


    @commands.Cog.listener()
    async def on_member_remove(self, Member):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        if Member is not self.bot:
            cursor.execute("DELETE FROM Members WHERE User_id = ? AND guild_id = ?", (Member.id, Member.guild.id,))
            db.commit()



def setup(bot):
    bot.add_cog(Welcome(bot))
