import sqlite3

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.guild import Guild, BanEntry
from discord.user import User

from config.config import TOKEN

bot = commands.Bot(command_prefix='!')
conn = sqlite3.connect('database.db')
cur = conn.cursor()


@bot.event
async def on_ready():
    cur.execute('''CREATE TABLE IF NOT EXISTS ban_lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            guild_id INTEGER
        );''')



async def get_banned_list(ctx: Context):
    guild: Guild = ctx.guild
    bans: list[BanEntry] = await guild.bans()
    return bans


@bot.command()
async def get_bans(ctx: Context):
    bans = await get_banned_list(ctx)
    for ban in bans:
        await ctx.send(f'{ban.user.id}, {ban.reason}')

# Helper commands


@bot.command()
@commands.is_owner()
async def ping(ctx: Context):
    await ctx.send(f'Pong! {bot.latency:.2f} seconds')


@bot.command()
@commands.is_owner()
async def guildId(ctx: Context):
    await ctx.send(f'Guild id: {ctx.guild.id}')


@bot.command()
@commands.is_owner()
async def userId(ctx: Context):
    await ctx.send(f'User id: {ctx.author.id}')

if __name__ == '__main__':
    bot.run(TOKEN)

"""
ideas:
getBans -> create a new BanList database entry with guild, user, date
           then create a ban entry for each banned user
showLists -> show banLists for this user and for this server

ban list -> get a list of users banned on this server, and the list of users to ban. ban the ~union of these 2
"""
