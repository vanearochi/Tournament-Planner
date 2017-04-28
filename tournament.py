#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import math


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


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
    print cursor.fetchall()
    # cursor.execute("""Select PlayerId From Players Where Name = %s """, (name,))
    # player_id = cursor.fetchone()
    # cursor.execute("""INSERT INTO Pairings(Round, PlayerId) VALUES (%s, %s)""", (1, player_id))
    # conn.commit()
registerPlayer("a")


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Select count(*) From Players;""")
    rows = cursor.fetchone()
    print rows
    return rows[0]

#countPlayers()
def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Delete from Players;""")
    conn.commit()

    cursor.execute("""Select * From Players""")
    number_of_players = cursor.fetchone()
    print number_of_players
#deletePlayers()

def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Delete from Matches""")
    cursor.execute("""Delete from Rounds""")
    conn.commit()
    cursor.execute("""Select * From Rounds""")
    number_of_players = cursor.fetchall()
    #print number_of_players
    return number_of_players


def register_match(round_id, player1_id, player2_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO
                      Matches(Created, RoundId, Player1Id, Player2Id)
                      VALUES
                      (clock_timestamp(), {RoundId}, {Player1Id}, {Player2Id})"""
                   .format(RoundId=round_id, Player1Id=player1_id, Player2Id=player2_id)
                   )
    conn.commit()
    cursor.execute("""Select * from Matches Order by Created DESC""")
    print cursor.fetchall()
    # last_match_registered_id = cursor.fetchone()
    # match_id = last_match_registered_id[0]
    # return match_id


def register_round(number):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Insert Into Rounds(Number) Values(%s)""" % number)
    cursor.execute("""Select id from Rounds Where Number = %s""" % number)
    return cursor.fetchone()[0]



def register_pairing(player_pair, match_id, round):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO Pairings(PlayerId, MatchId, round) VALUES (%s, %s, %s)""",
                   (player_pair[0][0], match_id, round))
    cursor.execute("""INSERT INTO Pairings(PlayerId, MatchId, round) VALUES (%s, %s, %s)""",
                   (player_pair[1][0], match_id, round))

    conn.commit()

    # cursor.execute("""INSERT INTO Pairings(Round, PlayerId, MatchId) VALUES (%s, %s, %s)""", (round_number,
    #                                                                                           player_pair[1][0]), match_id)
    # conn.commit()


# def register_pairing(round_number, pair, match_id):
#     conn = connect()
#     cursor = conn.cursor()
#     cursor.execute("""INSERT INTO Pairings(Round, PlayerId, MatchId) VALUES (%s, %s, %s)""", (round_number,
#                                                                                               pair[0][0]), match_id)
#     conn.commit()
#     cursor.execute("""INSERT INTO Pairings(Round, PlayerId, MatchId) VALUES (%s, %s, %s)""", (round_number,
#                                                                                               pair[1][0]), match_id)
#     conn.commit()
#     cursor.execute("""Select * from Pairings """)
#     bla = cursor.fetchall()
#     #print bla

def first_pairing():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""Select PlayerId from Players""")
    list_of_players = cursor.fetchall()
    pairs_of_players = zip(*[iter(list_of_players)] * 2)
    for pair in pairs_of_players:
        match_id = register_match()

        # register_pairing(1, pair)


# first_pairing()




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
    cursor.execute("""Select * from Pairings""")
    cursor.execute("""Select Players.PlayerId, Players.Name, Count(Pairings.Result = 'winner'),
                     Count(Pairings.MatchId != 0 )
                    from Players left Join Pairings On(Players.PlayerID = Pairings.PlayerID) Group by Players.PlayerId""")
    wins_table = cursor.fetchall()
    # print wins_table
    # print len(wins_table)
    # print "bla"
    return wins_table
    # cursor.execute("""Select * from Pairings""")
    # bla = cursor.fetchall()
    # print bla
    # cursor = conn.cursor()
    # cursor.execute("""Select count(*) From Pairings where Result = 'winner' and Pairings.PlayerId Is Not Distinct From
    #                 Pairings.PlayerId""")
    # bla = cursor.fetchall()
    # print bla
    # cursor.execute("""Select count(*) From Pairings where Pairings.MatchId Is Not Distinct From
    #                    Pairings.MatchId Group by PlayerId """)
    # bla = cursor.fetchall()
    # print bla


# TODO Seleccionar playerID  y Name de Players
# TODO Count wins and Matches from pairings
# TODO Join the results


# playerStandings()



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match_id = register_match()
    # print winner
    # TODO busca winner y loser que tengan el mismo matchID
    conn = connect()
    cursor = conn.cursor()
    # print match_id
    # cursor.execute("""Select MatchId from Pairings Where PlayerId = %s or PlayerId = %s and Pairings.MatchId IS NOT DISTINCT FROM Pairings.MatchId""",
    #                (winner, loser)
    #                )
    # match_id = cursor.fetchone()
    # print match_id
    cursor.execute("""UPDATE Pairings Set Result = 'winner', MatchId = %(match_id)s Where MatchId is not distinct from Null and
                                                                                                PlayerId = %(winner_id)s;""",
                   {"winner_id": winner, "match_id": match_id})
    conn.commit()
    cursor.execute("""Select * from Pairings where Result = 'winner'""")
    # print cursor.fetchall()
    cursor.execute("""UPDATE Pairings Set Result = Null, MatchId = %(match_id)s Where MatchId is not distinct from Null and
                                                                                playerId = %(loser_id)s""",
                   {"loser_id": loser, "match_id": match_id})
    conn.commit()

    # win_table = cursor.fetchall()
    # print win_table
    # return win_table


# reportMatch(2, 1)

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
    conn = connect()
    cursor = conn.cursor()
    round_query = cursor.execute("""Select * from Matches""")
    #round_query = 1
    if round_query is None:
        round_id = register_round(1)
        cursor.query("""Select * from Rounds""")
        print cursor.fetchall()
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""Select Id from Players""")
        list_of_players = cursor.fetchall()
        pairs_of_players = zip(*[iter(list_of_players)] * 2)
        for pair in pairs_of_players:
            player1_id = pair[0][0]
            player2_id = pair[1][0]
            register_match(round_id, player1_id, player2_id)
    else:
        round_id = register_round(1)
        print "si"
        round_query = cursor.execute("""Select * from Rounds""")
        print round_query.first()
        next_round_id = register_round()

swissPairings()
