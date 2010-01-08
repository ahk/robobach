#!/usr/bin/env python
# encoding: utf-8
"""
TransitionPSO.py

Created by Max Martin on 2008-04-12.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import decimal
import math
import random
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/PSO')
import Optimizer
import Swarm

import psyco
psyco.full()

adjacencies = []
			
def buildSequence(elements):
	global adjacencies
	sequence = [0]
	for transition in elements:
		last = sequence.pop()
		sequence.append(last)
		sequence.append(adjacencies[last][transition])
	
	return sequence

def fitness(elements):
	global adjacencies
	elts = buildSequence(elements)
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
	indsize = 150
	popsize = 1000
	constraints = []
	for i in range(indsize):
		constraints.append(0)
		constraints.append(7)
	table = open("Dimension8Table.txt")
	global adjacencies
	for i in range(256):
		adjacencies.append([])
		s = table.readline()
		temp = s.split()
		for t in temp:
			adjacencies[i].append(int(t))

	table.close()
	
	#from Potter paper
	#seed = [40,41,43,47,63,62,60,124,125,121,123,122,106,98,99,103,119,118,86,94,95,79,75,73,72,88,80,81,85,69,68,100,36,37,53,49,51,50,18,26,27,25,29,13,12,14,6,7,3,1,0,2]
	#89 from seeded GA
	#seed = [0, 1, 3, 7, 6, 14, 12, 13, 29, 25, 27, 26, 18, 50, 51, 49, 53, 37, 36, 100, 68, 69, 85, 81, 80, 88, 72, 73, 75, 79, 95, 94, 86, 118, 119, 103, 99, 98, 106, 122, 123, 121, 125, 124, 60, 62, 63, 47, 43, 41, 40, 168, 170, 186, 187, 185, 189, 173, 237, 236, 238, 206, 198, 199, 195, 193, 225, 241, 243, 242, 210, 218, 219, 217, 221, 220, 156, 158, 159, 151, 147, 145, 144, 176, 180, 182, 166, 167, 163]
	#90 from seeded GA
	#seed = [238, 236, 172, 173, 169, 41, 43, ,47, 63, 62, 60, 124, 125, 121, 123, 122, 106, 98, 99, 103, 119, 118, 86, 94, 95, 79, 75, 73, 72, 88, 80, 81, 85, 69, 68, 100, 36, 37, 53, 49, 48, 50, 18, 26, 27, 25, 29, 13, 12, 14, 6, 7, 3, 1, 0, 128, 132, 133, 149, 145, 147, 179, 163, 167, 166, 182, 180, 244, 240, 248, 184, 186, 170, 138, 139, 143, 159, 158, 156, 220, 221, 217, 219, 218, 210, 194, 195, 193, 225, 229]
	#transition 90
	#seed = [1,6, 0, 2, 7, 1, 2, 4, 0, 1, 6, 0, 2, 1, 0, 4, 3, 0, 2, 4, 0, 5, 3, 0, 4, 2, 1, 0, 4, 3, 0, 2, 4, 0, 5, 6, 0, 4, 2, 0, 1, 5, 3, 0, 1, 2, 4, 0, 1, 3, 0, 2, 1, 0, 7, 2, 0, 4, 2, 1, 5, 4, 2, 0, 4, 1, 6, 2, 3, 6, 1, 4, 5, 0, 2, 4, 0, 1, 6, 0, 2, 1, 0, 3, 4, 0, 1, 5, 2]
	#transition 88
	#seed = [0,1,2,0,3,1,0,4,2,1,0,3,5,0,1,2,4,0,6,5,0,4,2,0,3,4,0,1,2,4,0,3,5,0,4,2,0,3,4,0,1,2,0,6,1,0,4,2,1,0,7,1,4,0,1,2,4,6,0,1,5,3,0,2,1,5,4,1,0,5,3,0,1,2,0,6,1,0,3,2,1,0,5,2,1,4,0,2]
	#transition Potter
	seed = [0,1,2,4,0,1,6,0,2,1,0,4,3,0,2,4,0,5,3,0,4,2,1,0,4,3,0,2,4,0,5,6,0,4,2,1,0,5,3,0,1,2,4,0,1,3,0,2,1,0,1]
	
	vmin = -2
	vmax = 2
	SnakePSO = Optimizer.PSO(fitness,popsize,Swarm.IntegerParticle,indsize,vmin,vmax,7,2,0.2,constraints[:])
	
	best_scores = []

	for i in range(int(math.floor(popsize * 0.05))):
		newguy = Swarm.IntegerParticle(indsize,vmin,vmax,constraints[:])
		beg = random.randint(1,len(newguy.elements)-len(seed)-1)
		newguy.elements[beg:(beg + len(seed))] = seed
		newguy.pbest = newguy.elements[:]
	
		SnakePSO.particles[i] = newguy
		if fitness(newguy.elements) > fitness(SnakePSO.gbest):
			SnakePSO.gbest = newguy.elements[:]
	
	SnakePSO.best.append(fitness(SnakePSO.gbest))

	while SnakePSO.terminator() is None:
		for path in SnakePSO.particles:
			snake = findSnake(buildSequence(path.elements))
			origfit = fitness(path.elements)
			if snake[0] > 0:
				origval = path.elements[snake[0]-1]
				for i in range(8):
					path.elements[snake[0]-1] = i
					newfit = fitness(path.elements)
					if newfit <= origfit:
						#path.setGene(snake[0]-1,origval)
						path.elements[snake[0]-1] = origval
					else:
						path.pbest = path.elements[:]
						if newfit > fitness(SnakePSO.gbest):
							SnakePSO.gbest = path.elements[:]
						break
			if snake[1] < (indsize-2):
				origval = path.elements[snake[1]]
				for i in range(8):
					#path.setGene(snake[1],i)
					path.elements[snake[1]] = i
					newfit = fitness(path.elements)
					if newfit <= origfit:
						#path.setGene(snake[1],origval)
						path.elements[snake[1]] = origval
					else:
						path.pbest = path.elements[:]
						if newfit > fitness(SnakePSO.gbest):
							SnakePSO.gbest = path.elements[:]
						break
		
		SnakePSO.iterate() #Run a generation			
		current_best = fitness(SnakePSO.gbest)
		SnakePSO.best.append(current_best)
		print current_best

	best = SnakePSO.gbest
	print "The best solution found was: " + str(best)
	print "The PSO ran for %s iterations." % len(SnakePSO.best)
	print str(SnakePSO.best)
	#bests.append(SnakeGA.best_scores[-1])
	li = findSnake(buildSequence(best))
	#seed = best.elements[li[0]:li[1]]
	print best[li[0]:li[1]]
	print buildSequence(best)[li[0]:li[1]]
	print "Available nodes = " + str(li[2])



if __name__ == '__main__':
	main()

