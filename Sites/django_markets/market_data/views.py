from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import time
import json
import requests
import os
from .models import Candle
from .methods import crypto_symbols


def stock_candles(request, symbol):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(asset_class='stock', symbol=symbol, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        headers = {
            'APCA-API-KEY-ID': os.environ.get('ALPACA_KEY'),
            'APCA-API-SECRET-KEY': os.environ.get('ALPACA_SECRET')
        }

        start = (datetime.today() - timedelta(days=200)).date()
        end = (datetime.today() - timedelta(days=1)).date()
        r = requests.get('https://data.alpaca.markets/v2/stocks/' + symbol + '/bars?timeframe=1Day&start=' + str(start) + '&end=' + str(end), headers=headers)
        if r.status_code == 200:
            Candle.objects.filter(asset_class='stock', symbol=symbol.upper()).delete()
            response = r.text
            Candle.objects.create(symbol=symbol.upper(), asset_class='stock', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)

def crypto_candles(request, symbol):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(
        asset_class='crypto', symbol=symbol, date_added__gt=time_threshold)

    if record.exists():
        candles = record.latest('data').data
    else:
        Candle.objects.filter(asset_class='crypto', symbol=symbol).delete()
        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol.upper() + 'USDT&interval=1d')
        if r.status_code == 200:
            response = r.text
            list = json.loads(response)

            data = []
            for item in list:
                data.append([item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])])

            candles = json.dumps(data)
            Candle.objects.create(symbol=symbol.upper(), asset_class='crypto', data=candles)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(candles)

def forex_candles(request, pair):
    time_threshold = datetime.now() - timedelta(hours=5)
    record = Candle.objects.filter(asset_class='forex', symbol=pair, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        end = int(time.time())
        start = end - 331556952
        token = os.environ.get('FINNHUB_KEY')
        formatted = pair[:3] + '-' + pair[3:]
        r = requests.get('https://finnhub.io/api/v1/forex/candle?symbol=OANDA:' + formatted.upper() + '&resolution=D&from' + str(start) + '&to=' + str(end) + '&token=' + token)
        if r.status_code == 200:
            Candle.objects.filter(asset_class='forex', symbol=pair.upper()).delete()
            response = r.text
            Candle.objects.create(symbol=pair.upper(), asset_class='forex', data=response)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)


def crypto_pairs(request, pair):
    time_threshold = datetime.now() - timedelta(hours=1)
    record = Candle.objects.filter(asset_class='crypto_pairTTTT', symbol=pair, date_added__gt=time_threshold)

    if record.exists():
        response = record.latest('data').data
    else:
        symbol1 = pair[:3].upper()
        symbol2 = pair[3:].upper()

        pair_ticker = crypto_symbols()

        if symbol1 + symbol2 in pair_ticker:
            both = symbol1 + symbol2
            oneover = False
        elif symbol2 + symbol1 in pair_ticker:
            both = symbol2 + symbol1
            oneover = True
        else:
            return HttpResponse('invalid symbol', status=500)

        #determine ordering of symbols

        # params = json.loads(request.body)
        interval = '1m'

        r = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol1 + 'USDT&interval=' + interval)
        r2 = requests.get('https://www.binance.com/api/v3/klines?symbol=' + symbol2 + 'USDT&interval=' + interval)
        rx = requests.get('https://www.binance.com/api/v3/klines?symbol=' + both + '&interval=' + interval)

        if r.status_code == 200 and r2.status_code == 200 and rx.status_code == 200:
            list1 = json.loads(r.text)
            list2 = json.loads(r2.text)  
            listx = json.loads(rx.text)

            if len(list1) < len(list2):
                shortest = list1
            else:
                shortest = list2

            i = 0
            combined1 = []
            for item in shortest:
                combined1.append(
                    [
                        item[0], 
                        float(list1[i][1]) / float(list2[i][1]), 
                        float(list1[i][2]) / float(list2[i][2]),
                        float(list1[i][3]) / float(list2[i][3]),
                        float(list1[i][4]) / float(list2[i][4])
                    ]
                )
                i = i+1

            
            if len(combined1) < len(listx):
                shortest = combined1
            else:
                shortest = listx

            i = 0
            combinedx = []
            for item in shortest:
                if oneover:
                    x1 = 1 / float(listx[i][1])
                    x2 = 1 / float(listx[i][2])
                    x3 = 1 / float(listx[i][3])
                    x4 = 1 / float(listx[i][4])
                else:
                    x1 = float(listx[i][1])
                    x2 = float(listx[i][2])
                    x3 = float(listx[i][3])
                    x4 = float(listx[i][4])

                combinedx.append(
                    [
                        item[0],
                        float(combined1[i][1]) / x1,
                        float(combined1[i][2]) / x2,
                        float(combined1[i][3]) / x3,
                        float(combined1[i][4]) / x4
                    ]
                )
                i = i+1

            Candle.objects.filter(asset_class='crypto_pair', symbol=pair.upper()).delete()
            response = json.dumps(combinedx)
            Candle.objects.create(symbol=pair.upper(), asset_class='crypto_pair', data=combinedx)
        else:
            return HttpResponse(status=r.status_code)

    return HttpResponse(response)
