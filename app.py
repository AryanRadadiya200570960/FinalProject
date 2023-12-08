from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google-charts/piechart')
def google_piechart():
    return render_template('PieChart.html')

if __name__ == "__main__":
    app.run()   