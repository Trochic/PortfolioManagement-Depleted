#Get account info on wallet balance and 

from binance.client import Client
from datetime import datetime
import json
import csv
import time
import threading
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.tasks import loop
from discord.ext.commands import Bot
from mainfunct import cmdu
from tempfile import NamedTemporaryFile
import shutil
import matplotlib.pyplot as plt 
import pandas as pd


class Account(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def account(self, ctx):
        if cmdu.check(ctx.author.id):
            emaccount = discord.Embed(title=f'Portefeuille au {datetime.fromtimestamp(int(cmdu.getlinestamp(0, ctx.author.id)))}', color=0x3224ff)
            with open("./ids.csv", "r") as listidr:
                listidread = csv.DictReader(listidr)
                emaccount.add_field(name=f"Total", value=f'{format(cmdu.getlinesum(0, ctx.author.id),".3f")} €', inline="True")
                for row in listidread:
                    if int(row["discordid"]) == ctx.author.id:
                        acapi_key = row["api_key"]
                        acapi_secret = row["api_secret"]
                        interac = Client(acapi_key, acapi_secret)
                        acspotwal = interac.get_account()
                        emaccount.add_field(name=f"Deposé", value=f'{format(float(row["deposit"]), ".3f")} €', inline="True")
                        emaccount.add_field(name=f"Retiré", value=f'{format(float(row["withdraw"]), ".3f")} €', inline="True")
                        emaccount.add_field(name="\nSpot", value="\u200b", inline="False")
                        for acassets in acspotwal["balances"]:
                            if (float(acassets["free"]) >= 0.00000001) or (float(acassets["locked"]) >= 0.00000001):
                                toeur = float(acassets["free"]) + float(acassets["locked"])
                                if cmdu.asseteur(acassets["asset"], toeur) >= 0.5:
                                    emaccount.add_field(name=f'{acassets["asset"]}', value=f'{format(toeur, ".8f")}', inline="True")
                        try:
                            acfutwal = interac.futures_account_balance()
                            emaccount.add_field(name="\nFutures", value="\u200b", inline="False")
                            for items in acfutwal:
                                emaccount.add_field(name=f'{items["asset"]}', value=f'{items["balance"]}', inline = "True")
                        except:
                            print("rip")

                        await ctx.send(embed=emaccount)
        else:
            await ctx.send("Tu n'es pas enregistré fait .register (.help register) pour t'enregister")

    @commands.command()
    async def accounteur(self, ctx):
        if cmdu.check(ctx.author.id):
            emaccount = discord.Embed(title=f'Portefeuille au {datetime.fromtimestamp(int(cmdu.getlinestamp(0, ctx.author.id)))}', color=0x3224ff)
            with open("./ids.csv", "r") as listidr:
                listidread = csv.DictReader(listidr)
                emaccount.add_field(name=f"Total", value=f'{format(cmdu.getlinesum(0, ctx.author.id),".3f")} €', inline="False")
                for row in listidread:
                    if int(row["discordid"]) == ctx.author.id:
                        acapi_key = row["api_key"]
                        acapi_secret = row["api_secret"]
                        interac = Client(acapi_key, acapi_secret)
                        acspotwal = interac.get_account()
                        emaccount.add_field(name="\nSpot", value="\u200b", inline="False")
                        for acassets in acspotwal["balances"]:
                            if (float(acassets["free"]) >= 0.00000001) or (float(acassets["locked"]) >= 0.00000001):
                                toeur = float(acassets["free"]) + float(acassets["locked"])
                                asseteur = cmdu.asseteur(acassets["asset"], toeur)
                                if asseteur >= 0.5:
                                    emaccount.add_field(name=f'{acassets["asset"]}', value=f'{format(toeur, ".8f")} = {format(asseteur, ".3f")}€', inline="True")
                        try:
                            acfutwal = interac.futures_account_balance()
                            emaccount.add_field(name="\nFutures", value="\u200b", inline="False")
                            for items in acfutwal:
                                emaccount.add_field(name=f'{items["asset"]}', value=f'{items["balance"]}', inline = "True")
                        except:
                            print("rip")

                        await ctx.send(embed=emaccount)
        else:
            await ctx.send("Tu n'es pas enregistré fait .register (.help register) pour t'enregister")

    @commands.command()
    async def deposit(self, ctx, montant, asset= "EUR"):
        if cmdu.check(ctx.author.id):
            tempfile = NamedTemporaryFile(mode="w", delete=False)
            fields = ["discordid", "api_key", "api_secret", "deposit", "withdraw"]
            with open("./ids.csv", "r") as idee, tempfile:
                reader = csv.DictReader(idee, fieldnames=fields)
                writer = csv.DictWriter(tempfile, fieldnames=fields)
                for row in reader:
                    if row["discordid"] == str(ctx.author.id):
                        row["deposit"] = str(float(row["deposit"]) + cmdu.asseteur(asset.upper(), montant))
                    row = {"discordid" : row["discordid"], "api_key" : row["api_key"], "api_secret" : row["api_secret"], "deposit" : row["deposit"], "withdraw" : row["withdraw"]}
                    writer.writerow(row)
            shutil.move(tempfile.name, "ids.csv")
            await ctx.send("c bon")
        else:
            await ctx.send("Pas inscrit fait .cryptotuto")
    
    @commands.command()
    async def withdraw(self, ctx, montant, asset= "EUR"):
        if cmdu.check(ctx.author.id):
            tempfile = NamedTemporaryFile(mode="w", delete=False)
            fields = ["discordid", "api_key", "api_secret", "deposit", "withdraw"]
            with open("./ids.csv", "r") as idee, tempfile:
                reader = csv.DictReader(idee, fieldnames=fields)
                writer = csv.DictWriter(tempfile, fieldnames=fields)
                for row in reader:
                    if row["discordid"] == str(ctx.author.id):
                        acapi_key = row["api_key"]
                        acapi_secret = row["api_secret"]
                        interac = Client(acapi_key, acapi_secret)
                        print(interac.get_withdraw_history())
                        historiq = (interac.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1608761399000", "1608761500000"))[:1]
                        for tab in historiq[0]:
                            print(tab)
                        row["withdraw"] = str(float(row["withdraw"]) - cmdu.asseteur(asset.upper(), montant))
                    row = {"discordid" : row["discordid"], "api_key" : row["api_key"], "api_secret" : row["api_secret"], "deposit" : row["deposit"], "withdraw" : row["withdraw"]}
                    writer.writerow(row)
            shutil.move(tempfile.name, "ids.csv")
        else:
            await ctx.send("Pas inscrit fait .cryptotuto")

    @commands.command()
    async def graphaccount(self, ctx):
        client = cmdu.getid(ctx.author.id)
        data = pd.read_csv(f'./data/{client["discordid"]}.txt', sep=',', header=None)
        data = pd.DataFrame(data)

        x=matplotlib.dates.date2num(data[0])
        y=data[1]
        plt.plot_date(x,y)
        plt.savefig('graph.png')

def setup(client):
    client.add_cog(Account(client))