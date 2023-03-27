# Driver

import sys

sys.path.append(r"H:\blockgame TRUE\BlockGame\Lib\site-packages")

import mysqlServer

# Stub
HOST = 'localhost'
USER = 'root'
PASSWORD = ''

server = mysqlServer.MySQLServer(HOST, USER, PASSWORD)
server.ConnectToServer()