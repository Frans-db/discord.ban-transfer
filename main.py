from discord.ext import commands

from config.config import TOKEN

bot = commands.Bot(command_prefix='!')

@bot.command()
async def say(ctx, *, arg):
    await ctx.send(arg)


if __name__ == '__main__':
    bot.run(TOKEN)