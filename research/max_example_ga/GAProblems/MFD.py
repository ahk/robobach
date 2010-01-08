#!/usr/bin/env python
# encoding: utf-8
"""
MFD.py

Runs a Simple GA (as defined in the module SimpGA) on
a Multiple Fault Diagnosis (MFD) problem with 25 potential
diseases.

Uses the Modified Relative Likelihood (MRL) fitness
measure proposed by Dr. Potter.

Created by Max Martin on 2008-01-28.
"""

from __future__ import division
import sys
import os
sys.path.append('../../GA')
import GenGA
import time
import thread
import psyco

psyco.full()

#declare global fields
L3_vals = []
tendencies = []
orig_tend = []
Mplus = []

def intBin(i):
	'''A little hack to convert integers to binary. Adds leading zeros so that each string is 10 bits long.
	Used for auto-runs.'''
	b = []
	while i > 0:
		j = i & 1
		b.insert(0,j)
 		i >>= 1
		
	while len(b) < 10:
		b.insert(0,0)
	return b
	
	
def fitness(individual):
	'''Fitness function for MFD'''
	#Retrieve global fields needed
	global L3_vals
	global tendencies
	global orig_tend
	global Mplus

	#First, calculate L1
	L1 = 1
	for i in range(10):
		if Mplus[i] == 1:
			temp = 1
			for j in range(25):
				if individual.genome[j] == 1:
					temp = temp * (1 - tendencies[i][j])
			L1 = L1 * (1 - temp)

	#Now, calculate L2
	L2 = 1
	for j in range (25):
		#for every disease in the diagnosis
		if individual.genome[j] == 1:
			temp = 1
			for i in range(10):
				#for every symptom
				if (orig_tend[i][j] != 0.0) and (Mplus[i] == 0):
					#if the symptom is associated with the disease and the patient doesn't have it,
					temp = temp * (1 - tendencies[i][j]) #we need this term
			L2 = L2 * temp

	#last, calculate L3
	L3 = 1
	for i in range(25):
		if individual.genome[i] == 1:
			L3 = L3 * L3_vals[i]

	#Now that we have all, calculate the MRL
	L = L1 * L2 * L3
	#This is our fitness
	#print "L1: %s L2: %s L3: %s L: %s" % (L1, L2, L3, L)
	#if L == 0: print individual.string()
	
	return L


def main():
	prior = open("PriorProbabilities")
	prior_probs = []
	for i in range(25):
		prior_probs.append(float(prior.read(20)))
		prior.seek(1,1) #get rid of that pesky newline character
	prior.close()
	
	global L3_vals
	for i in range(25): #Calculate our L3 values for later
		L3_vals.append(prior_probs[i]/(1-prior_probs[i]))
	
	tend = open("TendencyMatrix")
	global tendencies
	global orig_tend
	for i in range(10): #10 symptoms
		tendencies.append([])
		orig_tend.append([])
		for j in range(25): #25 diseases
			val = float(tend.read(20))
			orig_tend[i].append(val) #append to orig list unchanged
			if val == 0:
				val = .000001
			if val == 1:
				val = .999999	
			tendencies[i].append(val) #add fixed values to tendencies
			tend.seek(1,1) #newline character
		tend.seek(1,1) #line between symptoms
	tend.close()
	
	#symptoms = raw_input("Enter a bitstring of the symptoms: ")
	#if len(symptoms) != 10: raise Exception("Symptoms must be 10 bits long")
	
	global Mplus
	#for s in symptoms:
	#	Mplus.append(int(s))
	
	#Fill a matrix with the results from file
	r = open("ExhaustiveResults")
	results = []
	for i in range(1023):
		results.append([])
		s = r.readline()
		temp = s.split()
		for j in range(1,4):
			results[i].append(float(temp[j]))
	r.close()
	
	rel = []
	elitism = (None,1) #change every 27 runs
	popsize = (80,120,160) #change every 9 runs
	xover = (0.4,0.6,0.8) #change every 3 runs
	mutation = (0.001,0.006,0.011) #change every run

	for param in range(54):
		rel.append([])
	
		begin_time = []
		end_time = []
		num_gens = []
		for run in range(10):
			begin_time.append(time.clock())
			rel[param].append(0)
			print "Elitism: " + str(elitism[param//27])
			print "Pop Size: " + str(popsize[(param//9)%3])
			print "Crossover rate: " + str(xover[(param//3)%3])
			print "Mutation rate: " + str(mutation[param%3])
			for sym in range(1,1024):
						
				Mplus = intBin(sym)
				#MFDGA = GenGA.SimpleGA(25,fitness,xover[(param//3)%3],mutation[param%3],popsize[(param//9)%3],elitism[param//27])
				#MFDGA = GenGA.SimpleGA(25,fitness)
				MFDGA = GenGA.SimpleVariantGA2(25,fitness,xover[(param//3)%3],mutation[param%3],popsize[(param//9)%3],elitism[param//27])
				MFDGA.evolve()
				best = MFDGA.getBest().string()
				#print sym
				#print "The GA ran for %s generations." % MFDGA.current_gen
				num_gens.append(MFDGA.current_gen)
				#print "The best score was: " + str(fitness(MFDGA.getBest()))
				if (fitness(MFDGA.getBest())+0.00000001) >= results[sym-1][0]:
					#print "Found best score!"
					rel[param][run] = rel[param][run] + 1
					
			end_time.append(time.clock())
	
			print "Time to complete: %s" % (end_time[run] - begin_time[run])
			
			print "Reliability for best: %s" % ((rel[param][run]/1023) * 100)
				
		#Let's get some averages
		rel_avg = 0
		for r in rel[param]:
			rel_avg += (r/1023) * 100
		rel_avg = rel_avg/10
	
		time_avg = 0
		for i in range(10):
			time_avg += (end_time[i] - begin_time[i])
		time_avg = time_avg/10
		
		gen_sum = 0
		for gen in num_gens:
			gen_sum += gen
	
		print "Average reliability: %s" % rel_avg
		print "Average time: %s" % time_avg
		print "Average gens: %s" % (gen_sum / len(num_gens))
	
	resultfile = open('Results','a')
		
	for param in rel:
		for run in param:
			resultfile.write(str((run/1023)*100) + ",")
			
	resultfile.close()

if __name__ == '__main__':
	main()
