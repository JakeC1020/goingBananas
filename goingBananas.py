"""
http://pythonprogramming.net/pygame-tutorial-moving-images-key-input/
"""

import pygame, time

pygame.init()

# Display Constants
displayWidth = 600
displayHeight = 400

white = (255,255,255)

#Create Display and setup display vars
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Going Bananas')

clock = pygame.time.Clock()
monkeyImg = pygame.image.load('monkey.png')



def moveMonkey(x,y):
	gameDisplay.blit(monkeyImg, (x,y))

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

# Position and other physics constants
gravity = 1.5

initialX = (displayWidth * .45)
initialY = (displayHeight * .7)

x = initialX
y = initialY

deltaX = 0

# Var to carry if monkey is still alive
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
				ySpeed = 25
				y -= 100
		elif event.type == pygame.KEYUP:
			# Key is no longer being pressed, stop changing x value
			deltaX = 0
	# Add the change in X to the Monkey's x
	x += deltaX

	# Check to see if monkey is in air, if it is, add "gravity"
	if inAir(y):
		y = changeYLocation(ySpeed, y)
		ySpeed = addGravity(ySpeed)
		


	# Redraw and flick screen
	gameDisplay.fill(white)

	moveMonkey(x,y)

	pygame.display.flip()
	clock.tick(60)

pygame.quit()
quit()


