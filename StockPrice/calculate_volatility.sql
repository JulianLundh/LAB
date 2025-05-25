create
    definer = julian@`%` function calculate_volatility(sym varchar(10)) returns float deterministic
BEGIN
  DECLARE result FLOAT;
  SELECT STDDEV_SAMP(close)
  INTO result
  FROM StockPrice
  WHERE stock_id = sym AND date >= CURDATE() - INTERVAL 30 DAY;
  RETURN result;
END;

