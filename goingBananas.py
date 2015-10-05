"""
http://pythonprogramming.net/pygame-tutorial-moving-images-key-input/
https://www.pygame.org/docs/tut/tom/games2.html
"""

import pygame, time

pygame.init()

# Display Constants
displayWidth = 600
displayHeight = 400

imageWidth = 64
imageHeight = 55
 
snakeImageWidth = 64
snakeImageHeight = 44

bananaImageWidth = 64
bananaImageHeight = 34

white = (255,255,255)

jungleGreen = (28, 53, 45)



#Create Display and setup display vars
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Going Bananas')

# Background display
background = pygame.Surface(gameDisplay.get_size())
background = background.convert()
background.fill(jungleGreen)

# Text Setup
font = pygame.font.Font(None, 36)


clock = pygame.time.Clock()
monkeyImg = pygame.image.load('img/monkey.png')
snakeImg = pygame.image.load('img/snake.png')
bananaImg = pygame.image.load('img/banana.png')
vineImg = pygame.image.load('img/vine.png')
vine2Img = pygame.image.load('img/vine2.png')
vine3Img = pygame.image.load('img/vine3.png')


def moveMonkey(x,y):
	gameDisplay.blit(monkeyImg, (x,y))

def moveSnake(snakeDict):
	snakeDict['x'] += snakeDict['speed']
	gameDisplay.blit(snakeImg, (snakeDict['x'], snakeDict['y']))

def moveBanana(bananaDict):
	bananaDict['x'] += bananaDict['speed']
	gameDisplay.blit(bananaImg, (bananaDict['x'], bananaDict['y']))

def inAir(y):
	if y < initialY:
		isInAir = True
	else:
		isInAir = False
	return isInAir

def addGravity(ySpeed):
	# Clock ticks roughly every .015ish of a second, this estimate will do for this game
	return ySpeed - gravity

def changeYLocation(ySpeed, y):
	# Takes in ySpeed and computes new location 
	return y - (ySpeed*.20)

def inBarrierLR(xCoord, displayWidth, imageWidth):
	if xCoord >= 0 and (xCoord + imageWidth) <= displayWidth:
		isInBarrier = True
	else:
		isInBarrier = False
	return isInBarrier

def inBarrierUp(yCoord, displayHeight):
	if yCoord >= 0:
		isInBarrier = True
	else:
		isInBarrier = False
	return isInBarrier

def isCollision(monkeyDict, snakeDict):
	xMatch = False
	yMatch = False
	collision = False

	if monkeyDict['x'] <= snakeDict['x'] <= (monkeyDict['x'] + monkeyDict['imageWidth']) or snakeDict['x'] <= monkeyDict['x'] <= (snakeDict['x'] + snakeDict['imageWidth']):
		xMatch = True

	if monkeyDict['y'] <= snakeDict['y'] <= (monkeyDict['y'] + monkeyDict['imageHeight']) or snakeDict['y'] <= monkeyDict['y'] <= (snakeDict['y'] + snakeDict['imageHeight']):
		yMatch = True

	if xMatch and yMatch:
		collision = True
	else:
		collision = False
	return collision

def getMonkeyDict(xCoord, yCoord, imageWidth, imageHeight):
	monkeyDict = {}
	monkeyDict['x'] = xCoord
	monkeyDict['y']  = yCoord
	monkeyDict['imageWidth'] = imageWidth
	monkeyDict['imageHeight'] = imageHeight
	return monkeyDict

def makeSnake(displayWidth, snakeImageWidth, snakeImageHeight, snakeSpeed, initialY):
	snakeDict = {}
	snakeDict['x'] = displayWidth - imageWidth
	snakeDict['y'] = initialY
	snakeDict['speed'] = snakeSpeed
	snakeDict['imageWidth'] = snakeImageWidth
	snakeDict['imageHeight'] = snakeImageHeight
	snakes.append(snakeDict)
	moveSnake(snakeDict)

def makeBanana(displayWidth, bananaImageWidth, bananaImageHeight, bananaSpeed, initialY):
	bananaDict = {}
	bananaDict['x'] = displayWidth - imageWidth
	bananaDict['y'] = initialY
	bananaDict['speed'] = bananaSpeed
	bananaDict['imageWidth'] = bananaImageWidth
	bananaDict['imageHeight'] = bananaImageHeight
	bananas.append(bananaDict)
	moveBanana(bananaDict)

def getHighScore():
	scoreFile = open('highScore.txt', 'r')
	score = scoreFile.read()
	scoreFile.close()
	return score

def setHighScore(newHighScore):
	scoreFile = open('highScore.txt', 'w')
	scoreFile.write(newHighScore)
	scoreFile.close()

# Position and other physics constants
gravity = 1.5

initialX = (displayWidth * .45)
initialY = (displayHeight * .7)

x = initialX
y = initialY

deltaX = 0

# Enemy Vars
tickCounter = 0
snakes = []
snakeSpeed = -5

# Banana Vars
bananas = []
bananaSpeed = -2

# Score Vars
score = 0
highScore = getHighScore()


# Var to check if monkey is still alive
hitSnake = False

while not hitSnake:
	for event in pygame.event.get():
		# Death Event 
		if event.type == pygame.QUIT:
			hitSnake = True
		elif event.type == pygame.KEYDOWN:
			# Key has been pressed, see which it is and act on it
			if event.key == pygame.K_LEFT:	
				deltaX = -5
			elif event.key == pygame.K_RIGHT:
				deltaX = 5
			elif event.key == pygame.K_SPACE:
				if inBarrierUp(y-100, displayHeight):
					ySpeed = 25
					y -= 100
		elif event.type == pygame.KEYUP:
			# Key is no longer being pressed, stop changing x value
			deltaX = 0
	# Add the change in X to the Monkey's x
	x += deltaX
	# If we just left the barrier, undo that
	if not inBarrierLR(x, displayWidth, imageWidth):
		x -= deltaX

	# Check to see if monkey is in air, if it is, add "gravity"
	if inAir(y):
		y = changeYLocation(ySpeed, y)
		ySpeed = addGravity(ySpeed)

	# Redraw and flip screen
	gameDisplay.blit(background, (0,0))
	textScore = font.render("Score: " + str(score), 1, (255,255,255))
	gameDisplay.blit(textScore, (475, 25))
	textHighScore = font.render("High Score: " + str(highScore), 1, (255,255,255))
	gameDisplay.blit(textHighScore, (415, 75))
	gameDisplay.blit(vineImg, (-25,0))
	gameDisplay.blit(vineImg, (75, 0))
	gameDisplay.blit(vine2Img, (275,0))
	gameDisplay.blit(vine3Img, (360, 0))
	# Move monkey
	moveMonkey(x,y)
		
	### Monkey is done moving this cycle, do enemy work ###
	for snake in snakes:

		# Check for snake collisions
		if isCollision(getMonkeyDict(x, y, imageWidth, imageHeight), snake):
			# User hit snake, end game
			hitSnake = True

		# Move snake
		moveSnake(snake)
	# Clean up old snakes
		if not inBarrierLR(snake['x'], displayWidth, snake['imageWidth']):
			# Snake is off screen
			snakes.remove(snake)
	# Generate new Snakes
	if tickCounter % 120 == 0:
		makeSnake(displayWidth, snakeImageWidth, snakeImageHeight, snakeSpeed, initialY)
	
 	### Enemy has been processed, do banana work

	for banana in bananas:

		# Check for banana collisions
		if isCollision(getMonkeyDict(x, y, imageWidth, imageHeight), banana):
			score += 1
			bananas.remove(banana)

		if not inBarrierLR(banana['x'], displayWidth, banana['imageWidth']):
			bananas.remove(banana)

		moveBanana(banana)

	if tickCounter % 60 == 0:
		makeBanana(displayWidth, bananaImageWidth, bananaImageHeight, bananaSpeed, initialY)
	
	tickCounter += 1


	pygame.display.flip()
	clock.tick(60)

if score > int(highScore):
	setHighScore(str(score))
	print "New High Score:", score

print("You Lose! Thanks for Playing!")

pygame.quit()
quit()


