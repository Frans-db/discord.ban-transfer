import discord

from config.config import TOKEN

client = discord.Client()

@client.event
async def on_ready():
    pass


@client.event
async def on_message(message):
    await message.channel.send('hi!')


if __name__ == '__main__':
    client.run(TOKEN)