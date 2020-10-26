create table if not exists data (
    id int PRIMARY KEY,
    hate_speech BOOLEAN not null default 0,
    offensive_language BOOLEAN not null default 0,
    tweet BLOB
    );