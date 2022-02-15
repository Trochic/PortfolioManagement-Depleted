import discord
from discord.ext import commands
from binance.client import Client
from mainfunct import cmdu
from datetime import datetime
import csv
import os

api_key = os.environ.get('APIKEY')
api_secret = os.environ.get('SECRETKEY')
inter = Client(api_key, api_secret)

#Recupere les donnees de l'utilisateur executant la commande et affiche plusieurs statistiques basiques

class Percent(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pourcentage(self, ctx, dur):
        if (cmdu.check(ctx.author.id)):
            compt = 0
            dur = int(dur)
            resume = discord.Embed(title="Resumé", color=0x3224ff)
            for line in reversed(list(open(f"./data/{ctx.author.id}.txt", "r"))):
                if compt == 0:
                    actual = float(line.rstrip()[11:])
                    resume.add_field(name=f'{datetime.fromtimestamp(3600 + int(line.rstrip()[:10]))}', value=f': {format(actual, ".3f")}€ \n{format(float(cmdu.assetbtc("EUR", actual)), ".8f")} BTC', inline="False")
                elif compt == dur:
                    tweny = float(line.rstrip()[11:])
                    timedur = datetime.fromtimestamp(3600 + int(line.rstrip()[:10]))
                compt += 1
                lastamp = datetime.fromtimestamp(3600 + int(line.rstrip()[:10]))
            if compt - 1 < dur:
                await ctx.send(f"Pas assez d'historique bg, tu peux aller jusqu'à {compt - 1} soit jusqu'au {lastamp}")
                return                
            resume.add_field(name="Différence", value=f'{format((actual - tweny), ".3f")}€', inline="False")
            res = ((actual - tweny) / tweny) * 100
            resume.add_field(name="Pourcentage", value=f'{format(res, ".3f")}% \n\n Depuis le : {timedur}', inline="False")
            await ctx.send(embed=resume)
        else:
            await ctx.send("Tu n'es pas enregistré fait .register (.help register) pour t'enregister")

    @commands.command()
    async def worth(self, ctx):
        with open("./ids.csv", "r") as listidr:
            listidread = csv.DictReader(listidr)
            for row in listidread:
                if row["discordid"] == str(ctx.author.id):
                    worthemb = discord.Embed(title="Rendement", color=0x3224ff)
                    worthemb.add_field(name=f"En dépot", value=f'{format(float(row["deposit"]) + float(row["withdraw"]),".2f")} €', inline="False")
                    total = cmdu.getlinesum(1, ctx.author.id)
                    res = ((total / (float(row["deposit"]) + float(row["withdraw"]))) * 100 )-100
                    worthemb.add_field(name=f"Pourcentage sur total", value=f'{format(res,".2f")} %', inline="False")
                    await ctx.send(embed=worthemb)



def setup(client):
    client.add_cog(Percent(client))