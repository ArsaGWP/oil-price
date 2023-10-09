from suds.client import Client
import xmltodict, json
import pandas as pd
import requests

client = Client('https://orapiweb.pttor.com/oilservice/OilPrice.asmx?WSDL')
oil_price = client.service.CurrentOilPrice(Language='thai')
price = xmltodict.parse(oil_price)
thai_oil = eval(json.dumps(price))

df = pd.DataFrame(thai_oil['PTTOR_DS']['FUEL'])
df = df.dropna()

url = 'https://notify-api.line.me/api/notify'
token = '3NPXyBKS2dFYYItVssGfCVf8AoRBud6wfKMiEgFzmOH'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
msg = "\nวันที่ : {} \nGasoline 95 : {} บาท\nGasohol 95 : {} บาท\nGasohol 91 : {} บาท\nPremium Diesel B7 : {} บาท\nDiesel B7 : {} บาท\nNGV : {} บาท".format(df.iloc[0,0], df.iloc[0,2], df.iloc[5,2], df.iloc[2,2],df.iloc[8,2], df.iloc[1,2], df.iloc[4,2])
r = requests.post(url, headers=headers, data ={'message':msg})

print(r.text)