"""
Jacob Crawford
10/6/15
Project #1
This program uses the library pygame to create a game where the player (the monkey), must avoid snakes who run across the screen while collecting the bananas that also go across the screen. 

Sources:
Modified player movement code from http://pythonprogramming.net/pygame-tutorial-moving-images-key-input/ 
Modified text display code from https://www.pygame.org/docs/tut/tom/games2.html
Frequently accessed the Python 2 docs https://docs.python.org/2/
All images are licensed under a public domain license, requiring no accreditation
"""

import pygame

########## Game Functions ##########

def drawBackground(score, highScore, backgroundColor, font, vineImg, vine2Img, vine3Img, gameDisplay):
	gameDisplay.fill(backgroundColor)
	textScore = font.render("Score: " + str(score), 1, (255,255,255))
	gameDisplay.blit(textScore, (475, 25))
	textHighScore = font.render("High Score: " + str(highScore), 1, (255,255,255))
	gameDisplay.blit(textHighScore, (415, 75))
	gameDisplay.blit(vineImg, (-25,0))
	gameDisplay.blit(vineImg, (75, 0))
	gameDisplay.blit(vine2Img, (275,0))
	gameDisplay.blit(vine3Img, (360, 0))

def moveMonkey(monkeyDict, monkeyImg, gameDisplay):
	gameDisplay.blit(monkeyImg, (monkeyDict['x'],monkeyDict['y']))

def moveSnake(snakeDict, snakeImg, gameDisplay):
	snakeDict['x'] += snakeDict['speed']
	gameDisplay.blit(snakeImg, (snakeDict['x'], snakeDict['y']))

def moveBanana(bananaDict, bananaImg, gameDisplay):
	bananaDict['x'] += bananaDict['speed']
	gameDisplay.blit(bananaImg, (bananaDict['x'], bananaDict['y']))

def inAir(y, initialY):
	if y < initialY:
		isInAir = True
	else:
		isInAir = False
	return isInAir

def addGravity(ySpeed, gravity):
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

def makeMonkey(xCoord, yCoord, imageWidth, imageHeight):
	monkeyDict = {}
	monkeyDict['x'] = xCoord
	monkeyDict['y']  = yCoord
	monkeyDict['imageWidth'] = imageWidth
	monkeyDict['imageHeight'] = imageHeight
	return monkeyDict

def makeSnake(displayWidth, snakeImageWidth, snakeImageHeight, snakeSpeed, initialY):
	snakeDict = {}
	snakeDict['x'] = displayWidth - snakeImageWidth
	snakeDict['y'] = initialY
	snakeDict['speed'] = snakeSpeed
	snakeDict['imageWidth'] = snakeImageWidth
	snakeDict['imageHeight'] = snakeImageHeight
	return snakeDict
	

def makeBanana(displayWidth, bananaImageWidth, bananaImageHeight, bananaSpeed, initialY):
	bananaDict = {}
	bananaDict['x'] = displayWidth - bananaImageWidth
	bananaDict['y'] = initialY
	bananaDict['speed'] = bananaSpeed
	bananaDict['imageWidth'] = bananaImageWidth
	bananaDict['imageHeight'] = bananaImageHeight
	return bananaDict
	

def getHighScore():
	scoreFile = open('highScore.txt', 'r')
	score = scoreFile.read()
	scoreFile.close()
	return score

def setHighScore(newHighScore):
	scoreFile = open('highScore.txt', 'w')
	scoreFile.write(newHighScore)
	scoreFile.close()

def main():
	pygame.init()

	########## Display Constants and Vars##########
	displayWidth = 600
	displayHeight = 400

	monkeyImageWidth = 64
	monkeyImageHeight = 55
	 
	snakeImageWidth = 64
	snakeImageHeight = 44

	bananaImageWidth = 64
	bananaImageHeight = 34

	white = (255,255,255)

	jungleGreen = (28, 53, 45)


	#Create Display and setup display vars
	gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
	pygame.display.set_caption('Going Bananas')

	# Text Setup
	font = pygame.font.Font(None, 36)

	clock = pygame.time.Clock()
	monkeyImg = pygame.image.load('img/monkey.png')
	snakeImg = pygame.image.load('img/snake.png')
	bananaImg = pygame.image.load('img/banana.png')
	vineImg = pygame.image.load('img/vine.png')
	vine2Img = pygame.image.load('img/vine2.png')
	vine3Img = pygame.image.load('img/vine3.png')

	########## Game Constants and Vars ##########

	# Physics vars

	initialX = (displayWidth * .45)
	initialY = (displayHeight * .7)

	X_SPEED = 5
	Y_SPEED = 25
	gravity = 1.5

	JUMP_HEIGHT = 100

	# Initialize speed vars
	xSpeed = 0
	ySpeed = 0

	# Enemy vars
	tickCounter = 0
	snakes = []
	SNAKE_SPEED = -5
	SNAKE_INTERVAL = 120

	# Banana vars
	bananas = []
	BANANA_SPEED = -2
	BANANA_INTERVAL = 60

	# Score vars
	score = 0
	highScore = getHighScore()


	# Var to check if monkey is still alive
	hitSnake = False

	# Make our monkey and start playing
	monkey = makeMonkey(initialX, initialY, monkeyImageWidth, monkeyImageHeight)

	while not hitSnake:
		# Set up the background
		drawBackground(score, highScore, jungleGreen, font, vineImg, vine2Img, vine3Img, gameDisplay)

		########## Monkey (Player) movement ##########
		for event in pygame.event.get():
			# Death Event 
			if event.type == pygame.QUIT:
				hitSnake = True
			elif event.type == pygame.KEYDOWN:
				# Key has been pressed, see which it is and act on it
				if event.key == pygame.K_LEFT:	
					xSpeed = -X_SPEED
				elif event.key == pygame.K_RIGHT:
					xSpeed = X_SPEED
				elif event.key == pygame.K_SPACE and inBarrierUp(monkey['y']-JUMP_HEIGHT, displayHeight):
					ySpeed = Y_SPEED
					monkey['y'] -= JUMP_HEIGHT
			elif event.type == pygame.KEYUP:
				# Key is no longer being pressed, stop changing x value
				xSpeed = 0

		# Add the change in X to the Monkey's x
		monkey['x'] += xSpeed

		# If we just left the barrier, undo that
		if not inBarrierLR(monkey['x'], displayWidth, monkeyImageWidth):
			monkey['x'] -= xSpeed

		# Check to see if monkey is in air, if it is, add "gravity"
		if inAir(monkey['y'], initialY):
			monkey['y'] = changeYLocation(ySpeed, monkey['y'])
			ySpeed = addGravity(ySpeed, gravity)

		# Move monkey
		moveMonkey(monkey, monkeyImg, gameDisplay)
			
		########## Monkey is done moving this cycle, do enemy work ##########

		for snake in snakes:
			# Check for snake collisions
			if isCollision(monkey, snake):
				# User hit snake, end game
				hitSnake = True

			# Move snake
			moveSnake(snake, snakeImg, gameDisplay)

			# Clean up old snakes
			if not inBarrierLR(snake['x'], displayWidth, snake['imageWidth']):
				# Snake is off screen
				snakes.remove(snake)

		# Generate new snakes
		if tickCounter % SNAKE_INTERVAL == 0:
			snakes.append(makeSnake(displayWidth, snakeImageWidth, snakeImageHeight, SNAKE_SPEED, initialY))
		
	 	########## Enemy has been processed, do banana work ##########

		for banana in bananas:
			# Check for banana collisions
			if isCollision(monkey, banana):
				score += 1
				bananas.remove(banana)

			# Move banana
			moveBanana(banana, bananaImg, gameDisplay)	

			# Clean up old bananas
			if not inBarrierLR(banana['x'], displayWidth, banana['imageWidth']):
				# Banana is off screen
				bananas.remove(banana)

		# Generate new bananas
		if tickCounter % BANANA_INTERVAL == 0:
			bananas.append(makeBanana(displayWidth, bananaImageWidth, bananaImageHeight, BANANA_SPEED, initialY))

		tickCounter += 1

		pygame.display.flip()
		clock.tick(60)

	########## Post Game Actions ##########

	if score > int(highScore):
		setHighScore(str(score))
		print "New High Score:", score

	print("You Lose! Thanks for Playing!")

	pygame.quit()
	quit()

main()
