create table StockPrice
(
    id       int auto_increment
        primary key,
    date     date        not null,
    open     double      null,
    close    double      null,
    high     double      null,
    low      double      null,
    volume   int         null,
    stock_id varchar(20) null,
    constraint StockPrice_ibfk_1
        foreign key (stock_id) references Stock (ticker)
);

create index stock_id
    on StockPrice (stock_id);

