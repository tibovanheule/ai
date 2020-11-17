create table if not exists model (
    name varchar PRIMARY KEY ,
    cat int not null default 0, /* 0= model, 1= vectorizer */
    model blob,
    status integer not null default 0           /* 0= ready, 1= in progress*/
    );

