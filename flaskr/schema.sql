DROP table if exists post;
DROP TABLE IF EXISTS user;
create table user(
    id integer primary key auto_increment,
    username varchar(100) unique not null,
    password TEXT not null
);
create table post(
    id integer primary key auto_increment,
    author_id integer not null,
    createdAt timestamp not null default current_timestamp,
    title varchar(100) not null,
    body text not null,
    foreign key (author_id) references user(id)
);