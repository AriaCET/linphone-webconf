drop table if exists entries;
create table entries (
id integer primary key autoincrement,
title string not null,
username number not null,
password string,
server string not null
);
create table auth (
username string not null,
password string not null
);
