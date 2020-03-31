import random
import curses
import time
import logging
import os
import uuid
from enum import Enum

# Logger configuration
APPNAME = "lifegame"
BASE_LOG_PATH = "/var/log/"
LOGDIR = BASE_LOG_PATH + APPNAME + '/'
LOGFILE = LOGDIR + "main.log"
# Create log dir if does not exist
os.makedirs(LOGDIR,exist_ok=True)
logging.basicConfig(filename=LOGFILE,level=logging.DEBUG)


# Lifegame rules for the next iteration :
# A cell that has exactly three alive neighbours becomes alive
# A cell that has less than three or more than three alive neighbours dies

class State(Enum):
    DEAD = 0
    ALIVE = 1

class Individual:

    MAX_AGE = 100

    # Initialize an individual with default values
    def __init__(self,max_x,max_y):
        self.uuid = uuid.uuid4()
        self.status = State.ALIVE
        self.maxCoordinates = [max_x,max_y]
        self.coordinates = [0,0]
        self.age = 0
        self.health = 100
        # Using rage because anger is too close of hunger
        self.rage = 50
        self.lust = 50
        self.hunger = 50

    def older():
        self.age += 1
        if self.age == MAX_AGE:
            self.status = State.DEAD


    def setCoordinates(x,y):
        if x<0 or x>self.maxCoordinates[0] or y<0 or y>self.maxCoordinates[1]:
            raise Exception("Trying to set out of bounds coordinates for Individual")
        else:
           self.coordinates = [x,y]
        

class Population:

    def __init__(self, size_x, size_y, scr):
        self.screen = scr
        logging.info("Initializaing population")
        self.size_x = size_x
        self.size_y = size_y
        # Create empty dict to simulate grid
        grid = []
        for row in range(size_x):
            col = [None for i in range(size_y)]
            grid.append(col)
            #print(grid)
        self.grid = grid
        quit


    # Create initial board population
    def populate(self):
        for i in range(1, self.size_x-1):
            for j in range(1,self.size_y-1):
                    # 10% of the initial grid is populated
                if random.random()>0.9:
                    logging.debug("Creating individual at x/y : %i/%i" % (i,j))
                    specimen = Individual(self.size_x, self.size_y)
                    self.grid[i][j] = specimen
        logging.debug("Individuals creation done")


    def birth(self, x, y):
        if x <= self.size_x-1 and y<=self.size_y-1:
            self.population.append([x, y])


    def death(self, x, y):
        self.population.remove([x, y])


    def nextRound(self):
        next_grid = []
        for row in range(self.size_x):
            col = [None for i in range(self.size_y)]
            next_grid.append(col)

        # Iterate over all the grid
        for x in range(self.size_x):
            for y in range(self.size_y):
                self.screen.addstr(x,y,".")
                #logging.debug("Processing cell %i/%i : %s" % (x,y,self.grid[x][y]))
                neighbours_count=0
                try:
                    if self.grid[x-1][y-1] != None :
                        neighbours_count+=1
                    if self.grid[x-1][y] != None :
                        neighbours_count+=1
                    if self.grid[x-1][y+1] != None :
                        neighbours_count+=1
                    if self.grid[x][y-1] != None :
                        neighbours_count+=1
                    if self.grid[x][y+1] != None :
                        neighbours_count+=1
                    if self.grid[x+1][y-1] != None :
                        neighbours_count+=1
                    if self.grid[x+1][y] != None :
                        neighbours_count+=1
                    if self.grid[x+1][y+1] != None :
                        neighbours_count+=1
    
                #If index out of bounds, consider no neighbor for this case
                except Exception as e:
                    #logging.debug("Exception caught: %s", e)
                    pass

                if neighbours_count == 3:
                    #logging.debug("Neighbours : %i. Creating new individual at %i/%i" % (neighbours_count,x,y))
                    next_grid[x][y] = Individual(self.size_x, self.size_y)
                    self.screen.addstr(x,y,"O")
                elif neighbours_count == 2:
                    #logging.debug("Neighbours : %i. Nothing changes at %i/%i" % (neighbours_count,x,y))
                    next_grid[x][y] = self.grid[x][y]
                else:
                    #logging.debug("Neighbours : %i. Killing cell at %i/%i" % (neighbours_count,x,y))
                    next_grid[x][y] = None
                    self.screen.addstr(x,y,".")
        self.grid = next_grid
        time.sleep(0.000001)
        self.screen.refresh()
        



#    def findNeighbours(self, x, y):
#        count = 0
#        if x != 0 and x != self.size_x-1:
#            if y != 0 and y!= self.size_y-1:
#                for i in [-1, 0, 1]:
#                    for j in [-1, 0, 1]:
#                        if i != 0 or j!=0:
#                            if [x+i,y+j] in self.population:
#                                count +=1
#            elif y == 0:
#                for i in [-1, 0, 1]:
#                    for j in [0, 1]:
#                        if i != 0 or j!=0:
#                            if [x+i,y+j] in self.population:
#                                count +=1
#            else:
#                for i in [-1, 0, 1]:
#                    for j in [-1, 0]:
#                        if i != 0 or j!=0:
#                            if [x+i,y+j] in self.population:
#                                count +=1
#        elif x == 0:
#            for i in [0, 1]:
#                for j in [-1, 0, 1]:
#                    if i != 0 or j!=0:
#                        if [x+i,y+j] in self.population:
#                            count +=1
#        else:
#            for i in [-1, 0]:
#                for j in [-1, 0, 1]:
#                    if i != 0 or j!=0:
#                        if [x+i,y+j] in self.population:
#                            count +=1
#        return count

    def playLife(self, population):
        dying = []
        coming_to_life = []
        for guy in population:
            if self.findNeighbours(guy[0], guy[1]) > 3 or self.findNeighbours(guy[0], guy[1])<2:
                dying.append(guy)
        for x in range(1, self.size_x-1):
            for y in range(1, self.size_y-1):
                if [x,y] not in population:
                    if self.findNeighbours(x, y) == 3:
                        coming_to_life.append([x,y])
        for dude in dying:
            if dude in population:
                population.remove(dude)
        for dude in coming_to_life:
            if dude not in population:
                population.append(dude)
        return population


def  main(stdscr):
    logging.info("Main called... here we go !!!")
    #wh, ww = stdscr.getmaxyx()
    wh=50
    ww=50
    logging.debug("Screen max y/x : %i/%i" % (wh,ww))
    # Create initial population grid
    popu = Population(wh,ww,stdscr)
    new_pop = popu.populate()
    #pop = popu.playLife(popu.population)
    logging.debug("Drawing loop start")
    stdscr.clear()
    for i in range(200):
#        stdscr.clear()
#        for guy in pop:
#            stdscr.addstr(guy[0], guy[1], "O")
#            stdscr.refresh()
#            time.sleep(0.000001)
#        pop = popu.playLife(pop)
        popu.nextRound()
#        time.sleep(0.1)

curses.wrapper(main)
