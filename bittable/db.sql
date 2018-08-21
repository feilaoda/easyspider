drop table market_rate;
CREATE TABLE `market_rate` (
  `name` varchar(20) NOT NULL COMMENT '自增主键',
  `rate` decimal(10,4) NOT NULL,
  KEY `idx_name` (`name`) USING BTREE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



drop table market_site;
CREATE TABLE `market_site` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `name` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  url varchar(255) NOT NULL,
  logo varchar(255) NOT NULL,
  KEY `idx_name` (`name`) USING BTREE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

drop table market_symbol;
CREATE TABLE `market_symbol` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `name` varchar(10) NOT NULL,
  `coin_id` int NULL,
  base_currency varchar(10) NOT NULL,
  quote_currency varchar(10) NOT NULL,
  price_decimal int ,
  amount_decimal int,
  KEY `idx_name` (`name`) USING BTREE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

drop table market_trade_min;
CREATE TABLE `market_trade_min` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `coin_id` int NULL,
  `symbol_id` int NULL,
  `site_id` int not null,
  tid bigint not null,
  data_type int default 0,
  price_date timestamp not null,
  `price_btc` decimal(18,8) DEFAULT NULL,
  `price_usd` decimal(18,8) DEFAULT NULL,
  price_open decimal(18,8) DEFAULT NULL COMMENT '开',
  price_close decimal(18,8) DEFAULT NULL COMMENT '收',
  price_high decimal(18,8) DEFAULT NULL COMMENT '高',
  price_low decimal(18,8) DEFAULT NULL COMMENT '低',
  volume bigint default null COMMENT '量',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  KEY `idx_coin_id` (`coin_id`) USING BTREE,
  KEY `idx_site_id` (`site_id`) USING BTREE,
  KEY `idx_tid` (`tid`) USING BTREE,
  KEY `data_type` (`data_type`) ,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


insert into market_site(name) values ('coinmarketcap');
insert into market_symbol(name) values ('bitcoin');
insert into market_symbol(name) values ('litecoin');
insert into market_symbol(name) values ('ethereum');
insert into market_symbol(name) values ('eos');


drop table market_coin;
CREATE TABLE `market_coin` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  name varchar(64) NOT NULL,
  title varchar(64) NOT NULL,
  symbol varchar(10),
  uri varchar(255) NULL,
  logo varchar(255) NULL,
  rank int null,
  market_cap bigint DEFAULT null,
  price  decimal(18,8) DEFAULT null,
  volume bigint DEFAULT null,
  supply  bigint default null,
  total_supply  bigint default null,
  change7d decimal(12,4) DEFAULT null,
  change24h decimal(12,4) DEFAULT null,
  change12h decimal(12,4) DEFAULT null,
  change6h decimal(12,4) DEFAULT null,
  change4h decimal(12,4) DEFAULT null,
  change2h decimal(12,4) DEFAULT null,
  change1h decimal(12,4) DEFAULT null,
  src varchar(255) NULL,
  website varchar(255) NULL,
  browser1 varchar(255) NULL,
  browser2 varchar(255) NULL,
  browser3 varchar(255) NULL,

  updated_at datetime DEFAULT CURRENT_TIMESTAMP COMMENT 'Update时间',
  KEY `idx_name` (`name`) USING BTREE,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

alter table market_coin add column src varchar(255) NULL;
alter table market_coin add column website varchar(255) NULL;
alter table market_coin add column browser1 varchar(255) NULL;
alter table market_coin add column browser2 varchar(255) NULL;
alter table market_coin add column browser3 varchar(255) NULL;
