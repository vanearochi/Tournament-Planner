-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE tournament(
    ID INTEGER PRIMARY KEY NOT NULL,
    Tournament VARCHAR(40) NOT NULL,
    Name VARCHAR(40) NOT NULL
       );

CREATE TABLE Winner(
    GroupID INTEGER NOT NULL,
    Player1 INTEGER NOT NULL,
    Player2 INTEGER NOT NULL,
    Winner INTEGER NOT NULL
    );
--DROP TABLE IF EXISTS tournament;
--DROP TABLE IF EXISTS Winner;






