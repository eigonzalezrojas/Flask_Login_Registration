create database if not exists `geeklogin` default character set utf8 collate utf8_general_ci;

use `geeklogin`;

create table if not exists `accounts`(
	`id` int (11) not null auto_increment,
    `username` varchar(50) not null,
    `password` varchar(255) not null,
    `email` varchar(100) not null,
    primary key (`id`)
);

