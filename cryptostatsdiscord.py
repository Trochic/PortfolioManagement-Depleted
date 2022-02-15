from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime
import json
import csv
import time
import threading
import discord
import os
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
from discord.ext.commands import Bot
from mainfunct import cmdu

api_key = os.environ.get('APIKEY')
api_secret = os.environ.get('SECRETKEY')
    
inter = Client(api_key, api_secret)

client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
    print('Bot is ready.')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}.py')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}.py')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def cryptotuto(ctx):
    tuto = discord.Embed(title="Tuto", color=0x3224ff)
    tuto.add_field(name="Instructions", value="Créer une clé api binance en lecture seule (comme ça je peux pas vous piquer d'argent) \nFaire .register <apikey> <apisecret> (Mieux vaut mp le bot pour passer la commande mais blc en vrai)\nEt ensuite faut que je redémarre le bot parce que pas tout est automatisé\nEt ensuite tu auras accès à ton solde cumulé en euros, et en BTC")
    await ctx.send(embed=tuto)


client.run(os.environ.get('CRYPTOTOKEN'))