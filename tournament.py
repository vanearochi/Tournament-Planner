#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2


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
    cursor.execute("""Select * from Players order by Id ASC""")
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
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Matches(Winner, Loser) VALUES ({Winner}, {Loser})""".format(Winner=winner, Loser=loser, ))
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
    cursor.execute("""SELECT * from Players """)
    cursor.execute("""SElect * from Matches""")
    matches_played = cursor.fetchall()

    if len(matches_played) == 0:
        # With a lil help from: http://stackoverflow.com/questions/4138734/how-to-return-0-if-table-empty-1-otherwise
        # If matches table is empty performs a query that checks if table is empty and returns 0 for the selected row
        cursor.execute("""SELECT players.id, players.name,
                          CASE
                            WHEN EXISTS (SELECT matches.winner FROM matches LIMIT 1) THEN 1 ELSE 0 END,
                          CASE
                           WHEN EXISTS (SELECT matches.id FROM matches LIMIT 1) THEN 1 ELSE 0 END from players
                            """)
        standing_list = cursor.fetchall()
        closeConnection(conn)
        return standing_list
    else:
        # If matches table is not empty performs a query that count the number of wined matches and played matches
        cursor.execute(
            """SELECT players.id, players.name,
               COUNT(CASE WHEN players.id=matches.winner THEN 1 END) as wins,
               Count(CASE WHEN players.id=matches.winner or players.id=matches.loser THEN 1 END) as played from matches,
               players GROUP BY players.name, players.id order by wins DESC;""")
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
