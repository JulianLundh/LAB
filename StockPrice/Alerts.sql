create table Alerts
(
    id             int auto_increment
        primary key,
    date_triggered date         not null,
    condition_met  varchar(255) not null,
    stock_id       varchar(20)  null,
    constraint Alerts_ibfk_1
        foreign key (stock_id) references Stock (ticker)
);

create index stock_id
    on Alerts (stock_id);

