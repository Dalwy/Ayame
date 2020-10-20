# from discord.ext import commands
# import sqlite3
# import math
# import asyncio
#
# #
# class LevelsCog(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#
#     @commands.Cog.listener()
#     async def on_message(self, message):
#         await asyncio.sleep(4)
#         if message.author.bot:
#             return
#         # msg = message.channel.id = 609807109374214194
#         # user = str(message.author.id)
#         # msg = str(message.created_at)
# #
#         db = sqlite3.connect('Main.sqlite')
#         xp_credit = 2
#         cursor = db.cursor()
#         cursor.execute(f"SELECT user_id, exp, lvl FROM xp_leveling"
#                        f" WHERE guild_id = '{message.author.guild.id}'"
#                        f"AND user_id='{message.author.id}'")
#         result = cursor.fetchone()
#         if result is None:
#             sql = (f"INSERT OR IGNORE INTO xp_leveling(guild_id, user_id, exp, lvl)"
#                    f"VALUES(?, ?, ?, ?)")
#             val = (message.author.guild.id, message.author.id, xp_credit, 0)
#             cursor.execute(sql, val)
#             db.commit()
#         else:
#             exp = result[1] + xp_credit
#             lvl_start = result[2]
#             required_xp = math.floor(5 * (lvl_start ** 2) + 50 * lvl_start + 100)
#
#             if required_xp < exp:
#                 lvl_start = lvl_start + 1
#                 # await message.channel.send(f'{message.author.mention} has leveled up. Now level *{lvl_start}*')
#                 print('LEVEL UP')
#
#             sql = "UPDATE xp_leveling SET exp = ?, lvl = ? WHERE guild_id = ? AND user_id = ?"
#             val = (exp, lvl_start, str(message.author.guild.id), str(message.author.id))
#             cursor.execute(sql, val)
#             db.commit()
# def setup(bot):
#     bot.add_cog(LevelsCog(bot))
#
