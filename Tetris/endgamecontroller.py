# Adam Kennedy
# 16/03/2023
# Advanced Higher Project

from config import *
from mySQLServerConfig import *
import mysqlServer

# sort algorithm to sort highscores from highest to lowest
def BubbleSort(arr, indexOfNum):
    tempHolder = 0
    outer = len(arr) - 1
    noSwap = False
    while (outer != -1 or noSwap == False):
        noSwap = True
        for inner in range(0, outer):
            if arr[inner][indexOfNum] < arr[inner + 1][indexOfNum]:
                tempHolder = arr[inner][indexOfNum]
                arr[inner][indexOfNum] = arr[inner + 1][indexOfNum]
                arr[inner + 1][indexOfNum] = tempHolder
                noSwap = False
        outer -= 1
    return arr

# class to control endgame display
class EndGameController():
    def __init__(self, game):
        self.game = game
        self.player = ''
        self.font = self.GetFont()
        self.prevPlayerTop5 = self.GetHighScoresToSurface()

    # gets font to use at endgame
    def GetFont(self, font=GAME_FONT, size=ENDGAME_SIZE, 
                bold=False, italic=False):
        return pg.font.SysFont(font, size, bold, italic)

    # gets highscores 
    def GetHighScoresToSurface(self):
        highscoresSurfaces = []
        highscores = self.game.app.mySQLServer.SelectStatement\
            (BLOCK_GAME_QUERIES['EndGameTop5'])
        highscores = highscores.fetchall()
        for i in range(0, len(highscores)):
            highscores[i] = [highscores[i][0], highscores[i][1]]
        if len(highscores) > 0:
            highscores = BubbleSort(highscores, 1)
        
        for (id, score) in highscores:
            prevPlayerText = str(id) + ' ' + str(score)
            prevPlayerTextSurface = self.GetText\
                (prevPlayerText, TEXT_COLOR, antialias=True)
            highscoresSurfaces.append(prevPlayerTextSurface)
        
        
        return highscoresSurfaces
    
    # gets the players inputs for endgame overlay
    def GetPlayerIdInput(self):
        pressedKey = self.game.app.pressedKey
        if (pressedKey != pg.K_BACKSPACE) and (len(self.player) < 3) \
            and (pressedKey != None) and \
                (pressedKey >= 97 and pressedKey <= 122):
            self.player = self.player + chr(pressedKey).upper()
        elif pressedKey == pg.K_BACKSPACE:
            self.player = self.player[:len(self.player) - 1]
        elif (len(self.player) == 3) and (pressedKey == pg.K_RETURN):
            if not(self.prevPlayerTop5 == 5):
                self.game.app.mySQLServer.InsertStatement\
                    (f'INSERT INTO highscores(id, score) VALUES' +\
                     f'("{str(self.player)}", "{int(self.game.score)}")')
                self.game.restart = True
            else:
                self.game.restart = True

    # gets text using font
    def GetText(self, text, textColor=TEXT_COLOR, antialias=False):
        return self.font.render(text, antialias, textColor)

    # draws text to screen
    def DrawText(self, pos, text, textColor=TEXT_COLOR, antialias=False):
        Text = self.font.render(text, antialias, textColor)
        self.game.app.display.blit(Text, pos)
        return Text

    # draws scores to display
    def DrawHighscores(self):
        textHeight = 0
        scoreHeaderText = self.DrawText\
            (HIGHSCORE_HEADER_OFFSET, 
             HIGHSCORE_HEADER, textColor=TEXT_COLOR, antialias=True)
        for i, prevPlayerInfo in enumerate(self.prevPlayerTop5):
            for text in (self.prevPlayerTop5[0:i]):
                textHeight += text.get_height()
            self.game.app.display.blit\
                (prevPlayerInfo, 
                 (HIGHSCORE_HEADER_OFFSET + \
                  (0, scoreHeaderText.get_height()) + (0, textHeight)))
            textHeight = 0
    
    # draws the players score to the screen
    def DrawPlayerScore(self):
        textHeight = 0
        playerHeader = self.DrawText\
            (PLAYER_SCORE_HEADER_OFFSET, 
             PLAYER_HEADER, textColor=TEXT_COLOR, antialias=True)
        player = self.GetText(self.player, TEXT_COLOR, antialias=True)
        score = self.GetText(str(self.game.score), TEXT_COLOR, antialias=True)
        playerInfoTup = (player, score)
        for i, playerInfo in enumerate(playerInfoTup):
            for text in (playerInfoTup[0:i]):
                textHeight += text.get_height()
            self.game.app.display.blit\
                (playerInfo, 
                 (PLAYER_SCORE_HEADER_OFFSET + \
                  (0, playerHeader.get_height()) + (0, textHeight)))
            textHeight = 0

    # Updates end game screen
    def Update(self):
        self.GetPlayerIdInput()


    # draws end game screen
    def Draw(self):
        self.game.app.display.fill((0, 0, 0))
        self.game.app.screen.fill((0, 0, 0))
        self.DrawHighscores()
        self.DrawPlayerScore()