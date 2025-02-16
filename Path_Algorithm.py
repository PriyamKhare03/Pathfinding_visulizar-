import pygame
from collections import deque
pygame.init()

width = 900
height = 900

WIN = pygame.display.set_mode((width,height))
pygame.display.set_caption("Pathfinding Visualizer")



RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)



class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    
    def is_barrier(self):
        return self.color == BLACK
        
    def draw(self,win):
    	pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def make_start(self):
    	self.color = ORANGE
    def make_end(self):
    	self.color = GRAY
    def make_open(self):
    	self.color = GREEN
    def make_barrier(self):
    	self.color = BLACK
    def make_close(self):
    	self.color = RED
    def make_path(self):
    	self.color = PURPLE

def reconstruct_path(came_from,current,draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

#breadth first dearch code...........
def bfs_algorithm(draw,grid,start,end):
	queue = deque([start])
	came_from = {}
	visited = set()
	
	visited.add(start)
	while queue:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		current = queue.popleft()
		if current == end:
			reconstruct_path(came_from,current,draw)
			start.make_start()
			end.make_end()
			return True
		
		neighbours = []
		if current.row < current.total_rows -1 and not grid[current.row +1][current.col].is_barrier():
			neighbours.append(grid[current.row +1][current.col])
		if current.row > 0 and not grid[current.row -1][current.col].is_barrier():
			neighbours.append(grid[current.row - 1][current.col])
		if current.col < current.total_rows - 1 and not grid[current.row][current.col+1].is_barrier():
			neighbours.append(grid[current.row][current.col + 1])  
		if current.col > 0 and not grid[current.row][current.col-1].is_barrier():
			neighbours.append(grid[current.row][current.col - 1])
			
			
		for neighbour in neighbours:
			if neighbour not in visited:
				visited.add(neighbour)
				came_from[neighbour] = current
				queue.append(neighbour)
				neighbour.make_open()
		
		draw()
		if current != start:
				current.make_close()
		pygame.time.delay(9)
	
	return False


# depth first search code.............
def dfs_algorithm(draw,grid,start,end):
	stack = [start]
	came_from = {}
	visited = set()
	
	visited.add(start)
	while stack:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		
		current = stack.pop()
		if current == end:
			reconstruct_path(came_from,current,draw)
			start.make_start()
			end.make_end()
			return True
		
		neighbours = []
		if current.row < current.total_rows -1 and not grid[current.row +1][current.col].is_barrier():
			neighbours.append(grid[current.row +1][current.col])
		if current.row > 0 and not grid[current.row -1][current.col].is_barrier():
			neighbours.append(grid[current.row - 1][current.col])
		if current.col < current.total_rows - 1 and not grid[current.row][current.col+1].is_barrier():
			neighbours.append(grid[current.row][current.col + 1])  
		if current.col > 0 and not grid[current.row][current.col-1].is_barrier():
			neighbours.append(grid[current.row][current.col - 1])
			
			
		for neighbour in neighbours:
			if neighbour not in visited:
				visited.add(neighbour)
				came_from[neighbour] = current
				stack.append(neighbour)
				neighbour.make_open()
		
		draw()
		if current != start:
				current.make_close()
		pygame.time.delay(9)
	
	return False



def make_grid(rows, width):
    grid = []  # We will keep our squares in this list
    gap = width // rows  # This decides the size of each square
    for i in range(rows):
        grid.append([]) 
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            grid[i].append(spot)
    return grid


#GRAY = (128,128,128)
#WHITE = (255,255,255)

def draw_grid(win, rows, width):
    gap = width // rows  # Size of each square
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))  # Draw horizontal lines
        pygame.draw.line(win, GRAY, (i * gap, 0), (i * gap, width))  # Draw vertical lines

def draw(WIN, grid, rows, width):
    WIN.fill(WHITE)  # Fill the background with white color
    for row in grid:
    	for spot in row:
    		spot.draw(WIN)
    draw_grid(WIN, rows, width)  # Draw the grid lines
    pygame.display.update()  # Refresh the window to show the grid

def get_clicked_pos(pos,rows,width):
	gap = width // rows
	y,x = pos
	row = y // gap
	col = x // gap
	return row,col
	
def main():
	run = True
	rows = 50
	start = None
	end = None
	started = False
	grid = make_grid(rows,width)
	while run:
		draw(WIN,grid,rows,width) 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if pygame.mouse.get_pressed()[0]:
				pos = pygame.mouse.get_pos()
				row,col = get_clicked_pos(pos,rows,width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()
				elif not end and spot != start:
					end = spot
					end.make_end()
				elif spot != start and spot != end:
					spot.make_barrier()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not started:
						bfs_algorithm(lambda:draw(WIN,grid,rows,width),grid,start,end)
						#started = True
				if event.key == pygame.K_d and not started:
					dfs_algorithm(lambda:draw(WIN,grid,rows,width),grid,start,end)
					#started = True
				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(rows,width)
	
	pygame.quit()


main()
