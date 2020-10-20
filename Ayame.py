import discord
from discord import guild
from discord.ext import commands
from discord.channel import TextChannel
import sqlite3
import json
import os
import logging
import datetime

logging.basicConfig(level=logging.INFO)


def load_creds():
    with open('creds.json') as f:
        return json.load(f)


creds = load_creds()
Rtoken = creds['Rtoken']
Atoken = creds['Atoken']
all_extensions = []

# Paradise = discord.Client()




def get_prefixes(bot, message):
    with open('JSON_Files/prefixes.json') as f:
        prefixes = json.load(f)
    if str(message.guild.id) not in prefixes:
        prefixes[str(message.guild.id)] = "Ayame "
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=get_prefixes)


@bot.event
async def on_ready():
    print('Welcome to Paradise: ' + str(bot.user.name) + '\n')
    print('Id: ' + str(bot.user.id))
    print('Guilds: ', str(len(bot.guilds)))
    print('Users: ', str(len(set(bot.get_all_members()))))
    game = discord.Game("With Dalwy ^-^")
    return await bot.change_presence(status=None, activity=game)




@bot.command(pass_context=True)
async def info(ctx, user: discord.Member):
    emoji = bot.get_emoji(598821577689137165)
    embed = discord.Embed()
    embed.colour = 0xf9f9f9

    embed.title = f"{emoji}"
    embed.add_field(name="ID ", value="{}".format(user.display_name))
    embed.add_field(name="Status ", value="{}".format(user.status))
    embed.add_field(name="Highest role ", value="{}".format(user.top_role))
    embed.add_field(name="Joined at ", value="{}".format(user.joined_at))
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)



@bot.command(pass_context=True, aliases=["Clear"])
@commands.has_permissions(administrator=True)
async def clear(ctx, number: int):
    var = datetime.time.second
    deleted = await TextChannel.purge(ctx.message.channel, limit=number)
    msg = 'Deleted {} Messages'.format(len(deleted))
    await ctx.send(msg)


@bot.event
async def on_guild_join(server):
    with open('JSON_Files/prefixes.json') as f:
        prefixes = json.load(f)
    prefixes[str(server.id)] = "Ayame "
    with open('JSON_Files/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(server):
    with open('JSON_Files/prefixes.json') as f:
        prefixes = json.load(f)
    prefixes.pop(str(server.id))
    with open('JSON_Files/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command(pass_context=True, aliases=["cp"])
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, prefix):
    """To change do `Ayame cp <prefix>`"""
    with open('JSON_Files/prefixes.json') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('JSON_Files/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send('Prefix has been changed to: ' + str(prefix))


@bot.command()
async def cogs (ctx):
    """Shows loaded and unloaded cogs"""
    loaded = [x for x in bot.cogs]
    unloaded = [x for x in all_extensions if x not in bot.cogs]
    if not unloaded:
        unloaded = ["None"]
    em = discord.Embed(color=discord.Color.dark_green())
    em.add_field(name="Loaded modules", value=', '.join(loaded))
    embed = discord.Embed(color=discord.Color.red())
    embed.add_field(name="Unloaded modules", value=', '.join(unloaded))
    cog = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Cog_font_awesome.svg/512px-Cog_font_awesome.svg.png"
    embed.set_thumbnail(url=cog)
    em.set_thumbnail(url=cog)
    await ctx.send(embed=em)
    await ctx.send(embed=embed)

for file in os.listdir('cogs'):
    name = file[:-3]
    try:
        if file.endswith('.py'):
            bot.load_extension("cogs.{}".format(name))
            all_extensions.append(name)
            print("Loaded cogs: " + name)
    except Exception as e:
        print("Failed to load {}\n{}: {}".format(name, type(e).__name__, e))
bot.run(Rtoken)

