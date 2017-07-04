import requests
import pandas as pd
url = "https://api-fxtrade.oanda.com/v1/candles?instrument=EUR_USD&count=300&granularity=M10"
df = requests.get(url)
data = pd.read_json(df.text,orient='records')
a = data['candles'].tolist()
b = pd.DataFrame(a)
b.to_csv("e.csv")
