# Discord Ban Transfer
Transfer ban lists between servers

## Invite Bot
[Click this to invite the bot to your server](https://discord.com/api/oauth2/authorize?client_id=999292142851735603&permissions=2052&scope=bot). The bot needs message and ban permissions.

If you would rather host the bot yourself the next section explains how to do this

## How to Setup
1. Clone the repo
   ```sh
   git clone git@github.com:Frans-db/discord.ban-transfer.git
   ```
2. Create an application + bot at https://discord.com/developers/applications (For more info see https://discordpy.readthedocs.io/en/stable/discord.html)
3. Enter your application token in `config/config.py`
   ```python
   TOKEN = 'ENTER YOUR TOKEN'
   ```
4. Run `main.py`

## Using the bot
Because this bot has the ability to ban many users currently only the server owner can use any of these commands. Due to API limitations the boy can only ban 1k members at a time.

Commands:

`@bantransfer help` - Display a help menu in discord

`@bantransfer create` - Create a list of banned users for the current server

`@bantransfer lists` - Show lists created by this user or created in this server

`@bantransfer view {list id}` - Show banned users in a list

`@bantransfer ban {list id}` - Ban users in a list

`@bantransfer unban {list id}` - Unban users in a list

`@bantransfer ping` - Show bot latency

## Contact
Having any issues with this bot, or do you have ideas for other bots and projects? Feel free to send me a discord dm [Frans#5292](https://discord.com/users/235080247194812416)