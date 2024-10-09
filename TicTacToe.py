import pygame
import sys
import time 

pygame.init()

width = 400
height = 400
bgColour = (0, 0, 0)
lineColour = (100, 100, 100)
circleColour = (0, 0, 255)
crossColour = (255, 0, 0)
glowColour = (255, 255, 0)

lineWidth = width // 35
circleWidth = width // 35
crossWidth = width // 40

rows = 3
columns = 3
squareSize = width // columns
circleRadius = squareSize // 3
space = squareSize // 4

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic-Tac-Toe')
screen.fill(bgColour)

currentPlayer = 1
gameOver = False
startTime = time.time()

lastMove = None
glowTimer = 0.1
glowDuration = 0.2

board = [[0 for _ in range(columns)] for _ in range(rows)]

def displayMessage(msg, x, y):
    fontObj = pygame.font.SysFont("freesans", width // 20)
    msgObj = fontObj.render(msg, False, (155, 155, 25))
    screen.blit(msgObj, (x, y))

def drawLines():
    for row in range(1, rows):
        pygame.draw.line(screen, lineColour, (0, row * squareSize), (width, row * squareSize), lineWidth)
    
    for col in range(1, columns):
        pygame.draw.line(screen, lineColour, (col * squareSize, 0), (col * squareSize, height), lineWidth)

def drawCircle(row, col):
    center = (col * squareSize + squareSize // 2, row * squareSize + squareSize // 2)
    pygame.draw.circle(screen, circleColour, center, circleRadius, circleWidth)

def drawCross(row, col):
    startDesc = (col * squareSize + space, row * squareSize + space)
    endDesc = (col * squareSize + squareSize - space, row * squareSize + squareSize - space)
    
    startAsc = (col * squareSize + space, row * squareSize + squareSize - space)
    endAsc = (col * squareSize + squareSize - space, row * squareSize + space)
    
    pygame.draw.line(screen, crossColour, startDesc, endDesc, crossWidth)
    pygame.draw.line(screen, crossColour, startAsc, endAsc, crossWidth)

def drawGlow(row, col, alpha):
    glowSurface = pygame.Surface((squareSize, squareSize), pygame.SRCALPHA)
    glowSurface.fill((*glowColour, alpha))
    screen.blit(glowSurface, (col * squareSize, row * squareSize))


def isBoardFull():
    for row in range(rows):
        for col in range(columns):
            if board[row][col] == 0:
                return False
    return True

def checkWin(player):
    for col in range(columns):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            drawVerticalWinningLine(col, player)
            return True

    for row in range(rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            drawHorizontalWinningLine(row, player)
            return True

    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        drawAscDiagonal(player)
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        drawDescDiagonal(player)
        return True

    return False

def drawVerticalWinningLine(col, player):
    posX = col * squareSize + squareSize // 2
    color = circleColour if player == 1 else crossColour
    pygame.draw.line(screen, color, (posX, 15), (posX, height - 15), 15)

def drawHorizontalWinningLine(row, player):
    posY = row * squareSize + squareSize // 2
    color = circleColour if player == 1 else crossColour
    pygame.draw.line(screen, color, (15, posY), (width - 15, posY), 15)

def drawAscDiagonal(player):
    color = circleColour if player == 1 else crossColour
    pygame.draw.line(screen, color, (15, height - 15), (width - 15, 15), 15)

def drawDescDiagonal(player):
    color = circleColour if player == 1 else crossColour
    pygame.draw.line(screen, color, (15, 15), (width - 15, height - 15), 15)

def restartGame():
    screen.fill(bgColour)
    drawLines()
    for row in range(rows):
        for col in range(columns):
            board[row][col] = 0

drawLines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not gameOver:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clickedRow = mouseY // squareSize
            clickedCol = mouseX // squareSize

            if board[clickedRow][clickedCol] == 0:
                board[clickedRow][clickedCol] = currentPlayer
                if currentPlayer == 1:
                    drawCircle(clickedRow, clickedCol)
                else:
                    drawCross(clickedRow, clickedCol)

                if checkWin(currentPlayer):
                    endTime = time.time()
                    totalTime = round(endTime - startTime, 2)
                    displayMessage(f"Player {currentPlayer} wins! Time: {totalTime}s", 10, 10)
                    displayMessage("Press 'SPACE' to restart", 10, 10 + width // 20)
                    gameOver = True

                currentPlayer = 3 - currentPlayer

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and gameOver:
                restartGame()
                currentPlayer = 1
                gameOver = False
                startTime = time.time()

    if lastMove:
        elapsedTime = time.time() - glowTimer
        if elapsedTime < glowDuration:
            alpha = int((1 - (elapsedTime / glowDuration)) * 255)
            drawGlow(lastMove[0], lastMove[1], alpha)
        else:
            lastMove = None 


    pygame.display.update()
