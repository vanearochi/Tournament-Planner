# UDACITY TOURNAMENT PLANNER. 

 This project consists of the design and creation of a PostgreSQL database and the code that keeps track of players and matches, 
 as well as  the corresponding player pairing in a Swiss system tournament

## Prerequisites.

* Install Vagrant:
```
        https://www.vagrantup.com/
```
* Install VirtualBox:
```
        https://www.virtualbox.org/
```
* Clone or Download project from:
```
        https://github.com/vanearochi/Tournament-Planner
```

## Project Files.

* tournament.sql
    Contains database structure, that is to say the tables and their corresponding columns that it will have.
* tournament.py
    Contains the functions that will manage players and matches of the tournament
    
* tournament_test.py
    Contains the tests that will test the functions on tournament.py


### Launch the Vagrant Virtual Machine.

* On the vagrant folder run:
    
```
        $ vagrant up
```
* Then:
    
```
        $ vagrant ssh

        You should see something like this on the command line:

        vagrant@vagrant-ubuntu-trusty-32:~$
```


### Starting up PostgreSQL.

* On Virtual Machine, change to vagrant folder:
    
```
        $ vagrant@vagrant-ubuntu-trusty-32:~$ cd /vagrant/
```

* Launch PostgreSQL:
```
        vagrant@vagrant-ubuntu-trusty-32:/vagrant/$ psql

        You should see something like this on the command line:

        vagrant=>
```
* Create tournament database:
    
```
        vagrant=> create database tournament.sql
```
* Import tournament.sql file to PostgreSQL to create tables:
```
        $ \i tournament.sql
```
* Get out of PostgreSQL:
```
        $ \q
```

## Running the tests

The tournament_test.py file tests the functions on tournament.py with data samples.

* On the Virtual Machine, on tournament folder run test:
    
```
        vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ python tournament_test.py
```

The outcome should be:

```
        1. Old matches can be deleted.
        2. Player records can be deleted.
        3. After deleting, countPlayers() returns zero.
        4. After registering a player, countPlayers() returns 1.
        5. Players can be registered and deleted.
        6. Newly registered players appear in the standings with no matches.
        7. After a match, players have updated standings.
        8. After one match, players with one win are paired.
        Success!  All tests pass!
```


## Registering your own tournament.

Using the tournament.py file you can register and delete players and matches results, 
check the players standings and pair players for the next round accordingly.

* Create a new python file from the command line on the tournament file:
```
        $ touch file_name.py
```
* Open your file and import tournament.py to use it's functions, type:
```
        from tournament import *
```
* To register a new player call the registerPlayer function on your new file:
```
        registerPlayer("player_name"):
```
* To report match results call the reportMatch function on your new file:
```
        reportMatch(winner_playerid, loser_playerid):
```
* To see the winning table and number of matches played for each player call the
playerStandings function on your new file:
```
        print playerStandings():
```
* To create a new pair of players based on their results call swissPairings function on your new file:
```
        print swissPairings():
```
* To delete all the Players or/and Matches from the table call deletePlayers or/and deleteMatches:
```
        deletePlayers()
        deleteMatches()
```


