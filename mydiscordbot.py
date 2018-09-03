import discord

from discord.ext import commands
import asyncio
import youtube_dl
import time

Client = discord.Client()
client = commands.Bot(command_prefix="!")

players = {}



@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='The Game'))
    print("Bot is ready!")


@client.event
async def on_message(message):
    userID = message.author.id
    if message.content == "give me a cookie please":
        await client.send_message(message.channel, " Here you go <@%s>:cookie:!" % (userID))
    elif message.content == "give me a cookie":
        await client.send_message(message.channel, "Say please <@%s>... :angry:" % (userID))
    if message.content.upper().startswith('!PING'):
        await client.send_message(message.channel, "<@%s> Pong!" % (userID))
    await client.process_commands(message)


@client.command(pass_context=True)
async def summon(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)


@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx, url):
    playingstatus = url
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()


@client.command(pass_context=True)
async def surprise(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    player.start()


@client.command(pass_context=True)
async def help_info(context):
    author = context.message.author
    embed = discord.Embed(
        color=discord.Color.dark_grey()
    )

    embed.set_author(name='List of Commands for the Bot!')
    embed.add_field(name='!ping', value='Returns Pong!', inline=False)
    embed.add_field(name="give me a cookie please", value='Will give you a cookie', inline=False)
    embed.add_field(name='!summon', value='Summons the bot to join the voice channel', inline = False)
    embed.add_field(name ='!play', value ='Plays the audio of a Youtube video', inline= True)
    embed.add_field(name='!pause', value='Pauses the current audio being played', inline =False)

    await client.send_message(author, embed=embed)


@client.command(pass_context=True)
async def test(context, arg1,arg2):
    await context.send('argument 1= ' + arg1 + ' argument 2=' + arg2)


@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()


@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()



client.run("NDg1OTkwODIxNzY2ODg5NDgz.Dm4nWw.KRKO12w94LXAdzdf8kTc59w1_2w")

