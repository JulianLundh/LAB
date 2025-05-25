import mysql.connector
import yfinance as yf
import math
from datetime import datetime


conn = mysql.connector.connect(
    host="",
    user="",
    password="",
    database="StockPrice"
)
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Stock (
    ticker VARCHAR(20) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(255),
    country VARCHAR(255)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS StockPrice (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    open DOUBLE,
    close DOUBLE,
    high DOUBLE,
    low DOUBLE,
    volume INT,
    stock_id VARCHAR(20),
    FOREIGN KEY (stock_id) REFERENCES Stock(ticker)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Alerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date_triggered DATE NOT NULL,
    condition_met VARCHAR(255) NOT NULL,
    stock_id VARCHAR(20),
    FOREIGN KEY (stock_id) REFERENCES Stock(ticker)
)
''')


companies_and_tickers = [
    ("Walmart", "WMT"),
    ("Amazon.com", "AMZN"),
    ("State Grid", "SGCC"),
    ("Saudi Aramco", "2222.SR"),
    ("Sinopec", "SNP"),
    ("China National Petroleum", "PTR"),
    ("Apple", "AAPL"),
    ("UnitedHealth", "UNH"),
    ("Berkshire Hathaway", "BRK-B"),
    ("CVS Health", "CVS"),
    ("Volkswagen", "VOW3.DE"),
    ("ExxonMobil", "XOM"),
    ("Shell", "SHEL"),
    ("China State Construction Engineering", "601668.SS"),
    ("Toyota Motor", "7203.T"),
    ("McKesson", "MCK"),
    ("Alphabet", "GOOGL"),
    ("Cencora", "COR"),
    ("Trafigura", "TRAF"),
    ("Costco Wholesale", "COST"),
    ("JPMorgan Chase", "JPM"),
    ("ICBC", "1398.HK"),
    ("TotalEnergies", "TOT"),
    ("Glencore", "GLEN.L"),
    ("BP", "BP"),
    ("Microsoft", "MSFT"),
    ("Cardinal Health", "CAH"),
    ("Stellantis", "STLA"),
    ("Chevron", "CVX"),
    ("China Construction Bank", "0939.HK"),
    ("Samsung Electronics", "005930.KS"),
    ("Foxconn", "2317.TW"),
    ("CIGNA", "CI"),
    ("Agricultural Bank of China", "1288.HK"),
    ("China Railway Engineering", "601390.SS"),
    ("Ford Motor", "F"),
    ("Bank of China", "3988.HK"),
    ("Bank of America", "BAC"),
    ("General Motors", "GM"),
    ("Elevance Health", "ELV"),
    ("BMW Group", "BMW.DE"),
    ("Mercedes-Benz Group", "MBG.DE"),
    ("China Railway Construction", "601186.SS"),
    ("China Baowu Steel Group", "600019.SS"),
    ("Citigroup", "C"),
    ("Centene", "CNC"),
    ("JD.com", "JD"),
    ("Home Depot", "HD"),
    ("Électricité de France", "EDF.PA"),
    ("Marathon Petroleum", "MPC"),
    ("Kroger", "KR"),
    ("Phillips 66", "PSX"),
    ("Ping An Insurance", "2318.HK"),
    ("Sinochem", "600500.SS"),
    ("China Mobile", "0941.HK"),
    ("China National Offshore Oil", "0883.HK"),
    ("Honda Motor", "7267.T"),
    ("Fannie Mae", "FNMA"),
    ("China Life Insurance", "2628.HK"),
    ("Walgreens Boots Alliance", "WBA"),
    ("Valero Energy", "VLO"),
    ("Banco Santander", "SAN"),
    ("China Communications Construction", "601800.SS"),
    ("BNP Paribas", "BNP.PA"),
    ("Mitsubishi Motors", "7211.T"),
    ("Meta Platforms", "META"),
    ("HSBC", "HSBC"),
    ("Verizon", "VZ"),
    ("China Minmetals", "1208.HK"),
    ("Alibaba Group", "BABA"),
    ("CITIC Group", "0267.HK"),
    ("China Resources", "0291.HK"),
    ("Hyundai Motor", "005380.KS"),
    ("AT&T", "T"),
    ("Shandong Energy Group", "602730.SS"),
    ("Comcast", "CMCSA"),
    ("Deutsche Telekom", "DTE.DE"),
    ("China Southern Power Grid", "600292.SS"),
    ("Uniper", "UN01.DE"),
    ("Wells Fargo", "WFC"),
    ("Hengli Group", "600346.SS"),
    ("Allianz", "ALV.DE"),
    ("China Post", "600763.SS"),
    ("China Energy Investment", "601868.SS"),
    ("Xiamen C & D", "600383.SS"),
    ("Reliance Industries", "RELIANCE.NS"),
    ("Goldman Sachs", "GS"),
    ("Freddie Mac", "FMCC"),
    ("Rosneft", "ROSN.ME"),
    ("Target Corporation", "TGT"),
    ("Equinor", "EQNR"),
    ("Humana Inc.", "HUM"),
    ("SAIC Motor", "600104.SS"),
    ("State Farm", "STF"),
    ("Life Insurance Corporation of India", "LICI.NS"),
    ("Nestlé", "NESN.SW"),
    ("Enel", "ENEL.MI"),
    ("Eni", "ENI.MI"),
    ("Petrobras", "PBR"),
    ("SK Hynix", "000660.KS")
]


def fetch_and_insert_data():
    for company_name, ticker in companies_and_tickers:
        try:
            print(f"[...] Hämtar data för {ticker}")

            stock = yf.Ticker(ticker)
            info = stock.info

            sector = info.get('sector', 'Unknown')
            country = info.get('country', 'Unknown')


            cursor.execute('''
            INSERT IGNORE INTO Stock (ticker, name, sector, country)
            VALUES (%s, %s, %s, %s)
            ''', (ticker, company_name, sector, country))

            recent_data = stock.history(period="15d")


            if len(recent_data) >= 14:
                old_price = recent_data.iloc[0]      
                current_price = recent_data.iloc[-1]  

                if old_price["Close"] > 0:
                    change = ((current_price["Close"] - old_price["Close"]) / old_price["Close"]) * 100

                    alert_type = None
                    if change >= 20:
                        alert_type = "↑ +20%"
                    elif change >= 10:
                        alert_type = "↑ +10%"
                    elif change >= 5:
                        alert_type = "↑ +5%"
                    elif change <= -20:
                        alert_type = "↓ -20%"
                    elif change <= -10:
                        alert_type = "↓ -10%"
                    elif change <= -5:
                        alert_type = "↓ -5%"

                    if alert_type:
                        alert_text = f"{alert_type} change over 14d for {company_name} ({ticker})"
                        cursor.execute('''
                        INSERT INTO Alerts (date_triggered, condition_met, stock_id)
                        VALUES (%s, %s, %s)
                        ''', (datetime.now().date(), alert_text, ticker))


            stock_data = stock.history(period="1y")
            for index, row in stock_data.iterrows():

                volume_value = row['Volume']
                if isinstance(volume_value, float) and math.isnan(volume_value):
                    volume = 0
                else:
                    volume = int(volume_value)

                cursor.execute('''
                INSERT INTO StockPrice (date, open, close, high, low, volume, stock_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    index.date(),
                    row['Open'],
                    row['Close'],
                    row['High'],
                    row['Low'],
                    volume,
                    ticker
                ))

            print(f"[✓] Klar med {ticker}")

        except Exception as e:
            print(f"[X] Fel med {ticker}: {e}")

    conn.commit()
    conn.close()
    print("✅ All data inlagd och anslutning stängd.")


fetch_and_insert_data()
