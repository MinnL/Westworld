# Westworld
crypto currency trading system

Please type in the following in commend line:
pip3 install coinbase
pip install plotly

Please type in the following in MYSQl to create a database and tables. 

create database westworld;
use westworld;
create table trade (
	trade_id int not null auto_increment,
    symbol_id int,
    action varchar(4),
    qty int,
    price decimal(12,2),
    time timestamp,
    inventory int,
    cash decimal(12,2),
    primary key(trade_id) 
);

create table symbol (
	symbol_id int ,
    coin_type char(3)
);

create table profit_loss(
	PL_id int not null auto_increment,
    symbol_id int,
    qty int,
    VWAP decimal (12,2),
    RPL  decimal (12,2),
    URPL decimal (12,2),
    time timestamp,
    primary key(PL_id)
);

insert into symbol values (1,'BTC'),(2,'ETH'),(3,'LTC')
