Before first run, setup login details to your database in app.py & import yfinance as yf.py
Make sure you have a database called "StockPrice" or another chosen name. 

Exampel bellow!
conn = mysql.connector.connect(
    host="100.100.100.100",
    user="username",
    password="password",
    database="StockPrice"
)
