import sys
import pygame as pg
import random

pg.init()
screenSize = (480,550)
screen = pg.display.set_mode(screenSize)
font = pg.font.SysFont(None,50)

grid =  [	[4, 3, 0, 0, 0, 0, 0, 0, 0], 
            [0, 2, 0, 4, 0, 0, 0, 0, 0], 
            [9, 0, 0, 0, 8, 1, 0, 2, 6], 
            [0, 0, 4, 9, 0, 3, 0, 5, 2], 
            [0, 9, 0, 5, 6, 8, 0, 3, 4], 
            [8, 0, 3, 2, 4, 0, 6, 0, 0], 
            [3, 0, 9, 8, 5, 0, 0, 0, 0], 
            [2, 0, 6, 7, 3, 9, 1, 8, 5], 
            [5, 0, 0, 0, 2, 0, 0, 4, 0]]
original_grid = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]

# set up for confetti
confetti = []
for i in range(50):
    x = random.randrange(0, 400)
    y = random.randrange(0, 400)
    confetti.append([x, y])
clock = pg.time.Clock()

# to check if num entered is valid ot not
def validate(num,pos):
	# check each row
	for col in range(9):
		if grid[pos[0]][col] == num and pos[1]!=col:
			return False

	# check each column
	for row in range(9):
		if grid[row][pos[1]] == num and pos[0]!=row:
			return False

	box_x = pos[1] // 3 #column value
	box_y = pos[0] // 3 #row value
	for i in range(box_y*3 ,box_y*3+3):
		for j in range(box_x*3 ,box_x*3+3):
			if grid[i][j]== num and (i,j)!=pos:
				return False
	return True

# for solution using backtracking
def solve():
	pos = findEmpty()
	if not pos:
		return True
	else:
		row = pos[0]
		col = pos[1]
	for num in range (1,10):
		if validate(num,pos):
			grid[row][col] = num
			if solve():
				return True
			grid[row][col] = 0


#display the grid layout
def background():
	rowWidth = 5
	screen.fill(pg.Color("white"))
	pg.draw.rect(screen, pg.Color("black"), pg.Rect(10,10,450,450), rowWidth)
	for i in range(9):
		if i % 3> 0:
			rowWidth=3
		else :
			rowWidth=5
		pg.draw.line(screen, pg.Color("black"), pg.Vector2((i*50+10),10), pg.Vector2((i*50+10),460), rowWidth)
		pg.draw.line(screen, pg.Color("black"), pg.Vector2(10,(i*50+10)), pg.Vector2(460,(i*50+10)), rowWidth)

# to display the pre-given numbers of the suduko grid question
def displayNumbers():
	for row in range(9):
		for col in range(9):
			n = grid[row][col]
			if n == 0:
				n = ""
			num = font.render(str(n),True,pg.Color("black"))
			screen.blit(num,pg.Vector2((col*50)+25, (row*50)+20))

# to diplay the sudoku grid question
def display():
	background()
	displayNumbers()
	pg.display.flip()

# to check empty spaces
def findEmpty():
	for row in range(9):
		for col in range(9):
			if grid[row][col] == 0:
				return [row,col]
	else:
		return None

# releases confetti if player completes the game
def win():
	for i in range(len(confetti)):
		random_r = random.randrange(255)
		random_g = random.randrange(255)
		random_b = random.randrange(255)
		pg.draw.circle(screen, pg.Color(random_r,random_g,random_b), confetti[i], 4)
		confetti[i][1] += 1
		if confetti[i][1] > 550:
			y = random.randrange(-50, -10)
			confetti[i][1] = y
			x = random.randrange(0, 550)
			confetti[i][0] = x
	pg.display.flip()
	clock.tick(10)

# to make the game work
def main():
	run = True
	pressed = False
	winner = False
	display()
	while run:
		if findEmpty() == None:
			win()
			display()
			winner = True
		for event in pg.event.get():
			# to exit the application
			if event.type==pg.QUIT:
				run = False
			# to detect mouse click location
			if event.type == pg.MOUSEBUTTONDOWN:
				pos = pg.mouse.get_pos()
				col = pos[0]//50
				row = pos[1]//50
				display()
				# to show selected box
				if original_grid[row][col] == 0 and winner == False:
					pg.draw.rect(screen, ("blue"), ((col*50) +10 ,(row*50) + 10,50,50), 4)
					pg.display.flip()

			# to record input number
			if event.type == pg.KEYUP and (event.key >= pg.K_1 and event.key <= pg.K_9):
				if original_grid[row][col] == 0:
					display()
					if event.key == pg.K_1:
						enteredValue = 1
						pressed = True
					elif event.key == pg.K_2:
						enteredValue = 2
						pressed = True
					elif event.key == pg.K_3:
						enteredValue = 3
						pressed = True
					elif event.key == pg.K_4:
						enteredValue = 4
						pressed = True
					elif event.key == pg.K_5:
						enteredValue = 5
						pressed = True
					elif event.key == pg.K_6:
						enteredValue = 6
						pressed = True
					elif event.key == pg.K_7:
						enteredValue = 7
						pressed = True
					elif event.key == pg.K_8:
						enteredValue = 8
						pressed = True
					elif event.key == pg.K_9:
						enteredValue = 9
						pressed = True

					# to see if input number is valid or not if yes then green else red
					if validate(enteredValue,(row,col)):
							pg.draw.rect(screen, ("green"), ((col*50) +10 ,(row*50) + 10,50,50), 4)
							num = font.render(str(enteredValue),True,pg.Color("black"))
							screen.blit(num,pg.Vector2((col*50)+25, (row*50)+20))
							pg.display.flip()
							grid[row][col]=enteredValue

					else:
						pg.draw.rect(screen, ("red"), ((col*50) +10 ,(row*50) + 10,50,50), 4)
						num = font.render(str(enteredValue),True,pg.Color("black"))
						screen.blit(num,pg.Vector2((col*50)+25, (row*50)+20))
						pg.display.flip()

			# to clear selected box
			if event.type == pg.KEYUP and pressed == True:
				if event.key == pg.K_BACKSPACE:
					pressed =False
					grid[row][col]=""
					display()

			if event.type == pg.KEYUP:
				if event.key == pg.K_SPACE:
					solve()
					display()
				if event.key == pg.K_DELETE:
					pressed = False
					grid = [[original_grid[x][y] for y in range(len(original_grid[0]))] for x in range(len(original_grid))]
					displayNumbers()
		
	sys.exit()

if __name__ == "__main__":
	main()

