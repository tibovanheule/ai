create table if not exists lexicon (
    term varchar(150) PRIMARY KEY,
    average_offensiveness int not null default 0
    );

