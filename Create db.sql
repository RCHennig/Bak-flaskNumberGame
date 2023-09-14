create database PlayerData;
use PlayerData;

create table scores(
	id int8 not null auto_increment primary key,
    player char(15),
    score int8 not null
);

insert into scores(player,scores)
VALUES ('Ecdion187', 420)

insert into scores(player, scores)
VALUES ('Taxary69', 420)