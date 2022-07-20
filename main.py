from discord.ext import commands

from config.config import TOKEN

bot = commands.Bot(command_prefix='!')

@bot.command()
@commands.is_owner()
async def ping(ctx):
    await ctx.send(f'Pong! {bot.latency:.2f} seconds')


if __name__ == '__main__':
    bot.run(TOKEN)