#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:34:36 2020

@author: ornwipa

settings from class Grid, map = [[0] * 4 for i in range(4)]
so map is [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

"""
from Grid_3 import Grid # for pre-test
# from Grid import Grid # for submission
from random import randint, randrange
import random
from BaseAI import BaseAI
import time
import math

class PlayerAI(BaseAI):
    
    """getMove() method is inherited from class BaseAI
       in GameManager, call self.playerAI.getMove(grid) to execute"""
    def getMove(self, grid):

        timeLimit = 0.2
        timeStart = time.clock()
        alpha = 1.0 #2
        beta = math.inf #2048
#        bestMove = randrange(0,4,1) 
        bestMove = grid.getAvailableMoves()[0] # randrange(0,4,1) # None
        
        """getAvailableMoves in vecIndex [UP, DOWN, LEFT, RIGHT]
        moves is a list, can include all/some/none of [0, 1, 2, 3]"""
#        moves = grid.getAvailableMoves()
        
        """starter code to randomly return values 0, 1, 2, 3"""
        # return moves[randint(0, len(moves) - 1)] if moves else None
        
        """ this is the decision state """
#        try:
#            maxUtility = 2
#
#            """ as if calling maximize function """
#            for child in moves:
#                g = grid.clone()
#                g.move(child)
#                (dummy, utility, bestMove) = self.minimize(g, timeStart, timeLimit, alpha, beta)
#                if utility > maxUtility:
#                    bestMove = child
#        except KeyError:
#            bestMove = None
#        
#        return bestMove
    
        return self.maximize(grid, timeStart, timeLimit, alpha, beta, bestMove)[2]
    
        """ w/o time limit... RecursionError: 
        maximum recursion depth exceeded while calling a Python object """
    
    def minimize(self, grid, timeStart, timeLimit, alpha, beta, bestMove):
        
        availableCells = grid.getAvailableCells()
        
        """terminate when no cell can be inserted """
        if availableCells == []:
#            return (None, grid.getMaxTile(), bestMove, alpha, beta)
            return (None, self.heuristic(grid), bestMove, alpha, beta)
        
#        (minChild, minUtility) = (None, math.inf) #2048)
        
        """ base case to no longer increase search depth, computer insert random tile """
        g = grid.clone()
#        compMove = availableCells[randint(0, len(availableCells) - 1)]
        compMove = availableCells[0]
        minChild = g.setCellValue(compMove, 2) # randrange(2,5,2))
#        g.setCellValue(compMove, randrange(2,5,2))
#        minChild = g
#        minUtility = g.getMaxTile()
        minUtility = self.heuristic(g)
        
        """ conditional case to keep searching 
            allow search in all possible cells (16-1) x 2 tile values """
        try:
            timeUpperBound = timeLimit/len(availableCells)/2
        except ZeroDivisionError:
            timeUpperBound = timeLimit/2
            
        if time.clock() - timeStart < timeUpperBound:
            
            # random.shuffle(availableCells) # do not random, search got worse
            for cell in availableCells:
                for newTile in [2, 4]:
                    """ g is the grid which a possible value inserted in an available cell """                    
                    g = grid.clone()
                    g.insertTile(cell, newTile)
                    """ recursive function """
                    (dummy, utility, testMove, alpha, beta) = self.maximize(g, timeStart, timeLimit, alpha, beta, bestMove)
                    
                    if utility < minUtility:
                        (minChild, minUtility) = (g, utility)
                        
                    """ prunning """
                    if minUtility <= alpha:
                        break
                    if minUtility < beta:
                        beta = minUtility      
        
        return (minChild, minUtility, bestMove, alpha, beta)
            
    def maximize(self, grid, timeStart, timeLimit, alpha, beta, bestMove):
        
        """ terminate either when cannot move """
        try:
            terminate = not grid.canMove(range(4))
        except AttributeError:      
            terminate = True
        """ or when reach 2048 """    
        if terminate: # or grid.getMaxTile() == 2048: # no need to terminate as max score grows
#            return (None, grid.getMaxTile(), bestMove, alpha, beta)
            return (None, self.heuristic(grid), bestMove, alpha, beta)
        
        moves = grid.getAvailableMoves()
        
        """ set the base case for maxChild to the child resulted from the best move instead of None """
        try:
            g = grid.clone()
            g.move(bestMove)
        except TypeError:
            maxChild = None
        else:
            maxChild = g

        maxUtility = 1.0
#        (maxChild, maxUtility, bestMove) = (None, 1.0, bestMove) #2, bestMove) # use math.log2(2)=1.0

        """ always keep searching, allow search in all possible directions, max 4 """
        try:
            timeUpperBound = timeLimit/len(moves)
        except ZeroDivisionError:
            timeUpperBound = timeLimit
            
        if time.clock() - timeStart < timeUpperBound:
            
            # random.shuffle(moves) # do not random, search got worse       
            for child in moves:                
                """ g is the moved grid to a possible direction """
                g = grid.clone()
                g.move(child)                
                """ recursive function """
                (dummy, utility, testMove, alpha, beta) = self.minimize(g, timeStart, timeLimit, alpha, beta, bestMove)
            
                if utility > maxUtility:
                    (maxChild, maxUtility, bestMove) = (g, utility, child)
                
                """ prunning """
                if maxUtility >= beta:
                    break
                if maxUtility > alpha:
                    alpha = maxUtility
            
        return (maxChild, maxUtility, bestMove, alpha, beta)
    
    def monotonicity(self, grid):
        """ to ensure that values of tiles are ALL either increasing or decreasing 
             (NOT equal) along BOTH the 4 left/right + 4 up/down directions = max 8 """
        h = 0
        # for i in range(4):
        #     if grid.map[i][0] < grid.map[i][1] and grid.map[i][1] < grid.map[i][2] and grid.map[i][2] < grid.map[i][3]:
        #         h += 1
        #     if grid.map[i][0] > grid.map[i][1] and grid.map[i][1] > grid.map[i][2] and grid.map[i][2] > grid.map[i][3]:
        #         h += 1            
        for j in range(4):
        #     if grid.map[0][j] < grid.map[1][j] and grid.map[1][j] < grid.map[2][j] and grid.map[2][j] < grid.map[3][j]:
        #         h += 1
        #     if grid.map[0][j] > grid.map[1][j] and grid.map[1][j] > grid.map[2][j] and grid.map[2][j] > grid.map[3][j]:
        #         h += 1
            for i in range(3):
                if grid.map[i][j] > grid.map[i+1][j]:
                    h += 1 # keep higher values on lower row
        for j in range(3):
            try:
                d = math.log2(grid.map[0][j+1]/grid.map[0][j])
                if d <= 0:
                    h += d
            except ValueError:
                h += 0
            except ZeroDivisionError:
                h += 0
            try:
                d = math.log2(grid.map[1][j]/grid.map[1][j+1])
                if d <= 0:
                    h += d
            except ValueError:
                h += 0
            except ZeroDivisionError:
                h += 0
            try:
                d = math.log2(grid.map[2][j+1]/grid.map[2][j])
                if d <= 0:
                    h += d
            except ValueError:
                h += 0
            except ZeroDivisionError:
                h += 0
            try:
                d = math.log2(grid.map[3][j]/grid.map[3][j+1])
                if d <= 0:
                    h += d
            except ValueError:
                h += 0
            except ZeroDivisionError:
                h += 0
        try:
            d = math.log2(grid.map[1][3]/grid.map[0][3])
            if d <= 0:
                h += d
        except ValueError:
            h += 0
        except ZeroDivisionError:
            h += 0
        try:
            d = math.log2(grid.map[2][0]/grid.map[1][0])
            if d <= 0:
                h += d
        except ValueError:
            h += 0
        except ZeroDivisionError:
            h += 0
        try:
            d = math.log2(grid.map[3][3]/grid.map[2][3])
            if d <= 0:
                h += d
        except ValueError:
            h += 0
        except ZeroDivisionError:
            h += 0
        """ normalised h to (0,1) scale """
        return h # h is forced to be negative
    
    def smoothness(self, grid):
        """ in order to merge (at the next move), adjacent tiles need to be the same value, 
            count 3 pairs x 4 rows + 3 pairs x 4 columns = max 24 """
        h = 0
        for i in range(4):
            for j in range(3):
                if grid.map[i][j] == grid.map[i][j+1]:
                    h += 1
        for j in range(4):
            for i in range(3):        
                if grid.map[i][j] == grid.map[i+1][j]:
                    h += 1
        """ normalised h to (0,1) scale """
        return h#/24
    
    def freeTiles(self, grid):
        """ heuristic function as a penalty for having too few free tiles, max = 16-1 """
        return len(grid.getAvailableCells())#/15 # get normalised to range between 0 and one
    
    def maxAtCorner(self, grid):
        """ to ensure that max value stays at corner, binary can be dominated by high log2(maxValue) 
            if aim for log2(512)=9 then its weight should be >= 9 times of log2(grid.getMaxTile()) """
        mtv = grid.getMaxTile()
        if grid.map[0][0] == mtv:# or grid.map[0][3] == mtv or grid.map[3][0] == mtv or grid.map[3][3] == mtv:
            return 40 # focus on one corner, give weight for 10*4 times the others
        return 0
    
    def heuristic(self, grid):
        """ weighted heuristic functions
            maximum at math.log2(2048) = 11.0 so no other heuristics should exceed 11 """
#        return grid.getMaxTile()
#        return math.log2(grid.getMaxTile())/4 + self.monotonicity(grid)/4 + self.smoothness(grid)/4 + self.freeTiles(grid)/4
        return self.monotonicity(grid)/6 + self.smoothness(grid)/6 + self.freeTiles(grid)/6 + self.maxAtCorner(grid)/3

