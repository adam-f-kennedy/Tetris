# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

import sys

sys.path.append\
    (r"H:\blockgame TRUE\BlockGame\Lib\site-packages")

import mysqlServer
import pygame as pg
from game import *
from config import *
from mySQLServerConfig import *


# class to handle the running of the app
class app:
    # initialises app
    def __init__(self):
        pg.init()
        self.Setup()
        pg.display.set_caption("Block Game")
        self.display = pg.display.set_mode(DISPLAY_SIZE)
        self.screen = pg.surface.Surface\
            ((FIELD_W*TILE_SIZE, FIELD_H*TILE_SIZE))
        self.SetTimer()
        self.keyHeld = [False, 0]
        self.clock = pg.time.Clock()
        self.game = Game(self)

    # setsup external game components
    def Setup(self):
        self.SetupDatabaseServer()
    
    def SetupDatabaseServer(self):
        self.mySQLServer = self.MakeMySQLServer()
        self.mySQLServer.ConnectToServer()
        databaseCreated = self.mySQLServer.CreateDB(BLOCKGAME_DB)
        self.mySQLServer.UseDB(BLOCKGAME_DB)
        if databaseCreated:
            self.mySQLServer.CreateTable(TABLES['highscores'])

    # makes mySQL server
    def MakeMySQLServer(self):
        return mysqlServer.MySQLServer\
            (self, SERVER['host'], SERVER['user'], SERVER['password'])

    # creates timmer for user events
    def SetTimer(self):
        self.userAnimEvent = pg.USEREVENT + 0
        self.userFastAnimEvent = pg.USEREVENT + 1
        self.animTrigger = False
        self.fastAnimTrigger = False
        pg.time.set_timer(self.userAnimEvent, ANIM_TIME)
        pg.time.set_timer(self.userFastAnimEvent, FAST_ANIM_TIME)
        

    # checks for events in pygame
    def CheckForEvents(self):
        self.pressedKey = None
        self.animTrigger = False
        self.fastAnimTrigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if (event.type == pg.KEYDOWN):
                 self.game.Controls(pressedKey=event.key)
                 self.pressedKey = event.key
            if event.type == self.userAnimEvent:
                self.animTrigger = True
            if event.type == self.userFastAnimEvent:
                self.fastAnimTrigger = True

    # updates game and controls frames
    def Update(self):
        self.game.Update()
        self.clock.tick(FPS)

    # draws updates to screen
    def Draw(self):
        self.screen.fill(FIELD_COLOR)
        self.game.Draw()
        if not(self.game.gameOver):
            self.display.blit(self.screen, FIELD_OFFSET + (0, 0))
        pg.display.flip()
    
    # main game loop
    def Main(self):
        run = True
        while run:
            if self.game.restart:
                self.game = Game(self)
            self.CheckForEvents()
            self.Update()
            self.Draw()

application = app()\
      # instantiates class that runs the application
application.Main() # calls main game loop
