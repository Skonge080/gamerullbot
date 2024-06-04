import os
import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import random
from keep_alive import keep_alive, send_request

keep_alive()
send_request()


start_time = datetime.datetime.now().replace(microsecond=0)

TOKEN = os.environ['TOKEN']
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
PREFIX = os.environ['PREFIX']
target_time1 = datetime.time(3, 0, 0)
target_time2 = datetime.time(3, 0, 59)


activity = discord.Activity(type=discord.ActivityType.watching, name="новый Мем")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, activity=activity)


async def upload_meme():
    try:
        current_date = datetime.datetime.now()
        directory = f'memes/{current_date.year}/{current_date.month}'
        for file in os.listdir(directory):
            if file.startswith(str(current_date.day) + '.'):
                file_path = os.path.join(directory, file)
                break
        if file_path and channel:
            with open(file_path, 'rb') as file:
                await asyncio.sleep(random.uniform(0.1, 3.0))
                await channel.send(file=discord.File(file))
                print('meme sent')
        else:
            print('No file found with the specified number.')
    except Exception as e:
        print(f'ERROR: {e}')


@tasks.loop(seconds=60)
async def daily_meme():
    print('Checking the time')
    current_time = datetime.datetime.now().time().replace(microsecond=0)
    if target_time1 <= current_time <= target_time2:
        print(f'Right time; datetime: {datetime.datetime.now().replace(microsecond=0)}')
        await upload_meme()
    else:
        print(f'Wrong time; datetime: {datetime.datetime.now().replace(microsecond=0)}')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')
    print('pong sent')

@bot.command()
async def meme(ctx):
    await upload_meme()

@bot.command()
async def stop(ctx):
    daily_meme.stop()
    print('daily upload stopped')
    await ctx.send('daily upload stopped')

@bot.command()
async def start(ctx):
    daily_meme.start()
    print('daily upload started')
    await ctx.send('daily upload started')

@bot.command()
async def pid(ctx):
    await asyncio.sleep(random.uniform(0.1, 3.0))
    await ctx.send(f'pid: {os.getpid()}, working time: {datetime.datetime.now().replace(microsecond=0) - start_time}')
    print('pid sent')

@bot.command()
async def close(ctx, *, pid: str):
    try:
        pid = int(pid)
    except ValueError:
        await asyncio.sleep(random.uniform(0.1, 3.0))
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
    daily_meme.start()


bot.run(TOKEN)
