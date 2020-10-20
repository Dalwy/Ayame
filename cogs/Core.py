import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta


class Greetings(commands.Cog):
    def cog_unload(self):
        print('cleanup goes here')

    def bot_check(self, ctx):
        # print('bot check')
        return True

    def bot_check_once(self, ctx):
        # print('bot check once')
        return True

    async def cog_check(self, ctx):
        print('cog local check')
        return await ctx.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        print('Error in {0.command.qualified_name}: {1}'.format(ctx, error))

    async def cog_before_invoke(self, ctx):
        print('cog local before: {0.command.qualified_name}'.format(ctx))

    async def cog_after_invoke(self, ctx):
        print('cog local after: {0.command.qualified_name}'.format(ctx))


    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.welcome_channel = 392630668066291713

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send('Hello {0.name}~'.format(member))
        else:
            await ctx.send('Hello {0.name}... This feels familiar.'.format(member))
        self._last_member = member


    # def gettime(self, time):
    #     # print(time)
    #     return time

    @commands.command()
    async def reminder(self, ctx, message, *, e_time):
        recourring_time = e_time
        r_time = datetime.strptime(recourring_time, "%I:%M %p")
        now = datetime.today().utcnow()
        then = now.replace(hour=r_time.hour, minute=r_time.minute, second=0)
        if then < now:
            then = then + timedelta(days=1)

        t_until = (then - now).seconds + 1
        msg = ctx.message
        await msg.delete()

        async def my_task(wait_time):
            await asyncio.sleep(wait_time)
            await ctx.send(message)
            self.bot.loop.create_task(my_task(24 * 60 * 60))  # run in a day

        self.bot.loop.create_task(my_task(t_until))

def setup(bot):
    bot.add_cog(Greetings(bot))
