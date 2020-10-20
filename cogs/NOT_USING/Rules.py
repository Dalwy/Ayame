import discord
from discord.ext import commands
import json



class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emojis =['✅']

        self.DalwyRules = 'https://cdn.discordapp.com/attachments/659652540488482837/659658620547629058/Dalwy.png'

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def Rules(self, ctx):
        # Dalwy Rules
        if ctx.guild.id == 692940723955302451:
            Ai = self.bot.get_emoji(692952284354576427)
            ST = self.bot.get_emoji(692952385856995339)
            PaS = self.bot.get_emoji(692952284581199892)
            DB = self.bot.get_emoji(692952284312633455)
            embed = discord.Embed()
            with open('JSON_Files/DalwyRules.json', encoding='utf-8'):
                my_dic = json.load(open('JSON_Files/DalwyRules.json', encoding='utf-8'))
                embed.description = '\n'.join(['{}'.format(x) for x in my_dic["Description"]])
                embed.colour = 0xf9f9f9
                embed.add_field(name="Ai", value=Ai)
                embed.add_field(name="Software Testing", value=ST)
                embed.add_field(name="Probability and Stats", value=PaS)
                embed.add_field(name="Databases", value=DB)
                embed.title = ''.join(my_dic["Title"])
                # embed.set_image(url=self.DalwyRules)
                msg = await ctx.send(embed=embed)
            await msg.add_reaction(Ai)
            await msg.add_reaction(PaS)
            await msg.add_reaction(DB)
            await msg.add_reaction(ST)
            message = ctx.message
            await message.delete()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 692986216005632060:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, self.bot.guilds)
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                else:
                    await guild.channel.send("Member not found")
            else:
                await guild.channel.send("Role not found")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        message_id = payload.message_id
        if message_id == 692986216005632060:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
            role = discord.utils.get(guild.roles, name=payload.emoji.name)
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)
                else:
                    await guild.channel.send("Member not found")
            else:
                await guild.channel.send("Role not found")
def setup(bot):
    bot.add_cog(Rules(bot))
