# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

from mySQLServerConfig import *
from endgamecontroller import *
import pygame as pg
from blocks import *
from config import *

class Game:
    # initialises game
    def __init__(self, app):
        self.app = app
        self.overlay = self.GetOverlay('Light')
        self.blockGroup = pg.sprite.Group()
        self.fieldArray = self.GetFieldArray()
        self.shape = self.GetShape()
        self.font = self.GetFont()
        self.speedUp = False
        self.lines = 0
        self.score = 0
        self.gameOver = False
        self.restart = False

    # draws play area grid
    def DrawGrid(self):
        for y in range(FIELD_H):
            for x in range(FIELD_W):
                pg.draw.rect(self.app.screen,
                             (0, 0, 0),
                               (x*TILE_SIZE,
                                 y*TILE_SIZE,
                                   TILE_SIZE,
                                     TILE_SIZE), 1)
    
    # loads the overlay for outside play area
    def GetOverlay(self, type='Light'):
        return pg.image.load\
            (f"{LOCAL_DIR_PATH}\\assets\\" +\
             f"overlay\\staticScreen{type}.png")
    
    # draws overlay to display
    def DrawOverlay(self):
        self.app.display.blit(self.overlay, (0, 0))

    # gets the font used in-game
    def GetFont(self, font=GAME_FONT, \
                size=FONT_SIZE, bold=False, italic=False):
        return pg.font.SysFont(font, size, bold, italic)

    # draws the score to the score box
    def GetText(self, text, color, antialias=False):
        textSurface = self.font.render\
            (text, antialias, color)
        return textSurface
    
    # gets the array with the state of each tile in play area      
    def GetFieldArray(self):
        return [[0 for x in range(FIELD_W)]\
                 for y in range(FIELD_H)]
    
    # instantiates a new shape object
    def GetShape(self):
        return Shape(self)
    
    # checks and clears whole lines
    def ClearLines(self):
        lines = 0
        row = FIELD_H - 1
        for y in range(FIELD_H -1, -1, -1):
            for x in range(FIELD_W):
                self.fieldArray[row][x] =\
                      self.fieldArray[y][x]
                if self.fieldArray[y][x]:
                    self.fieldArray[row][x].pos =\
                          pg.math.Vector2(x, row) 
            if sum(map(bool, self.fieldArray[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    lines += 1
                    self.fieldArray[row][x].living = False
                    self.fieldArray[row][x] = 0
        return lines
    
    # updates the score
    def UpdateScore(self, clearedLines):
        self.score += (SCORE_BASE) * (clearedLines**SCORE_MULT)

    # draws score to display
    def DrawScore(self):
        score = self.GetText\
            (str(self.score), TEXT_COLOR, antialias=True) # get score surface
        self.app.display.blit(score, SCORE_OFFSET) # show score
    
    # takes the position of the current shape 
    # and updates field array tile states accordingly
    def PutBlocksInFieldArray(self):
        for block in self.shape.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.fieldArray[y][x] = block

    # checks if the current shape has landed and
    #  if true cleans up everything for new shape to appear
    def CheckIfShapeLanded(self):
        if self.shape.landed:
            self.CheckIfGameOver()
            self.speedUp = False
            self.PutBlocksInFieldArray()
            self.shape = self.GetShape()

    # controls what happens when a key is pressed
    def Controls(self, pressedKey):
        self.lastKeyPressed = pressedKey
        if pressedKey == pg.K_a:
            self.shape.Move('left')
        elif pressedKey == pg.K_d:
            self.shape.Move('right')
        elif pressedKey == pg.K_s:
            self.speedUp = True
        elif pressedKey == pg.K_w:
            self.shape.Rotate('left')
        elif pressedKey == pg.K_e:
            self.shape.Rotate('right')

    # checks whether the game is over
    def CheckIfGameOver(self):
        for block in self.shape.blocks:
            if block.pos[1] * TILE_SIZE +\
                  FIELD_OFFSET[1] <= FIELD_OFFSET[1]:
                self.gameOver = True
                

    # updates the game state
    def Update(self):
        trigger = [self.app.animTrigger,\
                    self.app.fastAnimTrigger][self.speedUp]
        if not(self.gameOver):
            if trigger:
                self.lines = self.ClearLines()
                self.UpdateScore(self.lines)
                self.shape.Update()
                self.CheckIfShapeLanded()
                if self.gameOver:
                    self.endGameController =\
                          EndGameController(self)
            self.blockGroup.update()
        else:
            self.endGameController.Update()

    # draws the updates to the game to the screen 
    def Draw(self):
        if not(self.gameOver):
            self.DrawOverlay()
            self.DrawGrid()
            self.blockGroup.draw(self.app.screen)
            self.DrawScore()
        else:
            self.endGameController.Draw()
