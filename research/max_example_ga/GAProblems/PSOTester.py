#!/usr/bin/env python
# encoding: utf-8
"""
PSOTester.py

Created by Max Martin on 2008-02-16.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/PSO')
import Optimizer
import Swarm


def fitness(elements):
	f = 1
	for e in elements:
		if e == 1:
			f = f + 1
	return f

def main():
	TestPSO = Optimizer.PSO(fitness,20,Swarm.BinaryParticle,10,-4,4,2,2)
	TestPSO.optimize()
	print TestPSO.gbest
	print len(TestPSO.best)


if __name__ == '__main__':
	main()

