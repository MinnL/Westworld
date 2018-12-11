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
    qty decimal12,2),
    price decimal(12,2),
    time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    balance decimal(12,2),
    primary key(trade_id) 
);

create table symbol (
	symbol_id int ,
    coin_type char(3)
);

create table profit_loss(
    PL_id int not null auto_increment,
    symbol_id int,
    inventory int,
    VWAP decimal (12,2),
    RPL  decimal (12,2),
    URPL decimal (12,2),
    time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    primary key(PL_id)
);

create table graph(
  graph_id int not null auto_increment,
  symbol_id int,
  RPL  decimal (12,2),
  URPL decimal (12,2),
  time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  primary key(graph_id)
  );

insert into profit_loss (symbol_id,inventory,VWAP,RPL,URPL) values (1,0,0,0,0);
insert into profit_loss (symbol_id,inventory,VWAP,RPL,URPL) values (2,0,0,0,0);
insert into profit_loss (symbol_id,inventory,VWAP,RPL,URPL) values (3,0,0,0,0);

insert into symbol values (1,'BTC'),(2,'ETH'),(3,'LTC')
