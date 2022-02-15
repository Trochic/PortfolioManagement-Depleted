from binance.client  import Client
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
from discord.ext.commands import Bot
import csv
from mainfunct import cmdu

class Graph(commands.Cog):
    def __init__(self, client):
        self.client = client


    

def setup(client):
    client.add_cog(Graph(client))