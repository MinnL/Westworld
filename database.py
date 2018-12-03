create database westworld;
use westworld;



create table trade (
	trade_id int not null,
    symbol_id int not null,
    action varchar(4),
    qty int,
    price decimal(12,2),
    time timestamp
    
);

create table symbol (
	symbol_id int ,
    coin_type char(3)
);

create table profit_loss(
	PL_id int not null,
    symbol_id int not null,
    qty int,
    VWAP decimal (12,2),
    RPL  decimal (12,2),
    URPL decimal (12,2)
);


insert into symbol values (1,'BIT'),(2,'ETH'),(3,'LTC')