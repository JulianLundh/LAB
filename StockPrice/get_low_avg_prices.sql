create
    definer = julian@`%` procedure get_low_avg_prices(IN max_price double)
BEGIN
  SELECT s.ticker, s.name, ROUND(AVG(sp.close), 2) AS avg_close
  FROM Stock s
  JOIN StockPrice sp ON s.ticker = sp.stock_id
  WHERE sp.date >= CURDATE() - INTERVAL 30 DAY
  GROUP BY s.ticker, s.name
  HAVING avg_close < max_price
  ORDER BY avg_close ASC;
END;

