from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/transaction_details.json')
def transaction_details():
    return send_from_directory('static', 'transaction_details.json')

if __name__ == '__main__':
    app.run(debug=True)