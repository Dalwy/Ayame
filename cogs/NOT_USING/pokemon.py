# import asyncio
# from typing import Any, Union
#
# import discord
# from discord.ext import menus
# from discord.ext import commands
# import sqlite3
# import math
# import time
#
#
# # return '\n'.join(f'{i}. {v}' for i, v in enumerate(entries, start=offset))
#
#
# class Pokemon(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     #     # print(result)
#     # for x in range(0, len(result), 5):
#     #     if len(result) > 5:
#     #         result = result[5:]
#     #     # y = result[:x+5]
#     #     em.description = '\n'.join([x[0] for x in result][:5])
#
#     @commands.command()
#     async def find(self, ctx, member: discord.Member = None):
#         global page1
#         db = sqlite3.connect('Main.sqlite')
#         cursor = db.cursor()
#         pages = []
#         # if ctx.author == member:
#         cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ? "
#                        "AND guild_id = ? ", (ctx.author.id, ctx.author.guild.id,))
#         result = cursor.fetchall()
#         pagecount = len(cursor.fetchall())
#         numberofpages = math.ceil(pagecount / 5)
#         # x = 0
#         # if x < numberofpages:
#         #     print(x)
#
#         # page2 = discord.Embed(
#         #     title='Page 2/3',
#         #     description='Description',
#         #     colour=discord.Colour.orange()
#         # )
#         # page3 = discord.Embed(
#         #     title='Page 3/3',
#         #     description='Description',
#         #     colour=discord.Colour.orange()
#         # )
#         y = [x for l in result for x in l]
#         for x in range(0, len(result), 5):
#             page1 = discord.Embed(title="Database of shows for: " + str(ctx.author), description='\n'.join(y[x:x + 5]))
#             pages.append(page1)
#         i = 0
#         message = await ctx.send(embed=pages[i])
#         # await message.add_reaction('\u23ee')
#         await message.add_reaction('\u25c0')
#         await message.add_reaction('\u25b6')
#         # await message.add_reaction('\u23ed')
#         # i = 0
#         emoji = ''
#
#         while True:
#             if emoji == '\u25c0':
#                 if i > 0:
#                     i -= 1
#                     result = cursor.fetchmany(5)
#                     page1 = discord.Embed(title="Database of shows for: " + str(ctx.author),
#                                           description='\n'.join([x[0] for x in result][:5]))
#                     pages.append(page1)
#                     await message.edit(embed=pages[i])
#             if emoji == '\u25b6':
#                 if i < 2:
#                     i += 1
#                     # cursor.execute("SELECT ShowName FROM Anime WHERE User_id = ? "
#                     #                "AND guild_id = ? ", (ctx.author.id, ctx.author.guild.id,))
#                     result = cursor.fetchall()
#                     # y = [x for l in result for x in l]
#                     # for x in range(0, len(result), 5):
#                     em = discord.Embed(title="Database of shows for: " + str(ctx.author),
#                                        description='\n'.join([x[0] for x in result][5:]))
#                     pages.append(em)
#                     print(pages)
#                     await message.edit(embed=pages[i])
#             # if emoji == '\u23ed':
#             #     i += 2
#             #     await message.edit(embed=pages[i])
#             try:
#                 res = await self.bot.wait_for('reaction_add', timeout=30.0)
#                 if res is None:
#                     break
#                 if str(res[1]) != 'Rin#2751':  # Example: 'MyBot#1111'
#                     # print(res[1])
#                     emoji = str(res[0].emoji)
#                     await message.remove_reaction(res[0].emoji, res[1])
#             except asyncio.TimeoutError:
#                 return await message.clear_reactions()
#
#         await message.clear_reactions()
#     # x = pa.PokemonSprite(pokemon)
#     # print(x)
#     # embed = discord.Embed(title="Pokemon", description=Pokemon)
#     # embed.set_image(url=x)
#     # await ctx.send(embed=embed)
#     # p = pb.pokemon(id_or_name=pokemon)
#     # habitat = pb.pokemon_habitat(id_or_name=pokemon)
#     # sprite = pb.SpriteResource(pokemon, id_=2)
#     # print(str(sprite))
#     # em = discord.Embed(title=str(p))
#     # em.add_field(name="Habitat", value=str(habitat))
#     # await ctx.send(embed=em)
#
#
# def setup(bot):
#     bot.add_cog(Pokemon(bot))
