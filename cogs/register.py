import discord
from discord.ext import commands
from binance.client import Client
from mainfunct import cmdu
import csv

class Register(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def register(self, ctx, apikey, apisecret):
        with open("./ids.csv", "r") as listid:
            listidreader = csv.DictReader(listid)
            for row in listidreader:
                if int(row["discordid"]) == ctx.author.id:
                    await ctx.send("Déjà enregistré espèce de bg")
                    return
        with open("./ids.csv", "a") as listid:
            newrow = csv.writer(listid, delimiter= ',')
            newrow.writerow([f'{str(ctx.author.id)}', f'{str(apikey)}', f'{str(apisecret)}', "0", "0"])
            open(f'./data/{str(ctx.author.id)}.txt', 'x')

def setup(client):
    client.add_cog(Register(client))