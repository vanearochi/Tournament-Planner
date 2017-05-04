-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP TABLE IF EXISTS Players cascade;
DROP TABLE IF EXISTS Matches;


CREATE TABLE Players(
    Id SERIAL PRIMARY KEY,
    Name TEXT NOT NULL
       );

CREATE TABLE Matches(
    Id SERIAL PRIMARY KEY,
    Created timestamp with time zone NOT NULL,
    Winner INTEGER NOT NULL REFERENCES Players(id),
    Loser INTEGER NOT NULL REFERENCES Players(id)
    );










