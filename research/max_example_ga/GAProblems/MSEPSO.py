#!/usr/bin/env python
# encoding: utf-8
"""
MSEGA.py

Created by Max Martin on 2008-02-27.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/PSO')
import os
import Optimizer
import Swarm
import time
#import decimal

import psyco
psyco.full()

MSRT = 0
DNVT = 0


def fitness(elts):
	#individual cardinality
	corps = [42,9,168,56,7,92,4]
	sum = 0
	for i in range(7):
		sum += (elts[i]/corps[i]) * 0.142857
	CT = 50/sum
	
	#SEN1 to SEN2 relationship
	if elts[2] > (3 * elts[3]):
		S1S2 = (3*elts[3])/elts[2]
	else:
		if elts[3] != 0:
			S1S2 = elts[2]/(3*elts[3])
		else:
			S1S2 = 0
	
	#UHF connectivity
	available = elts[0] * 12
	X = ((elts[0] - 1) % 4) + 1
	Y = (elts[0] - 1) // 4
	Z = Y + 1
	av_b = (32 * Y) - (X * X) + (13 * X)
	needed = available - av_b + (2*elts[1]+elts[2]+elts[3]+elts[5]+elts[6])
	if abs(available - needed) > 12:
		UHF_conn = needed/available
	else:
		UHF_conn = 1
	
	#Maximum constraint violations
	max_con = 1
	div = [4,1,12,4,1,9,1]
	for i in range(7):
		if elts[i] > (div[i] * Z):
			max_con = 0
	
	#MSRT support
	global MSRT
	sup_MSRT = elts[5] * 25
	if sup_MSRT < MSRT:
		MSRT_sup = 0
	else:
		MSRT_sup = MSRT / sup_MSRT
	
	#DNVT support
	global DNVT
	sup_DNVT = (elts[0]*24) + (elts[1]*176) + (elts[2]*26) + (elts[3]*41)
	if sup_DNVT < DNVT:
		DNVT_sup = 0
	else:
		DNVT_sup = DNVT / sup_DNVT
	
	f = CT * S1S2 * UHF_conn * max_con * MSRT_sup * DNVT_sup
	return f

def main():
	global MSRT
	global DNVT
	MSRT = 672
	DNVT = 1495
	constraints = [1,42,0,9,0,168,0,56,1,7,0,92,0,4] #based on problem
	begin_time = time.clock()
	num_best = 0
	it_sum = 0
	for i in range(10):
		TestPSO = Optimizer.PSO(fitness,100,Swarm.IntegerParticle,7,-7.5,7.5,1,3,0.35,constraints)
		TestPSO.optimize()
		print "The best solution found was: " + str(TestPSO.gbest)
		print "The PSO ran for %s iterations." % len(TestPSO.best)
		it_sum += len(TestPSO.best)
		print "The best scores were: " + str(TestPSO.best)
		if fitness(TestPSO.gbest) > 327:
			num_best += 1
	end_time = time.clock()
	
	print "%s per cent reliability" % (num_best/10)
	print "Took %s seconds on average" % ((end_time - begin_time)/1000)
	print "%s iterations on average" % (it_sum/1000)

if __name__ == '__main__':
	main()

