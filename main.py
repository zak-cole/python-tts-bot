from asyncio import sleep
from discord.ext import commands

import discord
import pyttsx3

'''
Discord Text-to-Speech Bot

https://discordpy.readthedocs.io/en/latest/
pip install -U discord.py

https://pypi.org/project/pyttsx3/
pip install pyttsx3

https://ffmpeg.org/
'''

# init discord utils
client = discord.Client()
bot = commands.Bot(command_prefix="tts!")

# init tts utils
engine = pyttsx3.init()

# get ffmpeg path
f = open('ffmpeg_path.txt', 'r')
ffmpeg_path = f.read()


# when bot is logged in
@bot.event
async def on_ready():
    # login confirmation
    print('Logged in as {0.user}'.format(bot))

    # set bot status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='tts generation'))


# text to speech command
@bot.command(name='join')
async def join(ctx):
    connected = ctx.author.voice
    if connected:
        await connected.channel.connect()


# text to speech command
@bot.command(name='say')
async def text_to_speech(ctx, *args):
    # save tts to file
    engine.save_to_file(str(args), 'tts_file.mp3')
    engine.runAndWait()

    # make bot join voice channel
    voice_channel = ctx.message.author.voice.channel
    if voice_channel is not None:
        vc = await voice_channel.connect()

        # get and play audio
        source = discord.FFmpegPCMAudio(executable=ffmpeg_path, source='tts_file.mp3')
        vc.play(source)

        # make bot sleep while audio is playing
        while vc.is_playing():
            await sleep(.1)

        # disconnect bot
        await vc.disconnect()


# running the bot
def main():
    f = open('token.txt', 'r')
    token = f.read()
    bot.run(token)


# for easier running
if __name__ == '__main__':
    main()
