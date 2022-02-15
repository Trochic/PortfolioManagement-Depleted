import discord
from discord.ext import commands
from binance.client import Client
from mainfunct import cmdu
from datetime import datetime
import csv
import matplotlib.pyplot as plt 
import mplfinance as mpf
import pandas as pd
import matplotlib.dates as mpl_dates
import os 


class Defi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    #on demande la quantité et le pourcentage journalier de rendement
    async def interet(self, ctx, qte, pjr, jours = 7):
        qte = float(qte)
        pjr = float(pjr)
        resultat = qte
        gain = 0
        compt = 1
        journees = []
        quantite = []
        for i in range(int(jours)):
            resultat = resultat * (1 + (pjr/100)) + float(qte) #On compose les intérets
            quantite.append(resultat)
            journees.append(compt)
            compt+=1
            gain = gain - float(qte)

        plt.plot(journees, quantite)
        plt.ylabel('Quantite')
        plt.xlabel('Journees')
        
        plt.savefig('defi.png')

        gain = gain + resultat - qte #Calcul du gain
        prctgain = ((resultat * 100) / qte) - 100 #Calcul du pourcentage de gain
        
        resembed = discord.Embed(title = f'Resultats au bout de {jours} jours', color=0x3224ff)
        resembed.add_field(name='Resultat total :', value=f'{format(resultat,".4f")}', inline=True)
        resembed.add_field(name='Gain :', value=f'{format(gain,".4f")}',inline=True)
        resembed.add_field(name='Pourcentage de gains :', value=f'{format(prctgain,".2f")} %',inline=True)
        await ctx.send(embed=resembed)
        with open('./defi.png', "rb") as graphique:
            await ctx.send(file=discord.File(graphique, 'defi.png'))
            os.remove("./defi.png")


def setup(client):
    client.add_cog(Defi(client))