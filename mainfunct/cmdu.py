from binance.client import Client
import csv
import os


api_key = os.environ.get('APIKEY')
api_secret = os.environ.get('SECRETKEY')

inter = Client(api_key, api_secret)

    #Converti n'importe quelle monnaie disponible en euros
def asseteur(asset, amount):
    amount = float(amount)
    try:
        if asset != "USDT":
            if asset[:2] != "LD":
                usdtprice = amount * float(inter.get_avg_price(symbol=f'{asset}USDT')["price"])
            else:
                asset = asset[2:]
                if asset == "ERD":
                    asset = "EGLD"
                usdtprice = amount * float(inter.get_avg_price(symbol=f'{asset.upper()}USDT')["price"])
        else:
            usdtprice = amount
        priceeur = usdtprice / float(inter.get_avg_price(symbol="EURUSDT")["price"])
        return priceeur
    except:
        return 0

def assetbtc(asset, amount):
    try:
        amount = float(amount)
        if asset != "BTC":
            btcprice = amount / float(inter.get_avg_price(symbol=f'BTC{asset.uppper()}')["price"])
        else:
            btcprice = amount
        return btcprice
    except:
        return 0

def assetusd(asset, amount):
    amount = float(amount)
    if asset != "USDT":
        usdprice = amount * float(inter.get_avg_price(symbol=f'{asset.upper()}USDT')["price"])
    else:
        usdprice = amount
    return usdprice
        
def fetch(discid):
    with open("./ids.csv", "r") as listid:
        listidreader = csv.DictReader(listid)
        for row in listidreader:
            if int(row["discordid"]) == int(discid):
                intergt = Client(row["api_key"], row["api_secret"])
                futwal = intergt.get_isolated_margin_account()
                with open ("./recu.txt", "w") as ecriretest:
                    ecriretest = csv.writer(ecriretest)
                    ecriretest.writerow([f'{futwal}'])
                

def check(discid):
    with open("./ids.csv", "r") as listid:
        listidreader = csv.DictReader(listid)
        for row in listidreader:
            if int(row["discordid"]) == discid:
                return True
        return False

def getid(discid):
    with open("./ids.csv", "r") as listid:
        listidreader = csv.DictReader(listid)
        for row in listidreader:
            if int(row["discordid"]) == discid:
                return row
        return False

def getlinesum(nline, discid):
    compts = 0
    discid = str(discid)
    for line in reversed(list(open(f"./data/{discid}.txt", "r"))):
            if compts == int(nline):
                return float(line.rstrip()[11:])
            else:
                compts = compts + 1
    return 1

def getlinestamp(nline, discid):
    discid = str(discid)
    comptst = 0
    for line in reversed(list(open(f"./data/{discid}.txt", "r"))):
        if comptst == int(nline):
            return (int(line.rstrip()[:10]) + 3600)
        else:
            comptst = comptst + 1
    return 1
    
def asset(asset, amount):
    try:
        amount = float(amount)
        price = amount * float(inter.get_avg_price(symbol=f'{asset}')["price"])
        return price
    except:
        return 0
    
def pricefromstamp(asset, timestmap):
    
    inter.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1MINUTE, "1608761399000", "1608761500000")