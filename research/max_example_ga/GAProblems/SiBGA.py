#!/usr/bin/env python
# encoding: utf-8
"""
SiBGA.py

Created by Max Martin on 2008-03-23.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import decimal
import math
import random
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/GA')
import GenGA
import Ind

import psyco
psyco.full()

adjacencies = []

class SibGA(GenGA.GenerationalGA):
	def __init__(self,chr_len,fitness,cross=.8,mut=0.1,popsize=1000,elitism=1):
		global adjacencies
		GenGA.GenerationalGA.__init__(self,Ind.SnakePath,chr_len,fitness,"quaternaryTournament",cross,mut,popsize,elitism,"default","default",adjacencies[:])
		
	def terminator(self):
		if self.current_gen < 30: return None
		if round(self.best_scores[self.current_gen]) == round(self.best_scores[self.current_gen - 30]):
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!

def fitness(individual):
	global adjacencies
	elts = individual.genome
	length = 2
	maxlength = 2
	illegal = []
	lengths = []
	maxillegal = []
	for i in range(2,(len(elts)-1)):
		for ad in adjacencies[elts[i-2]]:
			if ad not in illegal:
				illegal.append(ad)
		if elts[i-2] not in illegal:
			illegal.append(elts[i-2])
		if elts[i-1] not in illegal:
			illegal.append(elts[i-1])
		if elts[i] not in illegal:
			illegal.append(elts[i])
		if elts[i+1] in illegal:
			if length > maxlength:
				maxlength = length
				maxillegal = illegal
			if length > 2:
				lengths.append(length)
			illegal = []
			length = 2
		else:
			length = length + 1
	'''for l in lengths:
		others += 0.1 * l'''
		
	available = 256 - len(maxillegal)
	
	return maxlength + (0.1 * available)
	
def findSnake(elts):
	length = 2
	maxlength = 2
	illegal = []
	maxillegal = []
	begin = 0
	newbegin = 0
	end = 0
	for i in range(2,(len(elts)-1)):
		for ad in adjacencies[elts[i-2]]:
			if ad not in illegal:
				illegal.append(ad)
		if elts[i-2] not in illegal:
			illegal.append(elts[i-2])
		if elts[i-1] not in illegal:
			illegal.append(elts[i-1])
		if elts[i] not in illegal:
			illegal.append(elts[i])
		if elts[i+1] in illegal:
			if length > maxlength:
				maxlength = length
				end = i+1
				begin = newbegin
				maxillegal = illegal
			illegal = []
			length = 2
			newbegin = i-1
		else:
			length = length + 1
			
	return [begin,end,(256 - len(maxillegal))]


def main():
	table = open("Dimension8Table.txt")
	global adjacencies
	for i in range(256):
		adjacencies.append([])
		s = table.readline()
		temp = s.split()
		for t in temp:
			adjacencies[i].append(int(t))

	table.close()
	
	popsize = 300
	indsize = 150
	
	#seed = [40,41,43,47,63,62,60,124,125,121,123,122,106,98,99,103,119,118,86,94,95,79,75,73,72,88,80,81,85,69,68,100,36,37,53,49,51,50,18,26,27,25,29,13,12,14,6,7,3,1,0,2]
	#seed = [0, 1, 3, 7, 6, 14, 12, 13, 29, 25, 27, 26, 18, 50, 51, 49, 53, 37, 36, 100, 68, 69, 85, 81, 80, 88, 72, 73, 75, 79, 95, 94, 86, 118, 119, 103, 99, 98, 106, 122, 123, 121, 125, 124, 60, 62, 63, 47, 43, 41, 40, 168, 170, 186, 187, 185, 189, 173, 237, 236, 238, 206, 198, 199, 195, 193, 225, 241, 243, 242, 210, 218, 219, 217, 221, 220, 156, 158, 159, 151, 147, 145, 144, 176, 180, 182, 166, 167, 163]
	seed = [238, 236, 172, 173, 169, 41, 43, 47, 63, 62, 60, 124, 125, 121, 123, 122, 106, 98, 99, 103, 119, 118, 86, 94, 95, 79, 75, 73, 72, 88, 80, 81, 85, 69, 68, 100, 36, 37, 53, 49, 48, 50, 18, 26, 27, 25, 29, 13, 12, 14, 6, 7, 3, 1, 0, 128, 132, 133, 149, 145, 147, 179, 163, 167, 166, 182, 180, 244, 240, 248, 184, 186, 170, 138, 139, 143, 159, 158, 156, 220, 221, 217, 219, 218, 210, 194, 195, 193, 225, 229]
	
	SnakeGA = SibGA(indsize,fitness,0.9,0.5,popsize,1)
	#SnakeGA.evolve()
	
	for i in range(int(math.floor(popsize * 0.6))):
		newguy = Ind.SnakePath(indsize,"default","default",adjacencies[:])
		#beg = random.randint(1,49)
		#newguy.genome[beg:(beg + len(seed))] = seed
		for j in range(1,len(seed)-5):
			if seed[0] in adjacencies[newguy.genome[j-1]]:
				newguy.setGenes(j,seed)
				#newguy.genome[(j):(j+len(seed))] = seed
				for k in range((j+len(seed)),indsize-1):
					index = random.randint(0,7)
					newguy.setGene(k,adjacencies[newguy.genome[k-1]][index])
					#newguy.genome[k] = adjacencies[newguy.genome[k-1]][index]
				break
		
		SnakeGA.current_pop.members[i] = newguy
		
	SnakeGA.current_pop.evaluatePop()
	
	while SnakeGA.terminator() is None:
		SnakeGA.generation() #Run a generation
		for path in SnakeGA.current_pop.members:
			snake = findSnake(path.genome)
			snakelen = snake[1] - snake[0]
			origfit = fitness(path)
			if snake[0] > 0:
				origval = path.genome[snake[0]-1]
				for change in adjacencies[path.genome[snake[0]]]:
					path.setGene(snake[0]-1,change)
					#path.genome[snake[0]-1] = change
					newsnake = findSnake(path.genome)
					newsnakelen = newsnake[1] - newsnake[0]
					newfit = fitness(path)
					if newfit <= origfit:
						path.setGene(snake[0]-1,origval)
						#path.genome[snake[0]-1] = origval
					else:
						for i in range(1,snake[0]-1):
							index = random.randint(0,7)
							path.setGene(snake[0]-1-i,adjacencies[path.genome[snake[0]-i]][index])
						break
			if snake[1] < (indsize-2):
				origval = path.genome[snake[1]]
				for change in adjacencies[path.genome[snake[1]-1]]:
					path.setGene(snake[1],change)
					#path.genome[snake[1]+1] = change
					newsnake = findSnake(path.genome)
					newsnakelen = newsnake[1] - newsnake[0]
					newfit = fitness(path)
					if newfit <= origfit:
						path.setGene(snake[1],origval)
						#path.genome[snake[1]+1] = origval
					else:
						for i in range(snake[1] + 1,len(path.genome)-1):
							index = random.randint(0,7)
							path.setGene(i,adjacencies[path.genome[i-1]][index])
						break
						
		SnakeGA.current_pop.evaluatePop() #calculate the fitnesses
		SnakeGA.best_scores.append(SnakeGA.current_pop.best) #store the best fitness in this gen
		print SnakeGA.current_pop.best
	
	best = SnakeGA.getBest()
	print "The best solution found was: " + str(best.genome)
	print "The GA ran for %s generations." % SnakeGA.current_gen
	print  str(SnakeGA.best_scores)
	li = findSnake(best.genome)
	print best.genome[li[0]:li[1]]
	print "Available nodes = " + str(li[2])
	
	'''snake1 = [0, 251, 249, 248, 249, 253, 252, 254, 255, 247, 245, 244, 245, 241, 240, 176, 184, 188, 60, 188, 190, 62, 63, 55, 183, 247, 243, 227, 225, 224, 228, 230, 102, 103, 101, 117, 125, 124, 120, 56, 48, 50, 18, 22, 20, 21, 29, 13, 9, 8, 136, 138, 142, 206, 204, 205, 221, 217, 219, 218, 210, 208, 80, 81, 65, 67, 75, 73, 72, 73, 77, 69, 68, 69, 5, 7, 6, 38, 34, 162, 163, 161, 160, 164, 166, 38, 39, 37, 33, 32, 33, 35, 3, 1, 5, 4, 12, 13, 15]
	snake2 = [40,41,43,47,63,62,60,124,125,121,123,122,106,98,99,103,119,118,86,94,95,79,75,73,72,88,80,81,85,69,68,100,36,37,53,49,51,50,18,26,27,25,29,13,12,14,6,7,3,1,0,2]
	
	li1 = findSnake(snake1)
	li2 = findSnake(snake2)
	
	print snake1[li1[0]:li1[1]]
	print len(snake1[li1[0]:li1[1]])
	print "Remaining nodes: " + str(li1[2])
	print snake2[li2[0]:li2[1]]
	print len(snake2[li2[0]:li2[1]])
	print "Remaining nodes: " + str(li2[2])'''


if __name__ == '__main__':
	main()

