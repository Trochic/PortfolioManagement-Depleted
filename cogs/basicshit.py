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



class BasicCommands(commands.Cog):
    def __init__(self, client):
        self.client = client


    apik = "s7O4bcEALbiJJ7AIhjbHDoWOZXEIkXHls5vLuAxD23nShT5LUhEXHWaCMfcgu2Y5"
    apisk = "9V9U1a5UVQRcXspOVOlxh4KgcYaUgVsK7Zq8CPSuKSPcPxDOk1iV5mBtDfeykPWD"
        
    @commands.command(aliases=['eur','e'])
    async def asseteur(self, ctx, montant, asset):
        await ctx.send(f'{cmdu.asseteur(asset.upper(), montant):,} €')

    @commands.command(aliases=['usd','u'])
    async def assetusd(self, ctx, montant, asset):
        await ctx.send(f'{cmdu.assetusd(asset.upper(), montant):,} $')

    @commands.command()
    async def assetbtc(self, ctx, montant, asset):
        await ctx.send(f'{cmdu.assetbtc(asset.upper(), montant):,} BTC')

    @commands.command(aliases=['a','ass'])
    async def asset(self, ctx, montant, asset):
        await ctx.send(f'{cmdu.asset(asset.upper(), montant):,} {asset[-3:]}')       

    @commands.command()
    async def fetch(self, ctx, discordid):
        with open('./ids.csv', 'r') as ids: 
            reader = csv.DictReader(ids)
            for row in reader:
                if row["discordid"] == str(discordid):
                    apik=row["api_key"]
                    apisk=row["api_secret"]
                    intergt = Client(apik, apisk)
                    print(intergt.futures_account_balance())


    @commands.command()
    async def graphtesting(self, ctx, paire, interv):
        apik = os.environ.get('APIKEY')
        apisk = os.environ.get('SECRETKEY')
        openacc = Client(apik, apisk)
        stamp = datetime.timestamp(datetime.now())
        if (interv.lower()[:2] == "1m"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_1MINUTE,start_str="2 hours ago UTC")
        elif (interv.lower()[:2] == "5m"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_5MINUTE,start_str="10 hours ago UTC")
        elif (interv.lower()[:3] == "15m"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_15MINUTE,start_str="30 hours ago UTC")
        elif (interv.lower()[:3] == "30m"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_30MINUTE,start_str="3 days ago UTC")
        elif (interv.lower()[:2] == "1h"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_1HOUR,start_str="5 days ago UTC")
        elif (interv.lower()[:2] == "4h"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_4HOUR,start_str="2 weeks ago UTC")
        elif (interv.lower()[:3] == "12h"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_12HOUR,start_str="1 month ago UTC")
        elif (interv.lower()[:2] == "1d"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_1DAY,start_str="3 month ago UTC")
        elif (interv.lower()[:2] == "1w"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_1WEEK,start_str="1 year ago UTC")
        elif (interv.lower()[:2] == "1m"):
            kline = openacc.get_historical_klines(f'{paire.upper()}', interval=Client.KLINE_INTERVAL_1MONTH,start_str="5 year ago UTC")
        else:
            await ctx.send("Ne reconnais pas l'intervalle")
        with open("kline.csv", "w") as datakline:
            fields = ["Date", "Open", "High", "Low", "Close"]
            writer = csv.DictWriter(datakline, fieldnames=fields)
            writer.writerow({"Date": "Date", "Open": "Open", "High": "High", "Low": "Low", "Close": "Close"})
            for lines in kline:
                row = {"Date": f'{lines[0]}', "Open": f'{lines[1]}', "High": f'{lines[2]}', "Low": f'{lines[3]}', "Close": f'{lines[4]}'}
                writer.writerow(row)
        df = pd.read_csv('kline.csv', index_col="Date")
        df.index = pd.to_datetime(df.index, unit='ms')
        mpf.plot(df, type='candle', style='mike',
        title=f'{paire.upper()} : {interv}',
        ylabel='Prix $',
        volume=False,
        savefig='result.png')
        with open("./result.png","rb") as graphique:
            await ctx.send(file=discord.File(graphique, f'{paire}.png'))
        




def setup(client):
    client.add_cog(BasicCommands(client))
