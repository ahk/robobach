#!/usr/bin/env python
# encoding: utf-8
"""
MSEGA.py

Created by Max Martin on 2008-02-27.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
sys.path.append('/Users/max/Documents/classes/CS/8940/PyCOP/GA')
import os
import GenGA
import Ind
import time
#import decimal

import psyco
psyco.full()

MSRT = 0
DNVT = 0
fitness_count = 0

class MSEGA(GenGA.GenerationalGA):
	def __init__(self,chr_len,fitness,cons,cross=.8,mut=0.15,popsize=500,elitism=None):
		GenGA.GenerationalGA.__init__(self,Ind.IntArray,chr_len,fitness,"quaternaryTournament",cross,mut,popsize,elitism,"age-based","default",cons)
		
	def terminator(self):
		if self.current_gen < 10: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 10]:
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!
			
class NaiveMSEGA(GenGA.GenerationalGA):
	def __init__(self,chr_len,fitness,cons,cross=.8,mut=0.15,popsize=500,elitism=None):
		GenGA.GenerationalGA.__init__(self,Ind.IntArray,chr_len,fitness,"quaternaryTournament",cross,mut,popsize,elitism,"default","default",cons)

	def terminator(self):
		if self.current_gen < 5: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 5]: 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!

def fitness(individual):
	elts = individual.genome[:]
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
	global fitness_count
	fitness_count += 1
	return f

def main():
	global MSRT
	global DNVT
	MSRT = 672
	DNVT = 1495
	constraints = [1,42,0,9,0,168,0,56,1,7,0,92,0,4] #based on problem
	begin_times = []
	num_best = []
	gen_sum = []
	end_times = []
	fitness_evals = []
	global fitness_count

	popsizes = (300,400,500)
	mutationrates = (0.05,0.1,0.15)
	for param in range(9):
		print 'Pop Size: ' + str(popsizes[(param//3)%3])
		print 'Mut Rate: ' + str(mutationrates[param%3])
		gen_sum.append(0)
		num_best.append(0)
		begin_times.append(time.clock())
		for run in range(1000):
			TestGA = MSEGA(7,fitness,constraints,0.8,mutationrates[param%3],popsizes[(param//3)%3])
			TestGA.evolve()
			best = TestGA.getBest()
			#print "The best solution found was: " + str(best.genome)
			#print "The GA ran for %s generations." % TestGA.current_gen
			gen_sum[param] += TestGA.current_gen
			#print "The best scores were: " + str(TestGA.best_scores)
			if fitness(best) > 327:
				num_best[param] += 1
		end_times.append(time.clock())
		
		fitness_evals.append(fitness_count)
		fitness_count = 0
		
		print "%s per cent reliability" % (num_best[param]/10)
		print "Took %s seconds on average" % ((end_times[param] - begin_times[param])/1000)
		print "%s generations on average" % (gen_sum[param]/1000)
		print "%s average fitness evals" % (fitness_evals[param]/1000)
		
	'''for param in range(9):
		print 'Pop Size: ' + str(popsizes[(param//3)%3])
		print 'Mut Rate: ' + str(mutationrates[param%3])
		gen_sum.append(0)
		num_best.append(0)
		begin_times.append(time.clock())
		for run in range(1000):
			TestGA = NaiveMSEGA(7,fitness,constraints,0.8,mutationrates[param%3],popsizes[(param//3)%3])
			TestGA.evolve()
			best = TestGA.getBest()
			#print "The best solution found was: " + str(best.genome)
			#print "The GA ran for %s generations." % TestGA.current_gen
			gen_sum[param+9] += TestGA.current_gen
			#print "The best scores were: " + str(TestGA.best_scores)
			if fitness(best) > 327:
				num_best[param+9] += 1
		end_times.append(time.clock())
		
		fitness_evals.append(fitness_count)
		fitness_count = 0

		print "%s per cent reliability" % (num_best[param+9]/10)
		print "Took %s seconds on average" % ((end_times[param+9] - begin_times[param+9])/1000)
		print "%s generations on average" % (gen_sum[param+9]/1000)
		print "%s average fitness evals" % (fitness_evals[param+9]/1000)
		'''
	print 'Reliabilities:'
	print [rel/10 for rel in num_best]
	print 'Generations:'
	print [gs/1000 for gs in gen_sum]
	print 'Evals:'
	print [fe/1000 for fe in fitness_evals]

if __name__ == '__main__':
	main()

