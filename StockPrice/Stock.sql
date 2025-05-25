create table Stock
(
    ticker  varchar(20)  not null
        primary key,
    name    varchar(255) not null,
    sector  varchar(255) null,
    country varchar(255) null
);

