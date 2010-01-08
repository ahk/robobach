#!/usr/bin/env python
# encoding: utf-8
"""
GenerationalGA.py

Classes to represent the general generational GA, as well as
specific instances like the Simple GA.

Created by Max Martin on 2008-01-26.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import Pop
import Ind
import random


class GenerationalGA:
	"""Class that represents a Generational GA"""
	
	
	def __init__(self,chromosome,chr_len,fitness,selector,c_prob,m_prob,popsize,elitism,mutation="default",crossover="default",constraints=None):
		#Define attributes
		self.popsize = popsize
		if selector == "rouletteWheel":
			self.current_pop = Pop.Population(popsize,chromosome,chr_len,fitness,mutation,crossover,constraints,1) #create a roulette population
		else:
			self.current_pop = Pop.Population(popsize,chromosome,chr_len,fitness,mutation,crossover,constraints) #create a normal population
		self.current_gen = 0
		self.selector = selector
		self.crossover_prob = c_prob
		self.mutate_prob = m_prob
		self.best_scores = [self.current_pop.best]
		self.fitness = fitness
		self.chr_len = chr_len
		self.chromosome = chromosome
		self.selector = selector
		self.elitism = elitism
		self.mutation = mutation
		self.crossover = crossover
		self.constraints = constraints
		#Check to make sure the input selector is valid
		if selector not in dir(self.current_pop): raise Exception("Invalid selector")
		
	def evolve(self):
		'''Run the GA until termination criterion is reached'''
		while self.terminator() is None:
			self.generation() #Run a generation
			self.current_pop.evaluatePop() #calculate the fitnesses
			self.best_scores.append(self.current_pop.best) #store the best fitness in this gen
			#print self.current_pop.best
			

	def generation(self):
		'''Runs one generation of the GA'''
		if self.selector == "rouletteWheel":
			new_pop = Pop.Population(self.popsize,self.chromosome,self.chr_len,self.fitness,self.mutation,self.crossover,self.constraints,1,1) #create an empty population
		else:
			new_pop = Pop.Population(self.popsize,self.chromosome,self.chr_len,self.fitness,self.mutation,self.crossover,self.constraints,None,1) #create an empty population
		count = 0
		if self.elitism is not None: #Let's be elite
			free_ride = self.getBest().copy()
			new_pop.add(free_ride)
			count = count + 1

		while(count < self.popsize): #add individuals to the new population
			#Parents will be chosen using input selector function
			parent1 = getattr(self.current_pop,self.selector)() #select a parent
			parent2 = getattr(self.current_pop,self.selector)() #select another parent
			if random.random() < self.crossover_prob: #crossover time!
				new_individuals = parent1.crossover(parent2) #Create new children through crossover
				#Grab children from returned list
				new_individual1 = new_individuals[0]
				if len(new_individuals) > 1:
					new_individual2 = new_individuals[1]
				for allele in range(self.chr_len): #give each gene a chance to be mutated
					if random.random() < self.mutate_prob:
						new_individual1.mutate(allele)
				if len(new_individuals) > 1:
					for allele in range(self.chr_len): #give each gene a chance to be mutated
						if random.random() < self.mutate_prob:
							new_individual2.mutate(allele)
				new_pop.add(new_individual1)
				count = count + 1
				if (len(new_pop.members) < self.popsize) and (len(new_individuals) > 1): #don't want to overfill the population!
					new_pop.add(new_individual2)
					count = count + 1
			else: #no crossover; just go through mutation and add parents as-is
				for allele in range(self.chr_len): #give each gene a chance to be mutated
					if random.random() < self.mutate_prob:
						parent1.mutate(allele)
				for allele in range(self.chr_len): #give each gene a chance to be mutated
					if random.random() < self.mutate_prob:
						parent2.mutate(allele)
				new_pop.add(parent1)
				count = count + 1
				if len(new_pop.members) < self.popsize: #don't want to overfill the population!
					new_pop.add(parent2)
					count = count + 1
		#Our new population is now full - it becomes the current population
		self.current_pop = new_pop
		self.current_gen = self.current_gen + 1
		
	
	def terminator(self):
		'''Termination criterion must be specified by a GA subclass'''
		pass
			
	def getBest(self):
		'''Return the best individual'''
		for member in self.current_pop.members:
			if self.fitness(member) == self.current_pop.best:
				return member
				
				
class SimpleGA(GenerationalGA):
	def __init__(self, chr_len, fitness, cross=.6, mut=.006, popsize=200, elitism=None):
		'''Create a Generational GA to Simple GA specifications'''
		GenerationalGA.__init__(self, Ind.BitString, chr_len, fitness, "rouletteWheel", cross, mut, popsize, elitism)
		
	def terminator(self):
		'''Check if the best fitness has improved in the last 5 generations'''
		if self.current_gen < 5: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 5]: 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!
		
class SimpleIntGA(GenerationalGA):
	def __init__(self,chr_len,fitness,cons,cross=.6,mut=0.006,popsize=200,elitism=None):
		GenerationalGA.__init__(self,Ind.IntArray,chr_len,fitness,"quaternaryTournament",cross,mut,popsize,elitism,"default","default",cons)
		
	def terminator(self):
		if self.current_gen < 10: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 10]: 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!
			
class SimpleVariantGA1(GenerationalGA):
	def __init__(self, chr_len, fitness, cross=.6, mut=.006, popsize=200, elitism=None):
		'''Create a Generational GA to a variant of Simple GA specifications'''
		GenerationalGA.__init__(self, Ind.BitString, chr_len, fitness, "rouletteWheel", cross, mut, popsize, elitism)
		
	def terminator(self):
		'''Check if the best fitness has improved in the last 5 generations'''
		if self.current_gen < 10: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 10]: 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!

class SimpleVariantGA2(GenerationalGA):
	def __init__(self, chr_len, fitness, cross=.6, mut=.006, popsize=200, elitism=None):
		'''Create a Generational GA to a variant of Simple GA specifications'''
		GenerationalGA.__init__(self, Ind.BitString, chr_len, fitness, "binaryTournament", cross, mut, popsize, elitism)

	def terminator(self):
		'''Check if the best fitness has improved in the last 5 generations'''
		if self.current_gen < 5: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 5]: 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!
			
class SimpleVariantGA3(GenerationalGA):
	def __init__(self, chr_len, fitness, cross=.6, mut=.006, popsize=200, elitism=None):
		'''Create a Generational GA to a variant of Simple GA specifications'''
		GenerationalGA.__init__(self, Ind.BitString, chr_len, fitness, "binaryTournament", cross, mut, popsize, elitism)

	def terminator(self):
		'''Check if the best fitness has improved in the last 10 generations'''
		if self.current_gen < 10: return None
		if self.best_scores[self.current_gen] == self.best_scores[self.current_gen - 10]: 
			return 1 #GA has converged
		else:
			return None #There is work to be done yet!
			
