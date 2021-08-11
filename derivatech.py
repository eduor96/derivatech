# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 13:28:15 2021

@author: eduor
"""

import requests
import pandas as pd
import numpy as np
import time
import math
from datetime import datetime


def ejecutar(ticker, tiempo, n, dic, now, fecha):
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                            params={'symbol': {ticker}, 'expiration': {fecha}, 'greeks': 'true'},
                            headers={'Authorization': 'Bearer 3tSIHJuBQJHanpGLncQYzSp6WGeU',
                                     'Accept': 'application/json'}
                            )
    json_response1 = response.json()

    response = requests.get('https://sandbox.tradier.com/v1/markets/quotes',
                            params={'symbols': {ticker}, 'greeks': 'false'},
                            headers={'Authorization': 'Bearer 3tSIHJuBQJHanpGLncQYzSp6WGeU',
                                     'Accept': 'application/json'}
                            )
    json_response = response.json()

    spot = (math.floor(json_response["quotes"]["quote"]['last']))

    for i in range(len(json_response1["options"]["option"])):
        if (json_response1["options"]["option"][i]["strike"]) == spot:
            v1 = i - 10
            v2 = i + 10
    num = v2 - v1
    lista = ["underlying", "option_type", "strike", "volume", "greeks", "bid", "ask", "expiration_date"]
    # lista=np.transpose(lista)
    data = np.empty((num, len(lista)))
    df = pd.DataFrame(data, columns=lista)

    for j in range(len(lista)):
        for i in range(v1, v2):
            df[lista[j]][i - v1] = str(json_response1["options"]["option"][i][lista[j]])

    df = df.assign(Spot=json_response["quotes"]["quote"]['last'])
    df = df.assign(Tiempo=now)
    dic[t] = df
    # print(json_response["quotes"]["quote"]['last'])
    time.sleep(tiempo)
    print(t)


ticker = "AAPL"
fecha = ["2021-08-13", "2021-08-20"]
texto = "n"
n = 0 #hola
dic = {}
# while True:
for i in range(1):
    t = texto + str(n)
    now = datetime.now()
    ejecutar(ticker, 10, t, dic, now, fecha[0])
    n = n + 1