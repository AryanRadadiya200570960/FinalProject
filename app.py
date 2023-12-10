from flask import Flask, render_template, Response
#from requests import Request, Session
#from requests.exceptions import ConnectionError, Timeout
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pymongo import MongoClient
import json
import time
import io
import pandas as pd

client = MongoClient("mongodb+srv://aryanrada0:aryan@final-project.yvhczbt.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('crypto')
records = db.crypto
data = records.find({}, {'data'})
data = pd.json_normalize(data[0]['data'], meta=['id', 'name', 'symbol', 'slug', 'total_supply', ['quote', 'USD', 'price']])
data = data.drop(columns=['platform.token_address', 'platform.slug', 'platform.symbol', 'platform.name', 'platform.id', 'id', 'num_market_pairs', 'date_added', 'tags', 'quote.USD.tvl', 'quote.USD.last_updated', 'quote.USD.market_cap_dominance', 'quote.USD.percent_change_90d', 'quote.USD.percent_change_60d', 'quote.USD.percent_change_30d', 'quote.USD.percent_change_7d', 'quote.USD.percent_change_1h', 'quote.USD.volume_change_24h', 'last_updated', 'tvl_ratio', 'self_reported_market_cap', 'self_reported_circulating_supply', 'cmc_rank', 'platform', 'max_supply', 'circulating_supply', 'quote.USD.market_cap', 'quote.USD.fully_diluted_market_cap', 'slug'])
top10 = data.head(10)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google-charts/piechart')
def google_piechart():
    #data = {'Task': 'Hours per Day', 'work': 11, 'Eat': 2, 'Commute': 2, 'Watching TV': 2, 'Sleeping': 7}
    pie = data.groupby('infinite_supply').count()
    pie = pie.set_index('pie.index')
    labels = [row[0] for row in pie]
    values = [row[1] for row in pie]
    return render_template('PieChart.html', labels=labels, values=values)

@app.route('/google-charts/linechart')
def google_linechart():
    return render_template('LineChart.html')

@app.route('/linechart.png')
def line_chart():
    fig = plt.subplots()
    fig.bar(top10['symbol'], top10['total_supply'], align='center')
    fig.set_title('Coefficent of Thermal Expansion (CTE) of Three Metals')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/google-charts/barchart')
def google_barchart():
    return render_template('BarChart.html')

if __name__ == "__main__":
    app.run()   