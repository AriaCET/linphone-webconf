drop table if exists entries;
create table entries (
id integer primary key autoincrement,
title string not null,
username number not null,
password string,
waittime number not null,
server string not null
);
