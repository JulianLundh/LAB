create
    definer = julian@`%` function get_max_price_30d(sym varchar(20)) returns double deterministic
BEGIN
  DECLARE max_price DOUBLE;

  SELECT MAX(high) INTO max_price
  FROM StockPrice
  WHERE stock_id = sym AND date >= CURDATE() - INTERVAL 30 DAY;

  RETURN max_price;
END;

