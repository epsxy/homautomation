import discord
import os
from rethinkdb import r
from dotenv import load_dotenv

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


if __name__ == '__main__':
    client.run(token)
