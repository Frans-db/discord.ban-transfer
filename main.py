from email import header
import sqlite3
import uuid
from tabulate import tabulate

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.guild import Guild, BanEntry
from discord.user import User

from config.config import TOKEN

table_format = 'github'

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
    cur.execute('''CREATE TABLE IF NOT EXISTS bans (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            ban_list_id VARCHAR(8) NOT NULL,
            user_id INTEGER,
            reason TEXT
        );''')

    print('Initialisation done')


async def get_banned_list(ctx: Context):
    guild: Guild = ctx.guild
    bans: list[BanEntry] = await guild.bans()
    return bans


@bot.command()
@commands.is_owner()
async def createList(ctx: Context):
    bans = await get_banned_list(ctx)

    ban_list_id = str(uuid.uuid4())[:8]
    user_id = ctx.author.id
    guild_id = ctx.guild.id

    cur.execute('INSERT INTO ban_lists (id, user_id, guild_id) VALUES (?, ?, ?)',
                (ban_list_id, user_id, guild_id))

    query_bans = []
    for ban in bans:
        query_bans.append((
            ban_list_id,
            ban.user.id,
            ban.reason,
        ))
    cur.executemany(
        'INSERT INTO bans (ban_list_id, user_id, reason) VALUES (?, ?, ?)', query_bans)

    conn.commit()

    await ctx.send(f'User {ctx.author} created ban list ({ban_list_id}) for server {ctx.guild} with {len(query_bans)} users')


@bot.command()
@commands.is_owner()
async def viewLists(ctx: Context):
    # get context data
    user_id = ctx.author.id
    guild_id = ctx.guild.id
    # get ban lists for the user and the guild
    cur.execute('SELECT * FROM ban_lists WHERE user_id = ?', (user_id, ))
    user_lists = cur.fetchall()
    cur.execute('SELECT * FROM ban_lists WHERE guild_id = ?', (guild_id, ))
    guild_lists = cur.fetchall()
    # table information
    headers = ['Ban List Id', 'User', 'Guild', 'Time']
    # create table data for the user
    table_data = []
    for (ban_list_id, user_id, guild_id, timestamp) in user_lists:
        guild = await bot.fetch_guild(guild_id)
        table_data.append([ban_list_id, ctx.author, guild, timestamp])
    # append to message
    message = f'**Ban lists for user {ctx.author}**\n'
    message += f"```{tabulate(table_data, headers=headers, tablefmt=table_format)}```\n"
    # create table data for the guild
    table_data = []
    for (ban_list_id, user_id, guild_id, timestamp) in guild_lists:
        user = await bot.fetch_user(user_id)
        table_data.append([ban_list_id, user, ctx.guild, timestamp])
    # append to message
    message += f'**Ban lists for guild {ctx.guild}**\n'
    message += f"```{tabulate(table_data, headers=headers, tablefmt=table_format)}```"

    await ctx.send(message)


@bot.command()
@commands.is_owner()
async def viewList(ctx: Context, ban_list_id: str):
    # get ban list from database
    cur.execute('SELECT * FROM ban_lists WHERE id = ?', (ban_list_id, ))
    ban_list = cur.fetchone()
    # check if list exists
    if ban_list is None:
        await ctx.send(f'No ban list with id **{ban_list_id}** found')
        return
    ban_list_id, user_id, guild_id, timestamp = ban_list
    # check if either user made the list, or the list was made in this server
    if (user_id != ctx.author.id) and (guild_id != ctx.guild.id):
        await ctx.send('Can\'t view ban lists that you didn\'t create or that weren\'t made in this server')
        return
    # get user who made the ban list and guild the ban list was made in
    user = await bot.fetch_user(user_id)
    guild = await bot.fetch_guild(guild_id)
    # get bans from database
    cur.execute('SELECT * FROM bans WHERE ban_list_id = ?', (ban_list_id, ))
    bans = cur.fetchall()
    # table information
    headers = ['User', 'Reason']
    # create ban table data
    table_data = []
    for id, ban_list_id, banned_user_id, reason in bans:
        banned_user = await bot.fetch_user(banned_user_id)
        table_data.append(
            [banned_user, reason if reason else "No Reason Given"])
    # create message
    message = f'Ban list created by **{user}** for server **{guild}** at time {timestamp} with {len(bans)} bans:\n'
    message += f"```{tabulate(table_data, headers=headers, tablefmt=table_format)}```"

    await ctx.send(message)


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
