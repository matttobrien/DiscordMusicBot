import discord
from discord.ext import commands
import youtube_dl
from requests import get

class music(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  # join voice channel
  @commands.command()
  async def join(self, ctx):
    # if not currently in a channel
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel")
    voiceChannel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voiceChannel.connect()
    else:
      await ctx.voice_client.move_to(voiceChannel)
  
  # disconnect from voice channel
  @commands.command()
  async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()
    await ctx.send('Ok bye!')
  
  # play music
  @commands.command()
  async def play(self, ctx, *args):
    # join args if user entered a string instead of url
    if len(args) > 1:
      url = " ".join(args)
    else:
      url = args
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': 'bestaudio'}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      try:
        get(url) 
      except:
        info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
      else:
        info = ydl.extract_info(url, download=False)
      url2 = info['formats'][0]['url']
      # create audio stream
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)
      await ctx.send(f"Now playing: {info['title']} 🎶")

  # stop music
  @commands.command()
  async def stop(self, ctx):
    ctx.voice_client.stop()
    await ctx.send('Stopped 🛑')

  # pause music
  @commands.command()
  async def pause(self, ctx):
    ctx.voice_client.pause()
    await ctx.send('Paused ⏸')
    
  # resume music
  @commands.command()
  async def resume(self, ctx):
    ctx.voice_client.resume()
    await ctx.send('Resumed ▶️')

def setup(client):
  client.add_cog(music(client))