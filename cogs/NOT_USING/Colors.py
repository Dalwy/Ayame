import discord
from discord.ext import commands
import json
from collections import OrderedDict


class Colors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.role_channel = 566857715192954881
        self.colors = json.load(open('JSON_Files/colors.json'), object_pairs_hook=OrderedDict, encoding='UTF-8')
        self.emojis = ['✅', '⬅', '➡']

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def Colors(self, ctx):
        """Colors for Users"""
        Black = self.bot.get_emoji(603444531597148185)
        White = self.bot.get_emoji(603444531605536784)
        Blue = self.bot.get_emoji(603444531186368549)
        LightBlue = self.bot.get_emoji(603444531660193803)
        Red = self.bot.get_emoji(603444531584827403)
        Coral = self.bot.get_emoji(603444531546947585)
        HotPink = self.bot.get_emoji(603444531278381058)
        CherryBlossom = self.bot.get_emoji(603444531513393152)
        Purple = self.bot.get_emoji(603444531727171585)
        LightPurple = self.bot.get_emoji(603444531743948821)
        Yellow = self.bot.get_emoji(603444531622445076)
        NeonGreen = self.bot.get_emoji(603444531408666645)
        Mint = self.bot.get_emoji(603444531353878541)





        em = discord.Embed()
        # em.set_image(url=self.rules_img)
        f = discord.File('Images/Colors.png', filename='Colors.png')
        await ctx.send(file=f)


        my_dic = self.colors
        embed = discord.Embed()
        embed.colour = 0xf9f9f9
        # embed.title = ' '.join(['{} {}'.format(str(), x) for x in my_dic["Title"]]) + str()
        # embed.description = ' '.join(['{} {}'.format(str(), x) for x in my_dic["Description"]]) + str()

        """Change this portion to a tuple later"""
        # for color in my_dic.values():
        #     embed.add_field(name=str(" ") + ' '.join(my_dic[color]), value="OwO")
        embed.add_field(name=str(Black) + ' '.join(my_dic['Field']), value="⠀")
        embed.add_field(name=str(White) + ' '.join(my_dic['Field2']), value="⠀")
        embed.add_field(name=str(Blue) + ' '.join(my_dic['Field3']), value="⠀")
        embed.add_field(name=str(LightBlue) + ' '.join(my_dic['Field4']), value="⠀")
        embed.add_field(name=str(Red) + ' '.join(my_dic['Field5']), value="⠀")
        embed.add_field(name=str(Coral) + ' '.join(my_dic['Field6']), value="⠀")
        embed.add_field(name=str(HotPink) + ' '.join(my_dic['Field7']), value="⠀")
        embed.add_field(name=str(CherryBlossom) + ' '.join(my_dic['Field8']), value="⠀")
        embed.add_field(name=str(Purple) + ' '.join(my_dic['Field9']), value="⠀")
        embed.add_field(name=str(LightPurple) + ' '.join(my_dic['Field10']), value="⠀")
        embed.add_field(name=str(Yellow) + ' '.join(my_dic['Field11']), value="⠀")
        embed.add_field(name=str(NeonGreen) + ' '.join(my_dic['Field12']), value="⠀")
        embed.add_field(name=str(Mint) + ' '.join(my_dic['Field13']), value="⠀")

        msg = await ctx.send(embed=embed)

        message = ctx.message
        await message.delete()
            # await ctx.send(embed=embed)
        await msg.add_reaction(Black)
        await msg.add_reaction(White)
        await msg.add_reaction(Blue)
        await msg.add_reaction(LightBlue)
        await msg.add_reaction(Red)
        await msg.add_reaction(Coral)
        await msg.add_reaction(HotPink)
        await msg.add_reaction(CherryBlossom)
        await msg.add_reaction(Purple)
        await msg.add_reaction(LightPurple)
        await msg.add_reaction(Yellow)
        await msg.add_reaction(NeonGreen)
        await msg.add_reaction(Mint)



            # await self.bot.wait_for('checkmark', timeout=None)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        if message_id == 603453472838516746:
            print(payload.emoji.name)
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)

            if payload.emoji.id == 603444531597148185:
                role = discord.utils.get(guild.roles, name='Black')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531605536784:
                role = discord.utils.get(guild.roles, name='White')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531186368549:
                role = discord.utils.get(guild.roles, name='Blue')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531660193803:
                role = discord.utils.get(guild.roles, name='Light Blue')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531584827403:
                role = discord.utils.get(guild.roles, name='Red')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531546947585:
                role = discord.utils.get(guild.roles, name='Coral')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531278381058:
                role = discord.utils.get(guild.roles, name='Hot Pink')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531513393152:
                role = discord.utils.get(guild.roles, name='Cherry Blossom')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531727171585:
                role = discord.utils.get(guild.roles, name='Purple')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531743948821:
                role = discord.utils.get(guild.roles, name='Light Purple')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531622445076:
                role = discord.utils.get(guild.roles, name='Yellow')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531408666645:
                role = discord.utils.get(guild.roles, name='Neon Green')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

            elif payload.emoji.id == 603444531353878541:
                role = discord.utils.get(guild.roles, name='Mint')
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role, atomic=True)
                        print("has been given: " + str(role))

def setup(bot):
    bot.add_cog(Colors(bot))
