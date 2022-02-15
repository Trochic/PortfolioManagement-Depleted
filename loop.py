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

while True:
    with open("./ids.csv") as listid:
        reader = csv.DictReader(listid)
        for row in reader:
            idapi_key = row["api_key"]
            idapi_secret = row["api_secret"]
            intergt = Client(idapi_key, idapi_secret)
            somme = 0
            try:
                spotwal = intergt.get_account()
            except BinanceAPIException:
                print(f'{row["discordid"]} erreur code : 11')
            for assets in spotwal["balances"]:
                if (float(assets["free"]) >= 0.00000001) or (float(assets["locked"]) >= 0.00000001):
                    somme = somme + cmdu.asseteur(assets["asset"], assets["free"]) + cmdu.asseteur(assets["asset"], assets["locked"])
            try:
                futwal = intergt.futures_account_balance()
                for items in futwal:
                    if items["asset"] == "USDT":
                        somme = somme + cmdu.asseteur(items["asset"], items["balance"])
                        with open(f'./data/{row["discordid"]}.txt', "a") as data:
                            stamp = datetime.timestamp(datetime.now())
                            newrow = csv.writer(data, delimiter= ',')
                            newrow.writerow([f'{str(int(stamp))}', f'{somme}'])
            except:
                with open(f'./data/{row["discordid"]}.txt', "a") as data:
                    stamp = datetime.timestamp(datetime.now())
                    newrow = csv.writer(data, delimiter= ',')
                    newrow.writerow([f'{str(int(stamp))}', f'{somme}'])

    time.sleep(300)