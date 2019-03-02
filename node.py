import math
from copy import deepcopy
import queue
import time

class node:
	childs = None
	parent = None
	gridMap = None
	key = ""
	isMax = None
	alpha = None
	beta = None
	depth = None
	moveFromPrevious = None

	def __init__(self, childs, parent, depth, isMax, alpha, beta, grid):
		self.childs = childs
		self.parent = parent
		self.grid = grid
		self.depth = depth
		self.isMax = isMax
		self.alpha = alpha
		self.beta = beta
		for x in range(0,4):
			for y in range(0,4):
				self.key += str(grid.map[x][y])
	def evaluate(self):
		blankTiles = len(self.grid.getAvailableCells())
		score = 0
		weights = [[8,7,6,5],[5,4,3,2],[2,1,0,0],[1,0,0,0]]
		for i in range(0,4):
			for j in range(0,4):
				score += weights[i][j] * self.grid.map[i][j]
		penalty = self.sumClusterScores()
		return score*5 - penalty*3 + 1.9**blankTiles

	def sumClusterScores(self):
		sumAnswer = 0
		for i in range(0,4):
			for j in range(0,4):
				up = [i,j-1]
				down = [i,j+1]
				left = [i-1,j]
				right = [i+1,j]
				sumAnswer+= self.getDiff(up,self.grid.map[i][j])
				sumAnswer+= self.getDiff(down,self.grid.map[i][j])
				sumAnswer+= self.getDiff(left,self.grid.map[i][j])
				sumAnswer+= self.getDiff(right,self.grid.map[i][j])
		return sumAnswer

	def getDiff(self,pos,element):
		if pos[0] < 0 or pos[0] > 3 or pos [1] < 0 or pos[1] > 3:
			return 0
		if element == 0:
			return abs(self.grid.map[pos[0]][pos[1]]-element)
		else:
			return abs(self.grid.map[pos[0]][pos[1]]-element)

	def setChildren(self):
		possibleMoves = self.grid.getAvailableMoves()
		children = []
		for x in range(0,len(possibleMoves)):
			copy = self.grid.clone()
			if possibleMoves[x] == 0:
				copy.moveUD(False)
			if possibleMoves[x] == 1:
				copy.moveUD(True)
			if possibleMoves[x] == 2:
				copy.moveLR(False)
			if possibleMoves[x] == 3:
				copy.moveLR(True)

			toAdd = node(None,self,self.depth+1,True,-999999,999999,copy)
			toAdd.moveFromPrevious = possibleMoves[x]
			children.append(toAdd)

		self.childs = children

	def setChildrenCG(self):
		children = []
		emptyCells = self.grid.getAvailableCells()
		for x in range(0,len(emptyCells)):
			copy2 = self.grid.clone()
			copy4 = self.grid.clone()
			copy2.setCellValue(emptyCells[x],2)
			copy4.setCellValue(emptyCells[x],4)
			children.append(node(None,self,self.depth+1,False,-999999,999999,copy2))
			children.append(node(None,self,self.depth+1,False,-999999,999999,copy4))

		self.childs = children

	def maximize(self, maxDepth, alpha, beta, startTime):
		if self.depth >= maxDepth or (time.time()-startTime)>0.5:
			return [self.evaluate(),self]
		if self.childs is None:
			self.setChildren()
		if len(self.childs) == 0:
			return [self.evaluate(),self]
		bestChild = None
		for x in range(0,len(self.childs)):
			value = self.childs[x].minimize(maxDepth,alpha,beta, startTime)[0]
			if (value > alpha):
				alpha = value
				bestChild = self.childs[x]
			if alpha >= beta:
				return [alpha,bestChild]
		return [alpha,bestChild]

	def minimize(self, maxDepth, alpha, beta, startTime):
		if self.depth is maxDepth or (time.time()-startTime)>0.5:
			return [self.evaluate(),self]
		if self.childs is None:
			self.setChildrenCG()
		if len(self.childs) == 0:
			return [self.evaluate(),self]
		bestChild = None
		for x in range(0,len(self.childs)):
			value = self.childs[x].maximize(maxDepth,alpha,beta, startTime)[0]
			if (value < beta):
				beta = value
				bestChild = self.childs[x]
			if beta <= alpha:
				return [beta,bestChild]
				break
		return [beta,bestChild]
		'''avg = 0
		for x in range(0,len(self.childs)):
			avg += self.childs[x].maximize(maxDepth,alpha,beta)[0]
		avg /= len(self.childs)
		return [avg,self.childs[0]]'''
