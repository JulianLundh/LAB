from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="",
        user="",
        password="",
        database="StockPrice"
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prices')
def prices():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sector = request.args.get('sector')
    country = request.args.get('country')
    ticker = request.args.get('ticker')

    query = '''
        SELECT s.ticker, s.name, s.sector, s.country, sp.close, sp.date
        FROM Stock s
        JOIN (
            SELECT stock_id, MAX(date) AS max_date
            FROM StockPrice
            GROUP BY stock_id
        ) latest ON s.ticker = latest.stock_id
        JOIN StockPrice sp ON sp.stock_id = latest.stock_id AND sp.date = latest.max_date
        WHERE 1=1
    '''
    params = []
    if sector:
        query += " AND s.sector = %s"
        params.append(sector)
    if country:
        query += " AND s.country = %s"
        params.append(country)
    if ticker:
        query += " AND s.ticker LIKE %s"
        params.append(f"%{ticker}%")

    query += " ORDER BY sp.date DESC LIMIT 100"

    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return render_template('prices.html', stocks=data)

@app.route('/alerts')
def alerts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.date_triggered, a.condition_met, s.name, s.ticker
        FROM Alerts a
        JOIN Stock s ON a.stock_id = s.ticker
        WHERE a.date_triggered >= CURDATE() - INTERVAL 14 DAY
        ORDER BY a.date_triggered DESC
    """)
    alerts = cursor.fetchall()
    conn.close()
    return render_template('alerts.html', alerts=alerts)

@app.route('/volatility', methods=['GET', 'POST'])
def volatility():
    result = None
    symbol = request.form.get('ticker') if request.method == 'POST' else None
    if symbol:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT calculate_volatility(%s)", (symbol,))
        row = cursor.fetchone()
        result = row[0] if row and row[0] is not None else None
        conn.close()
    return render_template('volatility.html', result=result, symbol=symbol)

@app.route('/volume')
def volume():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT stock_id, ROUND(AVG(volume), 0) AS avg_volume
        FROM StockPrice
        WHERE date >= CURDATE() - INTERVAL 30 DAY
        GROUP BY stock_id
        ORDER BY avg_volume DESC
        LIMIT 50
    """)
    volumes = cursor.fetchall()
    conn.close()
    return render_template('volume.html', volumes=volumes)

@app.route('/maxprice', methods=['GET', 'POST'])
def maxprice():
    result = None
    symbol = request.form.get('ticker') if request.method == 'POST' else None
    if symbol:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT get_max_price_30d(%s)", (symbol,))
        row = cursor.fetchone()
        result = row[0] if row and row[0] is not None else None
        conn.close()
    return render_template('maxprice.html', result=result, symbol=symbol)

@app.route('/lowavg', methods=['GET', 'POST'])
def lowavg():
    results = []
    threshold = request.form.get('threshold')
    if request.method == 'POST' and threshold:
        try:
            value = float(threshold)
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.callproc('get_low_avg_prices', [value])
            for res in cursor.stored_results():
                results = res.fetchall()
            conn.close()
        except ValueError:
            results = []
    return render_template('lowavg.html', results=results, threshold=threshold)


if __name__ == '__main__':
    app.run(debug=True)
