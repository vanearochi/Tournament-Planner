#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import datetime


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def closeConnection(conn):
    """Close PostgreSQL database connection
    Args:
      conn: A database connection
    """
    conn.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Players(Name) VALUES (%s)""", (name,))
    conn.commit()
    closeConnection(conn)

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Select count(*) From Players;""")
    rows = cursor.fetchone()
    closeConnection(conn)
    return rows[0]


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Delete from Players;""")
    conn.commit()
    closeConnection(conn)


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Delete from Matches""")
    conn.commit()
    closeConnection(conn)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    datetime_now = datetime.datetime.now()
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Matches(Created, Winner, Loser) VALUES (%s, %s, %s);""", (
            datetime_now, winner, loser, ))
    conn.commit()
    closeConnection(conn)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""SElECT Players.id as Id, Players.name as Name,
                      COUNT(CASE WHEN Players.id=Matches.winner THEN 1 END) as win,
                      COUNT(Matches.id) as Played
                      FROM Players left outer join matches on (players.id = matches.winner or players.id= matches.loser)
                      GROUP BY Players.id, Players.name
                      ORDER BY win desc""")
    standing_list = cursor.fetchall()
    closeConnection(conn)
    return standing_list


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    player_standing = playerStandings()
    # Creates list of pairs from player_standing list
    # With a lil help from: http://stackoverflow.com/questions/2233204/how-does-zipitersn-work-in-python
    pairs_of_players = zip(*[iter(player_standing)] * 2)
    pairing_list = []
    for pair in pairs_of_players:
        player_1 = pair[0]
        player_2 = pair[1]
        pairing_list.append((player_1[0], player_1[1], player_2[0], player_2[1]))

    return pairing_list
