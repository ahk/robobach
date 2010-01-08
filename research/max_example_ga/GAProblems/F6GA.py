#!/usr/bin/env python
# encoding: utf-8
"""
F6GA.py

Created by Max Martin on 2008-03-04.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import decimal
import math
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/GA')
import GenGA
import Ind

import psyco
psyco.full()

def binInt(binary):
	'''Converts binary list to integer'''
	num = 0
	pow = 0
	b = binary[:]
	
	while len(b) > 0:
		num += b.pop() * (2 ** pow)
		pow += 1
		
	
	return num
	

class F6GA(GenGA.GenerationalGA):
	def __init__(self,chr_len,fitness,cross=.8,mut=0.006,popsize=300,elitism=None):
		GenGA.GenerationalGA.__init__(self,Ind.BitString,chr_len,fitness,"quaternaryTournament",cross,mut,popsize,elitism,"swap","uniform")
		
	def terminator(self):
		if self.current_gen < 10: return None
		if self.best_scores[self.current_gen] == (self.best_scores[self.current_gen - 10]): 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!

	
def fitness(individual):
	x = (binInt(individual.genome[:22]) * 0.00004768372718899898) - 100
	y = (binInt(individual.genome[22:]) * 0.00004768372718899898) - 100
	
	num = (math.sin(math.sqrt((x**2) + (y**2)))**2) - 0.5
	den = (1 + 0.001*((x**2) + (y**2)))**2
	
	fit = 0.5 + (num/den)
	
	return fit
	
def main():
	bests = []
	
	for i in range(100):
		RunGA = F6GA(44,fitness,0.6,0.01,3000,1)
		RunGA.evolve()
		best = RunGA.getBest()
		#print "The best solution found was: " + str(best.genome)
		#print "The GA ran for %s generations." % RunGA.current_gen
		print  str(RunGA.best_scores)
		bests.append(fitness(best))
		
	bests.sort()
	print "The bests found were: " + str(bests)


if __name__ == '__main__':
	main()

