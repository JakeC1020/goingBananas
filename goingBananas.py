"""
http://pythonprogramming.net/pygame-tutorial-moving-images-key-input/
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

white = (255,255,255)

#Create Display and setup display vars
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Going Bananas')

clock = pygame.time.Clock()
monkeyImg = pygame.image.load('monkey.png')
snakeImg = pygame.image.load('snake.png')


def moveMonkey(x,y):
	gameDisplay.blit(monkeyImg, (x,y))

def moveSnake(snakeDict):
	snakeDict['x'] += snakeDict['speed']
	gameDisplay.blit(snakeImg, (snakeDict['x'], snakeDict['y']))

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
	gameDisplay.fill(white)
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
	

	
	tickCounter += 1

	pygame.display.flip()
	clock.tick(60)

name = input("You Lose! Thanks for Playing!")

pygame.quit()
quit()


