import pygame
from queue import PriorityQueue
import random


VISUALIZE  =True
WIDTH =700    
ROWS =100       
window = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* PathFinding Algorithm")


START = (0, 255, 0)
PATH = (255, 215, 0)
END = (255, 0, 0)
WHITE = (255, 255, 255)
OBST = (0, 0, 0)
OPEN = (255, 165, 0)
CLOSED = (0, 0, 255)


class Cube:
    def __init__(self, row, col, width, total_rows):
        self.row =row
        self.col =col
        self.width =width
        self.total_rows =total_rows
        self.x = row* width
        self.y = col*width
        self.color=WHITE
        self.neighbours =[]

    def getPos(self):
        return self.row,self.col
    
    def isClosed(self):
        return self.color ==CLOSED
    
    def isOpen(self):
        return self.color ==OPEN
    
    def isStart(self):
        return self.color ==START
    
    def isEnd(self):
        return self.color == END
    
    def isWall(self):
        return self.color == OBST
    
    def reset(self):
        self.color =WHITE
    
    def setClosed(self):
        self.color=CLOSED
    
    def setOpen(self):
        self.color=OPEN
    
    def setWall(self):
        self.color=OBST
    
    def setEnd(self):
        self.color=END
    
    def setStart(self):
        self.color=START
    def setPath(self):
        self.color=PATH

    def draw(self ,win):
        pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.width))

    def updateNeighbour(self, grid):
        self.neighbours = []
        directions = [
            (1, 0),   
            (-1, 0),  
            (0, 1),
            (0,-1)
        ]
        
        for drow, dcol in directions:
            newRow, newCol = self.row + drow, self.col + dcol
            if 0 <= newRow < self.total_rows and 0 <= newCol < self.total_rows and not grid[newRow][newCol].isWall():
                self.neighbours.append(grid[newRow][newCol])

    
    def __lt__(self, value):
        return False

def h(p1, p2):
    x1,y1 =p1
    x2,y2 =p2
    return abs(x1-x2) +abs(y1-y2)

def reconstructPath(camefrom, end, draw):
    current =end
    while current in camefrom:
        current = camefrom[current]
        current.setPath()
        if VISUALIZE:
            draw()


def algorithm(draw, grid, start, end):
    count =0
    openSet= PriorityQueue()
    openSet.put((0, count, start))
    openSetHash={start}
    cameFrom ={}
    
    #score

    while not openSet.empty():
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
        
        current  = openSet.get()[2]
        openSetHash.remove(current)
        
        #solution     
        
        if VISUALIZE:
            draw()

        if current != start and VISUALIZE:
            current.setClosed()

    return False

def setGrid(rows, width):
    grid= []
    gap =width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cube = Cube(i,j,gap,rows)
            grid[i].append(cube)
    return grid

def drawGrid(win, rows , width):
    gap =width //rows
    for i in range(rows):
        pygame.draw.line(win,WHITE,(0,i*gap),(width,i*gap))
        pygame.draw.line(win,WHITE,(i*gap,0),(i*gap,width))

def draw(win, grid,rows , width):
    win.fill(WHITE)

    for row in grid:
        for cub in row:
            cub.draw(win)
    
    drawGrid(win, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    x, y =pos
    gap =width//rows
    rows = x//gap
    col =  y//gap
    return rows,col

def setPredefinedWalls(grid):
    total_cells = ROWS * ROWS
    wall_cells = int(total_cells * 0.3)

    wall_positions = random.sample(range(total_cells), wall_cells)

    for pos in wall_positions:
        row = pos // ROWS
        col = pos % ROWS
        if (row, col) != (0, 0) and (row, col) != (ROWS - 1, ROWS - 1):
            grid[row][col].setWall()


def main(win, width,ROWS):
    grid = setGrid(ROWS, width)

    setPredefinedWalls(grid)

    run = True
    started = False

    start = None
    end = None

    while run :
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
            
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos,ROWS , width)
                cube= grid[row][col]
                if not start and cube!=end:
                    start=cube
                    cube.setStart()
                    cube.draw(win)
                elif not end and cube !=start:
                    end = cube
                    cube.setEnd()
                    cube.draw(win)
                elif cube != end and cube != start:
                    cube.setWall()
                    cube.draw(win)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row , col = getClickedPos(pos,ROWS , width)
                cube= grid[row][col]
                if cube == start :
                    start = None
                elif cube ==end:
                    end =None 
                cube.reset()
                cube.draw(win)
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_SPACE and start and end:
                    for row in grid:
                        for cube in row:
                            cube.updateNeighbour(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width), grid ,start ,end)
                if event.key ==pygame.K_c:
                    start =None
                    end   =None
                    grid = setGrid(ROWS, width)

                    setPredefinedWalls(grid)

main(window, WIDTH, ROWS)