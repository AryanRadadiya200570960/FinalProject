from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout
from flask import Flask, render_template, Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pandas as pd
import time

client = MongoClient("mongodb+srv://aryanrada0:aryan@final-project.yvhczbt.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('crypto')
records = db.crypto

#Fetching data from API and storing it in cloud server
#it will fetch data every 24 hours
while True:
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start':'1',
      'limit':'100',
      'convert':'USD'
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': '60074b30-5b62-4b4a-8d2e-2e9638817673',
    }

    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        records.insert_one(data)
        time.sleep(86400)
else:
    exit()

data = records.find({}, {'data'})
data = pd.json_normalize(data[0]['data'], meta=['id', 'name', 'symbol', 'slug', 'total_supply', ['quote', 'USD', 'price']])
data = data.drop(columns=['platform.token_address', 'platform.slug', 'platform.symbol', 'platform.name', 'platform.id', 'id', 'num_market_pairs', 'date_added', 'tags', 'quote.USD.tvl', 'quote.USD.last_updated', 'quote.USD.market_cap_dominance', 'quote.USD.percent_change_90d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_1h', 'quote.USD.volume_change_24h', 'last_updated', 'tvl_ratio', 'self_reported_market_cap', 'self_reported_circulating_supply', 'cmc_rank', 'platform', 'max_supply', 'circulating_supply', 'quote.USD.market_cap', 'quote.USD.fully_diluted_market_cap', 'slug'])

#Pie Chart
pie = data.groupby('infinite_supply').count()
pie = pie['name'].to_dict()
values = pie.items()
pie = {str(key): value for key, value in values}
pie_data = {"Infinite Supply": "Values"}
pie_data.update(pie)

#Column Chart
top10 = data.head(10)
top10 = top10.loc[:, ['symbol', 'quote.USD.percent_change_24h']]
top10 = top10.set_index('symbol')
top = top10.to_dict()
top = top['quote.USD.percent_change_24h']
column_data = {"Symbol": "Percentage Change"}
column_data.update(top)

#Bar Chart
top10 = data.head(10)
top10 = top10.loc[:, ['symbol', 'total_supply']]
top10 = top10.set_index('symbol')
top = top10.to_dict()
top = top['total_supply']
bar_data = {"Symbol": "Total Supply"}
bar_data.update(top)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html', data=pie_data, data1=column_data, data2=bar_data)

@app.route('/google-charts/piechart')
def google_piechart():
    return render_template('PieChart.html', data=pie_data)

@app.route('/google-charts/columnchart')
def google_columnchart():
    return render_template('ColumnChart.html', data=column_data)

@app.route('/google-charts/barchart')
def google_barchart():
    return render_template('BarChart.html', data=bar_data)

if __name__ == "__main__":
    app.run()   