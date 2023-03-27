# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

import pygame as pg
from config import *
import random

# class to define the block components of shape
class Block(pg.sprite.Sprite):
    # initialises block object
    def __init__(self, shape, pos):
        self.pos = pg.math.Vector2(pos) + INIT_START_POS
        self.shape = shape
        self.living = True
        self.image = pg.image.load\
            (f"{LOCAL_DIR_PATH}\\assets\\blocks\\" +\
             f"{self.shape.shape}.png").convert()
        self.rect = pg.rect.Rect\
            (self.pos[0]*TILE_SIZE, 
             self.pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        super().__init__(shape.game.blockGroup)

    # if block is alive(whether it has been clearedd)
    def IsAlive(self):
        if not(self.living):
            self.kill()

    # gets if the block has collided with something it can't pass
    def IsCollide(self, pos):
        x, y = int(pos.x), int(pos.y)
            
        if (0 <= x < FIELD_W) and (y < FIELD_H) and \
            ((y < 0) or \
             (not self.shape.game.fieldArray[y][x])):
            return False
        return True
    
    # sets position and size of rect
    def SetRectPos(self):
        self.rect.topleft = self.pos * TILE_SIZE
    
    # rotates blocks around pivot point
    def Rotate(self, pivotPos, direction):
        if not(self.shape.shape == 'O'):
            if direction=='left':
                diffPos = pg.math.Vector2\
                    (self.pos - pivotPos)
                rotatedPos = diffPos.rotate(-90)
                rotatedPos += pivotPos
                return rotatedPos
            elif direction=='right':
                diffPos = pg.math.Vector2\
                    (self.pos - pivotPos)
                rotatedPos = diffPos.rotate(90)
                rotatedPos += pivotPos
                return rotatedPos
        else:
            return self.pos
    
    # updates block
    def update(self):
        self.IsAlive()
        self.SetRectPos()
        
    
    # draws block to screen
    def Draw(self):
        self.shape.game.app.screen.blit\
            (self.image, self.pos*TILE_SIZE)
    
class Shape:
    # initialises shape object
    def __init__(self, game):
        self.game = game
        self.shape = self.GetShape()
        self.blocks = self.GetArrayOfBlocks()
        self.landed = False
    
    # chooses a shape
    def GetShape(self):
        return random.choice(list(SHAPES.keys()))
    
    # gets array of blocks that make up the shape
    def GetArrayOfBlocks(self):
        return \
            [Block(self, pos)\
              for pos in SHAPES[self.shape]]

    # checks if any blocks in shape collide
    def IsCollide(self, newBlockPos):
        return any\
            (map(Block.IsCollide, self.blocks, newBlockPos))
    
    
    # moves all blocks in the shape
    def Move(self, direction):
        moveDirection = MOVEMENT_DIR[direction]

        # creates array of blocks new positions
        newBlockPos = [block.pos + moveDirection\
                        for block in self.blocks] 
        
        # checks if any of the blocks new positions collide with anything
        isCollide = self.IsCollide(newBlockPos)
              

        # if no blocks collide
        if not (isCollide) and not (self.landed):
            for block in self.blocks:
                block.pos += moveDirection
        elif direction=='down':
            self.landed = True

    # rotates the current block and makes sure nothing collides
    def Rotate(self, direction):
        pivotPos = self.blocks[0].pos
        newBlockPos = [block.Rotate(pivotPos, direction)\
                        for block in self.blocks]
        isCollide = self.IsCollide(newBlockPos)

        if not(isCollide):
            for i, block in enumerate(self.blocks):
                block.pos = newBlockPos[i]
    
    # updates shape
    def Update(self):
        self.Move('down')