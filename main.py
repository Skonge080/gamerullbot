import os
import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import random
import requests
from keep_alive import keep_alive

keep_alive()

start_time = datetime.datetime.now()

TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
PREFIX = os.environ['PREFIX']
PING_URL = os.environ['PREFIX']
target_time1 = datetime.time(4, 0, 0)
target_time2 = datetime.time(4, 0, 59)

activity = discord.Activity(type=discord.ActivityType.watching, name="новый Мем")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, activity=activity)


async def upload_image():
  try:
    image_number = datetime.datetime.now().day
    file_path = f"images/{image_number}.jpg"
    if channel:
      with open(file_path, 'rb') as file:
        await channel.send(file=discord.File(file))
        print('image sent')
  except Exception as e:
    print(f'ERROR: {e}')


@tasks.loop(seconds=60)
async def keep_alive():
    try:
        response = requests.get(PING_URL)
        if response.status_code == 200:
            print("Успешный запрос к проекту")
        else:
            print(f"Ошибка при обращении к проекту. Код состояния: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

@tasks.loop(seconds=60)
async def daily_image():
  print('Checking the time')
  current_time = datetime.datetime.now().time()
  if target_time1 <= current_time <= target_time2:
    print(f'Right time; datetime: {datetime.datetime.now()}')
    await upload_image()
  else:
    print(f'Wrong time; datetime: {datetime.datetime.now()}')


@bot.command()
async def ping(ctx):
  await ctx.send('pong')
  print('pong sent')

@bot.command()
async def image(ctx):
  await upload_image()

@bot.command()
async def stop(ctx):
  daily_image.stop()
  print('daily upload stopped')
  await ctx.send('daily upload stopped')

@bot.command()
async def start(ctx):
  daily_image.start()
  print('daily upload started')
  await ctx.send('daily upload started')

@bot.command()
async def pid(ctx):
  await asyncio.sleep(random.uniform(0.1, 3.0))
  await ctx.send(f'pid: {os.getpid()}, working time: {datetime.datetime.now() - start_time}')
  print('pid sent')

@bot.command()
async def close(ctx, *, pid: str):
    try:
        pid = int(pid)
    except ValueError:
        await ctx.send("Пожалуйста, введите число.")
        return
    if pid == os.getpid():
      print(f'{pid} closed')
      await ctx.send(f'{pid} closed')
      await asyncio.sleep(1)
      await bot.close()

@bot.event
async def on_ready():
  global channel
  channel = bot.get_channel(CHANNEL_ID)
  print(f'Logged in as {bot.user.name}')
  daily_image.start()
  keep_alive.start()


bot.run(TOKEN)
