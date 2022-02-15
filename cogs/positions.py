from binance.client  import Client
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
from discord.ext.commands import Bot
import csv
from mainfunct import cmdu

class Positions(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pos(self, ctx):
        with open("./ids.csv", "r") as listidr:
            listidread = csv.DictReader(listidr)
            for row in listidread:
                if row["discordid"] == str(ctx.author.id):
                    apik = row["api_key"]
                    apisk = row["api_secret"]
                    openacc = Client(apik, apisk)
                    for rows in openacc.get_all_orders(symbol="BTCUSDT"):
                        print(f'{rows["side"]}, {rows["price"]}, {rows["origQty"]}, {rows["executedQty"]}, {rows["type"]}, {rows["status"]}, {rows["cummulativeQuoteQty"]}, {rows["origQuoteOrderQty"]}')
                    

def setup(client):
    client.add_cog(Positions(client))