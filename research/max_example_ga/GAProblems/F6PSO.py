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
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/PSO')
import Optimizer
import Swarm

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
	

	
def fitness(elts):
	x = (binInt(elts[:22]) * 0.00004768372718899898) - 100
	y = (binInt(elts[22:]) * 0.00004768372718899898) - 100
	
	num = (math.sin(math.sqrt((x**2) + (y**2)))**2) - 0.5
	den = (1 + 0.001*((x**2) + (y**2)))**2
	
	fit = 0.5 + (num/den)
	
	return fit
	
def main():
	bests = []
	
	for i in range(100):
		RunPSO = Optimizer.PSO(fitness,88,Swarm.BinaryParticle,44,-7,7,4,3,0.9)
		RunPSO.optimize()
		best = RunPSO.best
		#print "The best solution found was: " + str(best.genome)
		#print "The PSO ran for %s iterations." % len(best)
		print str(RunPSO.best)
		bests.append(best.pop())
		
	bests.sort()
	print "The bests found were: " + str(bests)


if __name__ == '__main__':
	main()

