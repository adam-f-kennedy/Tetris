# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

# server connection info
HOST = 'localhost'
USER = 'root'
PASSWORD = ''

# dictionary for server info
SERVER = {
    'host':HOST,
    'user':USER, 
    'password':PASSWORD
}

# datebase for blockgame
BLOCKGAME_DB = 'blockgame'

TABLES = {}

TABLES['highscores'] =(
    'CREATE TABLE HighScores('
    '   id varchar(3) NOT NULL,'
    '   score INT NOT NULL)'
)

# blockgame queries

BLOCK_GAME_QUERIES = {}


BLOCK_GAME_QUERIES['EndGameTop5'] = ('SELECT * FROM highscores ORDER BY score DESC LIMIT 5')