import discord
from discord.ext import commands
import sqlite3


class Karaoke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        author = ctx.message.author
        if author != ctx.author:
            await ctx.send("Cannot add other people!")
            return
        cursor.execute("SELECT User_id FROM Karaoke")
        result = cursor.fetchall()
        if author.id not in result:
            cursor.execute("INSERT OR IGNORE INTO Karaoke (User_id, DisplayName) VALUES (?, ?)",
                           (author.id, str(author),))
            db.commit()
        await ctx.send("You have been added to queue")
        # elif author.id not in result:
        #     cursor.execute("INSERT INTO Karaoke (User_id, DisplayName) VALUES (?, ?)",
        #                    (author.id, author,))
        #     db.commit()


    @commands.command()
    async def queue(self, ctx):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        em = discord.Embed(title="Queue for Karaoke", description="Current Queue")
        cursor.execute("SELECT * FROM Karaoke")
        result = cursor.fetchall()
        for name in result:
            em.add_field(name="Name", value=name[1])
        await ctx.send(embed=em)

    @commands.command()
    async def leave(self, ctx):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        author = ctx.message.author
        if author != ctx.author:
            await ctx.send("Cannot add other people!")
            return
        cursor.execute("DELETE FROM Karaoke WHERE User_id = ?", (author.id,))
        db.commit()
        await ctx.send("You have been removed from the queue")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def removeall(self, ctx):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        cursor.execute("DELETE FROM Karaoke")
        db.commit()
        await ctx.send("You have removed everyone from the queue")

def setup(bot):
    bot.add_cog(Karaoke(bot))
