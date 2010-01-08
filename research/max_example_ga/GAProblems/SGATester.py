#!/usr/bin/env python
# encoding: utf-8
"""
Tester.py

Designed to test the Simple GA classes in PyGMy.

Created by Max Martin on 2008-01-28.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/GA')
import GenGA


def fitness(individual):
	f = 1



	return f

def main():
	constraints = []
	for i in range(10):
		constraints.append(-20) #min
		constraints.append(20) #max
	TestGA = GenGA.SimpleIntGA(10,fitness,constraints)
	TestGA.evolve()
	best = TestGA.getBest().string()
	print "The best solution found was: " + best
	print "The GA ran for %s generations." % TestGA.current_gen
	print "The best scores were: " + str(TestGA.best_scores)


if __name__ == '__main__':
	main()

