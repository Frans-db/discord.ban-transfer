import sqlite3
import uuid

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
            id        VARCHAR(8) PRIMARY KEY UNIQUE        NOT NULL,
            user_id   INTEGER                              NOT NULL,
            guild_id  INTEGER                              NOT NULL,
            timestamp TIMESTAMP  DEFAULT CURRENT_TIMESTAMP NOT NULL
        );''')
    print('Initialisation done')


async def get_banned_list(ctx: Context):
    guild: Guild = ctx.guild
    bans: list[BanEntry] = await guild.bans()
    return bans


@bot.command()
async def createList(ctx: Context):
    bans = await get_banned_list(ctx)

    ban_list_id = str(uuid.uuid4())[:8]
    user_id = ctx.author.id
    guild_id = ctx.guild.id

    cur.execute('INSERT INTO ban_lists (id, user_id, guild_id) VALUES (?, ?, ?)',
                (ban_list_id, user_id, guild_id))
    conn.commit()

    await ctx.send(f'User {ctx.author} created ban list ({ban_list_id}) for server {ctx.guild}')


@bot.command()
async def viewLists(ctx: Context):
    user_id = ctx.author.id
    guild_id = ctx.guild.id

    cur.execute('SELECT * FROM ban_lists WHERE user_id = ?', (user_id, ))
    user_lists = cur.fetchall()
    cur.execute('SELECT * FROM ban_lists WHERE guild_id = ?', (guild_id, ))
    guild_lists = cur.fetchall()

    message = f'**Ban lists for user {ctx.author}**\n'
    for (ban_list_id, user_id, guild_id, timestamp) in user_lists:
        guild = bot.get_guild(guild_id)
        message += f'{ban_list_id}, {ctx.author}, {guild}, {timestamp}\n'
    await ctx.send(message)

    message = f'**Ban lists for guild {ctx.guild}**\n'
    for (ban_list_id, user_id, guild_id, timestamp) in guild_lists:
        user = bot.get_user(user_id)
        message += f'{ban_list_id}, {user}, {ctx.guild}, {timestamp}\n'
    await ctx.send(message)


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
