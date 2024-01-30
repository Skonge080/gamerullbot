import os
import discord
from discord.ext import commands, tasks
import datetime
from keep_alive import keep_alive

keep_alive()

TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
#OWNER_ID = int(os.environ['OWNER_ID'])
PREFIX = os.environ['PREFIX']
log = False
target_time1 = datetime.time(4, 0, 0)
target_time2 = datetime.time(4, 4, 59)

activity = discord.Activity(type=discord.ActivityType.watching, name="новый Мем")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, activity=activity)

message_buffer = []

async def upload_image():
  try:
    image_number = datetime.datetime.now().day
    file_path = f"images/{image_number}.jpg"
    if channel:
      with open(file_path, 'rb') as file:
        await channel.send(file=discord.File(file))
    if log:
      message_buffer.append('image sent')
      print('image sent')
    else:
      print('image sent')
  except Exception as e:
    if log:
      message_buffer.append(f'ERROR: {e}')
      print(f'ERROR: {e}')
    else:
      print(f'ERROR: {e}')

@tasks.loop(seconds=300)
async def send_log():
  if message_buffer:
    if owner:
      await owner.send("\n".join(message_buffer))
      message_buffer.clear()

@tasks.loop(seconds=300)
async def daily_image():
  if log:
    message_buffer.append('Checking the time')
    print('Checking the time')
  else:
    print('Checking the time')
  current_time = datetime.datetime.now().time()
  if target_time1 <= current_time <= target_time2:
    if log:
      message_buffer.append(f'Right time; datetime: {datetime.datetime.now()}; {PREFIX}; {target_time1}')
      print(f'Right time; datetime: {datetime.datetime.now()}')
    else:
      print(f'Right time; datetime: {datetime.datetime.now()}')
    await upload_image()
  else:
    if log:
      message_buffer.append(f'Wrong time; datetime: {datetime.datetime.now()}; {PREFIX}; {target_time1}')
      print(f'Wrong time; datetime: {datetime.datetime.now()}')
    else:
      print(f'Wrong time; datetime: {datetime.datetime.now()}')


@bot.command()
async def ping(ctx):
  await ctx.send('pong')
  if log:
    message_buffer.append('pong sent')
    print('pong sent')
  else:
    print('pong sent')


@bot.command()
async def image(ctx):
  await upload_image()


@bot.command()
async def stop(ctx):
  daily_image.stop()
  if log:
    message_buffer.append('daily upload stopped')
    print('daily upload stopped')
  else:
    print('daily upload stopped')


@bot.command()
async def start(ctx):
  daily_image.start()
  if log:
    message_buffer.append('daily upload started')
    print('daily upload started')
  else:
    print('daily upload started')


@bot.event
async def on_ready():
  global channel, owner
  channel = bot.get_channel(CHANNEL_ID)
  owner = await bot.fetch_user(OWNER_ID)
  if log:
    message_buffer.append(f'Logged in as {bot.user.name}')
    print(f'Logged in as {bot.user.name}')
  else:
    print(f'Logged in as {bot.user.name}')
  daily_image.start()
  #send_log.start()


bot.run(TOKEN)
