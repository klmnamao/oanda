import requests
import json
import csv
import pandas as pd
import time
from sklearn.ensemble import RandomForestRegressor
from numpy import *
import random
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

def hisdata(n):
    url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=5000&granularity=M10"
    res = requests.get(url)
    data = pd.read_json(res.text,orient='records')
    a = data['candles'].tolist()
    b = pd.DataFrame(a)
    b=b.drop(['complete','time'],1)
    while n>1:
        b[str(n)+"ema"] = b['closeAsk'].ewm(span = n, min_periods=n).mean()
        #df[str(n)+"ma"] = df['Close'].rolling(n).mean()
        n = n-1
    return b
def cd(df,n,m,l):
    try:
        temp = df.copy()
        temp['dif'] = temp[str(n)+'ema']-temp[str(m)+'ema']
        temp['difema'] = temp['dif'].ewm(span=l, min_periods =l).mean()
        temp['decision'] = temp['dif']-temp['difema']
        temp['result'] = temp['decision']*temp['decision'].shift(1)
        mon = []
        for index, row in temp.iterrows():
            if (row['result']<0 and row['decision']>0):
                mon.append(-2*row['closeAsk'])
            elif (row['result']<0 and row['decision']<0):
                mon.append(2*row['closeBid'])
            else:
                mon.append(0)
        temp['money']=mon
        money = [i for i in mon if i!=0]
        if money[0]*money[-1]>0:
            money.pop()
        money[0] = money[0]/2
        money[-1] = money[-1]/2
        return sum(money),temp
    except:
        return -1,-1
def cd1(df,n,m,l):
        temp = df.copy()
        temp['dif'] = temp[str(n)+'ema']-temp[str(m)+'ema']
        temp['difema'] = temp['dif'].ewm(span=l, min_periods =l).mean()
        temp['decision'] = temp['dif']-temp['difema']
        temp['result'] = temp['decision']*temp['decision'].shift(1)
        mon = []
        for index, row in temp.iterrows():
            if (row['result']<0 and row['decision']>0 and row['dif']<0):
                mon.append(-2*row['closeAsk'])
            elif (row['result']<0 and row['decision']<0 and row['dif']>0):
                mon.append(2*row['closeBid'])
            else:
                mon.append(0)
        temp['money']=mon
        money = [i for i in mon if i!=0]
        a=1
        while a < len(money):
            if (money[a]*money[a-1]) >0:
                money.pop(a)
            else:
                a=a+1

        if len(money) !=0:            
            if money[0]*money[-1]>0:
                money.pop()
            money[0] = money[0]/2
            money[-1] = money[-1]/2
            
            return sum(money),temp
        else:
            return 0, temp

def decision(n,m,l,counter):
        url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=300&granularity=M10"
        df = requests.get(url)
        data = pd.read_json(df.text,orient='records')
        a = data['candles'].tolist()
        b = pd.DataFrame(a)
        b=b.drop(['complete','time'],1)
        i=100
        while i>1:
            b[str(i)+"ema"] = b['closeAsk'].ewm(span = i, min_periods=i).mean()
            #df[str(n)+"ma"] = df['Close'].rolling(n).mean()
            i = i-1
        temp = b.copy()
        temp['dif'] = temp[str(n)+'ema']-temp[str(m)+'ema']
        temp['difema'] = temp['dif'].ewm(span=l, min_periods =l).mean()
        temp['decision'] = temp['dif']-temp['difema']
        temp['result'] = temp['decision']*temp['decision'].shift(1)
        temp.to_csv('temp.csv')
        if (temp.iloc[-1]['result']<0 and temp.iloc[-1]['decision']>0):
            if counter == 0:
                buy(50000)
                counter = 1
            elif counter == -1:
                buy(100000)
                counter = 1
            print('buy')
        elif (temp.iloc[-1]['result']<0 and temp.iloc[-1]['decision']<0):
            if counter == 0:
                sell(50000)
                counter = -1
                
            elif counter == 1:
                sell(100000)
                counter = -1
            print('sell')
        else:
            print('not triggered')
        return counter,temp.iloc[-1]['dif'],temp.iloc[-1]['difema'],temp.iloc[-1]['closeAsk'],temp.iloc[-1]['closeAsk']
def sample(df):
    df1 = df.copy()
    a = random.randint(100,300)
    df1 = df1.loc[a:a+1000]
    return df1
def val_sample(df):
    df1 = df.copy()
    a = random.randint(300,600)
    df1 = df1.loc[a:a+1000]
    return df1
df1 = hisdata(100)
df1.dropna(inplace = True)
index = [0,1,2,3,4]
#initial members
li = [[12,26,5], [6,20,10], [8,20,7], [4,12,7], [5,10,8]]
rev = []
count = []
for i in range(0,1000):
        print(i)    
        a = random.sample(set(index), 2)
        sampledata = sample(df1)
        r0,temp = cd1(sampledata,li[a[0]][0],li[a[0]][1],li[a[0]][2])
        r1,temp = cd1(sampledata,li[a[1]][0],li[a[1]][1],li[a[1]][2])
        if r0 > r1:
            c = li[a[0]].copy()            
            c[0] = c[0]+random.randint(-2,2)
            c[1] = c[1]+random.randint(-2,2)
            c[2] = c[2]+random.randint(-2,2)
            if c[0] > 1 and c[1] > 1 and c[2]>1:
                li.remove(li[a[1]])
                li.append(c)
        else:
            c = li[a[1]].copy()            
            c[0] = c[0]+random.randint(-2,2)
            c[1] = c[1]+random.randint(-2,2)
            c[2] = c[2]+random.randint(-2,2)
            if c[0] > 1 and c[1] > 1 and c[2]>1:
                li.remove(li[a[0]])
                li.append(c)
        if (r0 != -1 and r1 != -1):
            rev.append((r0+r1)/2)
            count.append(i)
        print(li)
        print(r0,r1)
prof=[]
for i in range (0, 50):
    sample_validation = val_sample(df1)
    r,temp = cd1(sample_validation, li[0][0], li[0][1], li[0][2])
    prof.append(r)
    print (r)
    temp.to_csv("temp.csv")
print(sum(prof)/50)
