-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
--DROP TABLE IF EXISTS Players;
--DROP TABLE IF EXISTS Matches;
--DROP TABLE IF EXISTS Rounds;

CREATE TABLE Players(
    Id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    Name VARCHAR(40) NOT NULL
       );

CREATE TABLE Matches(
    Id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    Created timestamp with time zone,
    RoundId INTEGER,
    Player1Id INTEGER NOT NULL,
    Player2Id INTEGER NOT NULL,
    Winner INTEGER
    );

CREATE TABLE Rounds(
    id SERIAL PRIMARY KEY UNIQUE NOT NULL,
    Number INTEGER NOT NULL
);




--CREATE TABLE Winner(
--    GroupID INTEGER NOT NULL,
--    Player1 INTEGER NOT NULL,
--    Player2 INTEGER NOT NULL,
--    Winner INTEGER NOT NULL
--    );









