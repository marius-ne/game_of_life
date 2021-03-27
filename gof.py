from pprint import pprint
import numpy as np
from PIL import Image
import time
import imageio
import random

class GoF(object):

    def __init__(self, gens):
        '''Initialises image. It's represented by a 256x256 sized array.'''
        self.gens = gens
        self.count = 1
        self.images = []
        self.grid = []
        for _ in range(0,1024):
            self.grid.append([[0,0,0,255] for col in range(0,1024)])
        self.grid = np.array(self.grid)

    def turn(self,pixel):
        '''Reverses the state off one pixel from ONE->OFF and vice versa.'''
        row, col = pixel
        if not self.state(pixel):
            if self.count  == 0:
                self.grid[row][col] = np.array([255,0,0,255])
                self.count += 1
            elif self.count  == 1:
                self.grid[row][col] = np.array([0,0,255,255])
                self.count += 1
            elif self.count  == 2:
                self.grid[row][col] = np.array([0,255,0,255])
                self.count = 0
        else:
            self.grid[row][col] = np.array([0,0,0,255])

    def get(self,pixel):
        '''Gets the RGB at a certain coordinate.'''
        row, col = pixel
        return self.grid[row][col]

    def state(self,pixel):
        '''Gets the state at a certain coordinate.'''
        if self.get(pixel)[0] == 0 and self.get(pixel)[1] == 0 and self.get(pixel)[2] == 0:
            return False
        else:
            return True

    def neighbours(self,pixel,state='vals'):
        '''Returns neighbours of a given cell.
        With vals the RGB values, with bin the state, with cords the coordinates.'''
        row, col = pixel
        if state=='vals':
            rt = [self.get((row+1,col)),
                self.get((row-1,col)),
                self.get((row,col+1)),
                self.get((row,col-1)),
                self.get((row-1,col-1)),
                self.get((row-1,col+1)),
                self.get((row+1,col+1)),
                self.get((row+1,col-1))]
            return rt
        elif state=='bin':
            rt = [self.state((row+1,col)),
                self.state((row-1,col)),
                self.state((row,col+1)),
                self.state((row,col-1)),
                self.state((row-1,col-1)),
                self.state((row-1,col+1)),
                self.state((row+1,col+1)),
                self.state((row+1,col-1))]
            return rt
        elif state=='cords':
            rt = [(row+1,col),
                (row-1,col),
                (row,col+1),
                (row,col-1),
                (row-1,col-1),
                (row-1,col+1),
                (row+1,col+1),
                (row+1,col-1)]
            return rt

    def figure(self,pixels):
        '''Creates first figure from input
        pixels = [(0,0),(127,127),(200,200)...] 
        -> First row, then column, 
        -> First tuple is starting point'''
        self.points = [p for p in pixels]
        for pxl in pixels:
            self.turn(pxl)

    def algorithm(self,pixels):
        '''Takes input pixels and calls self.figure. From there on, the pixels are kept track of in 
        a dictionary called track. Key is the pixel with the corresponding state as value. (ON/OFF)
        With each generation tracked is updated with all not-yet present neighbour-cells.
        
        Then, for each key (px) in tracked, the neighbouring states are evaluated according to
        Conway's rules. If more than four or less than one neighbour of an active cell are also active
        the cell dies. If three cells around an inactive cell are active, it becomes active as well.
        
        If a cell matching these criteria is found, it is appended to a list (turned), which is
        iterated over and turned with self.turn.'''
        pixels = list(set(pixels))
        self.figure(pixels)
        self.show(0)
        self.images[0].save('init.PNG')
        tracked = {p:self.state(p) for p in pixels}
        count = 0
        while count<self.gens:
            print(count)
            turns = []
            tracked.update({nb:self.state(nb) for px in tracked for nb in self.neighbours(px, state='cords') if nb not in tracked})
            for px, s in tracked.items():
                trues = self.neighbours(px, state='bin').count(True)
                if s == True:
                    if trues >= 4 or trues <= 1:
                        turns.append(px)
                        tracked[px] = False
                elif s == False:
                    if trues == 3:
                        turns.append(px)
                        tracked[px] = True
            for px in list(set(turns)):
                self.turn(px)
            count += 1
            self.show(count)

    def show(self,num):
        '''Creates two images of the current generation.'''
        img = Image.fromarray(self.grid.astype(np.uint8))
        self.images.append(img)
        self.images.append(img)
        self.images.append(img)
    
    def animate(self):
        '''Creates gif from images.'''
        imageio.mimsave('movie.gif', self.images)

grid = GoF(400)
grid.algorithm([
    (random.choice(range(400,600)), random.choice(range(400,600))) for i in range(30000)])
grid.animate()



    