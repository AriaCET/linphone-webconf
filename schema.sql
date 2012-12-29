drop table if exists entries;
create table entries (
id integer primary key autoincrement,
title string not null,
username number not null,
password string,
wait-time number not null,
server string not null
);
