create table if not exists adversarial (
    id integer PRIMARY KEY AUTOINCREMENT,
    hate_speech BOOLEAN not null default 0,
    offensive_language BOOLEAN not null default 0,
    tweet BLOB
    );