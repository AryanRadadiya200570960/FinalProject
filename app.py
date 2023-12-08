from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google-charts/piechart')
def google_piechart():
    return render_template('PieChart.html')

@app.route('/google-charts/linechart')
def google_linechart():
    return render_template('LineChart.html')

@app.route('/google-charts/barchart')
def google_barchart():
    return render_template('BarChart.html')

if __name__ == "__main__":
    app.run()   