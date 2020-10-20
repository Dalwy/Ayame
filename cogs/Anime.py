import asyncio
import discord
from discord.ext import commands
import math
import sqlite3
import aiohttp
from bs4 import BeautifulSoup


class AnimeNights(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.db = sqlite3.connect('Member.sqlite')
        # self.curr = self.db.cursor()

    def addToDB(self, user, name, guild):
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        cursor.execute(
            "SELECT User_id, ShowName, guild_id FROM Anime WHERE User_id = ? AND ShowName = ? AND guild_id = ?",
            (user, name, guild,))
        result = cursor.fetchone()
        if result is None:
            return True
        else:
            return False

    @commands.command(aliases=["AS", "as", "add"])
    async def addShow(self, ctx, *, input):
        """Aliases: AS, as, add. Example: Ayame as Sword Art Online"""

        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        """How to use: a!addShow <Anime Name>
            or a!AS <Anime Name>"""
        global em, name
        async with aiohttp.ClientSession() as session:
            url = 'https://myanimelist.net/search/all'
            params = {'q': input}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}

            async with session.get(url, params=params, headers=headers) as resp:
                text = await resp.text()
                soup = BeautifulSoup(text, 'html.parser')
                a = soup.find('a', {'class': 'hoverinfo_trigger fw-b fl-l'})
                PageLink = a['href']

                async with session.get(PageLink, headers=headers) as resp2:
                    text = await resp2.text()
                    soup = BeautifulSoup(text, 'html.parser')
                    ShowName = soup.find('span', itemprop='name').text
                    ShowImage = soup.find('img', itemprop='image')
                    ShowImageLink = ShowImage['data-src']
                    ShowRating = soup.find('span', itemprop='ratingValue').text
                    UserCount = soup.find('span', itemprop='ratingCount').text
                    # ShowImage['src'] for link to image
        success = self.addToDB(ctx.author.id, ShowName, ctx.author.guild.id)
        if success:
            cursor.execute("INSERT INTO Anime(User_id, ShowName, ShowLink, Rating, UserCount, guild_id) "
                           "VALUES(?,?,?,?,?,?)", (ctx.author.id, ShowName, PageLink, ShowRating, UserCount,
                                                   ctx.author.guild.id))
            db.commit()
            em = discord.Embed(title="Added Show", description="Rating: " + str(ShowRating) + ", By: " + str(UserCount)
                               + " Users")
            em.set_image(url=ShowImageLink)
            em.set_author(name=ShowName, url=PageLink, icon_url=''.join(ShowImageLink))
            em.add_field(name="Show\n", value=ShowName)
            await ctx.send(embed=em)
        elif not success:
            cursor.execute("SELECT * FROM Anime")
            result = cursor.fetchone()
            em = discord.Embed(title="Database Results for: " + str(ctx.author), description="Rating: " + str(result[3]) + " By: " +
                                                                     str(result[4]) + " Users")
            em.set_image(url=ShowImageLink)
            em.set_author(name=ShowName, url=PageLink, icon_url=''.join(ShowImageLink))
            em.add_field(name="Show\n", value=ShowName)
            await ctx.send(embed=em)
    @commands.command()
    async def search(self, ctx, *, input):
        """Aliases: None. Example: Ayame search Sword Art Online"""
        em = discord.Embed(title="Search Results", description="Show you're looking for " + input)
        async with aiohttp.ClientSession() as session:
            url = 'https://myanimelist.net/anime.php?'
            params = {'q': input}
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}

            async with session.get(url, params=params, headers=headers) as resp:
                text = await resp.text()
                soup = BeautifulSoup(text, 'html.parser')
                a = soup.findAll('a', {'class': 'hoverinfo_trigger fw-b fl-l'})
                for number, name in enumerate(a[:10], 1):
                    x = name.find('strong').get_text()
                    em.add_field(name=str(number), value=x + '\n')
        await ctx.send(embed=em)

    @commands.command()
    async def shows(self, ctx, member: discord.Member = None):
        """Aliases: None. Example: Ayame shows"""
        db = sqlite3.connect('Main.sqlite')
        cursor = db.cursor()
        if not member:
            member = ctx.message.author
        if ctx.author == member:
            pages = []
            cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ?"
                           "AND guild_id = ?", (ctx.author.id, ctx.author.guild.id,))
            result = cursor.fetchall()
            cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ? "
                           "AND guild_id = ? ", (ctx.author.id, ctx.author.guild.id,))
            pagecount = len(cursor.fetchall())
            numberofpages = math.floor(pagecount / 10)
            y = [x for l in result for x in l]
            # for x in range(0, len(result), 10):
            page1 = discord.Embed(title="List of Shows For: " + str(ctx.author), description='\n'.join(y[:10]))
            pages.append(page1)
            i = 0
            if len(pages) == 0:
                await ctx.send(str(ctx.author) + " Has not added any shows to their list yet.")
                return
            message = await ctx.send(embed=pages[i].set_footer(text=str(i) + " of: " + str(numberofpages)))
            await message.add_reaction('\u25c0')
            await message.add_reaction('\u25b6')
            while True:

                def check(reaction, user):
                    if reaction.message.id != message.id:
                        return False
                    if user != ctx.message.author:
                        return False
                    return True
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                    if user != self.bot.user:
                        await message.remove_reaction(reaction, user)
                except asyncio.TimeoutError:
                    return await message.clear_reactions()
                else:
                    if str(reaction.emoji) == '\u25c0':
                        if i > 0:
                            i -= 1
                            # result = cursor.fetchmany(10)
                            page1 = discord.Embed(title="List of Shows For: " + str(ctx.author),
                                                  description='\n'.join([x[0] for x in result][:10]))
                            # i -= 1
                            pages.append(page1)

                            # page1.set_footer(text=str(i) + " of: " + str(numberofpages))
                            await message.edit(embed=pages[i].set_footer(text=str(i) + " of: " + str(numberofpages)))
                    if str(reaction.emoji) == '\u25b6':
                        if i < numberofpages:
                            i += 1
                            # cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ? "
                            #                "AND guild_id = ? ", (ctx.author.id, ctx.author.guild.id,))
                            # result = cursor.fetchmany(10)
                            # print(result)
                            # y = [x for l in result for x in l]
                            # for x in range(0, len(result), 5):
                            em = discord.Embed(title="List of Shows For: " + str(ctx.author),
                                               description='\n'.join([x[0] for x in result][10:]))
                            # em.set_footer(text=str(i) + " of: " + str(numberofpages))
                            pages.append(em)
                            # print(pages)
                            await message.edit(embed=pages[i].set_footer(text=str(i) + " of: " + str(numberofpages)))

        else:
            pages = []
            cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ?"
                           "AND guild_id = ?", (member.id, ctx.author.guild.id,))
            result = cursor.fetchall()
            cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ? "
                           "AND guild_id = ? ", (member.id, ctx.author.guild.id,))
            pagecount = len(cursor.fetchall())
            # print(pagecount)
            numberofpages = math.floor(pagecount / 10)
            y = [x for l in result for x in l]
            for x in range(0, len(result), 10):
                page1 = discord.Embed(title="List of Shows For: " + str(member), description='\n'.join(y[x:x + 10]))
                pages.append(page1)
            i = 0
            if len(pages) == 0:
                await ctx.send(str(member) + " Has not added any shows to their list yet.")
                return
            message = await ctx.send(embed=pages[i].set_footer(text=str(i) + " of: " + str(numberofpages)))
            await message.add_reaction('\u25c0')
            await message.add_reaction('\u25b6')
            if ctx.author != member:
                while True:
                    def check(reaction, user):
                        if reaction.message.id != message.id:
                            return False
                        if user != ctx.message.author:
                            return False
                        return True

                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                        if user != self.bot.user:
                            await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:
                        return await message.clear_reactions()
                    if str(reaction.emoji) == '\u25c0':
                        if i > 0:
                            i -= 1
                            page1 = discord.Embed(title="List of Shows For: " + str(member),
                                                  description='\n'.join([x[0] for x in result][:10]))
                            pages.append(page1)
                            await message.edit(embed=pages[i].set_footer(text=str(i) + " of: " + str(numberofpages)))
                    if str(reaction.emoji) == '\u25b6':
                        if i < numberofpages:
                            i += 1
                            em = discord.Embed(title="List of Shows For: " + str(member),
                                               description='\n'.join([x[0] for x in result][10:]))
                            pages.append(em)
                            await message.edit(embed=pages[i].set_footer(text=str(i) + " of: " + str(numberofpages)))



def setup(bot):
    bot.add_cog(AnimeNights(bot))