from random import randint

from BaseAI_3 import BaseAI

from node import node

import time

class PlayerAI(BaseAI):

     def getMove(self, grid):
          moves = grid.getAvailableMoves()
          timeStart = time.time()
          blankTiles = len(grid.getAvailableCells())
          startNode = node(None,None,0,True,-999999,999999,grid)
          startNode.setChildren()
          childsArr = startNode.childs
          if blankTiles > 6:
               maxDepth = 4
          else:
               maxDepth = 5

          toGoTo = startNode.maximize(maxDepth,-999999,999999, timeStart)[1].moveFromPrevious
          timeElapsed = time.time()-timeStart
          print("running_time_calculating_move: "+str(timeElapsed))

          return toGoTo
          
