import discord
import os
from rethinkdb import r
from dotenv import load_dotenv
import asyncio
from threading import Thread
import time

load_dotenv(verbose=True)

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()
conn = r.connect(db_host, db_port).repl()


def get_temperature():
    cursor = r.db('dashboard') \
              .table('temperatures') \
              .order_by(r.desc('timestamp')) \
              .run(conn)
    return cursor[0]['value'], cursor[0]['timestamp']


def get_humidity():
    cursor = r.db('dashboard') \
              .table('humidity') \
              .order_by(r.desc('timestamp')) \
              .run(conn)
    return cursor[0]['value'], cursor[0]['timestamp']


def get_door():
    cursor = r.db('dashboard') \
              .table('doors') \
              .order_by(r.desc('timestamp')) \
              .run(conn)
    return cursor[0]['opened'], cursor[0]['timestamp']


def is_me(m):
    return m.author == client.user


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!ping'):
        await message.channel.send('pong')

    if message.content.startswith('!temperature'):
        value, ts = get_temperature()
        pattern = 'Temperature: {}°C ({}-{}-{} {}:{})'
        await message.channel.send(pattern.format(
            value,
            ts.year,
            ts.month,
            ts.day,
            ts.hour,
            ts.minute
        ))

    if message.content.startswith('!humidity'):
        value, ts = get_humidity()
        pattern = 'Humidity: {}% ({}-{}-{} {}:{})'
        await message.channel.send(pattern.format(
            value,
            ts.year,
            ts.month,
            ts.day,
            ts.hour,
            ts.minute
        ))

    if message.content.startswith('!door'):
        value, ts = get_door()
        if value is True:
            formatted_value = 'opened'
        else:
            formatted_value = 'closed'
        pattern = 'Door was {} ({}-{}-{} {}:{})'
        await message.channel.send(pattern.format(
            formatted_value,
            ts.year,
            ts.month,
            ts.day,
            ts.hour,
            ts.minute
        ))

    if message.content.startswith('!clear'):
        await message.channel.purge(limit=100)


async def door_supervisor():
    while(True):
        cursor = r.db('dashboard').table('doors').changes().run(conn)
        for document in cursor:
            if document['new_val']['opened'] is True:
                formatted_value = 'opened'
            else:
                formatted_value = 'closed'
            pattern = 'Door was {} ({}-{}-{} {}:{})'
            channel = client.get_channel(734049980721135656)
            await channel.send(pattern.format(
               formatted_value,
               document['new_val']['timestamp'].year,
               document['new_val']['timestamp'].month,
               document['new_val']['timestamp'].day,
               document['new_val']['timestamp'].hour,
               document['new_val']['timestamp'].minute
            ))

async def start():
    await client.start(token) # use client.start instead of client.run

def run_it_forever(loop):
    loop.run_forever()

if __name__ == '__main__':
    asyncio.get_child_watcher() # I still don't know if I need this method. It works without it.

    loop = asyncio.get_event_loop()
    loop.create_task(start())

    thread = Thread(target=run_it_forever, args=(loop,))
    thread.start()
    time.sleep(3)
    loop.create_task(door_supervisor())