#!/usr/bin/env python
# encoding: utf-8
"""
Population.py

Created by Max Martin on 2008-01-26.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from __future__ import division
import sys
import os
import Ind
import random

class Population:
	'''Class to represent a population of individuals to be operated on by a genetic algorithm.'''
	def __init__(self,size,chromosome,length,fitness,mutation,crossover,constraints,roulette=None,empty=None):
		members = []
		#if not issubclass(chromosome, Ind.Individual):
			#raise Exception("Chromosome type must be a subclass of Individual.")
		if empty is None:
			'''fill the population with random individuals
			this will only not be true for Generational GAs creating empty populations
			for the next generation'''
			for i in range(size):
				if constraints is None:
					x = chromosome(length,mutation,crossover)
				else:
					x = chromosome(length,mutation,crossover,constraints[:])
				members.append(x)
		self.members = members
		self.size = size
		self.chromosome = chromosome
		self.fitness_function = fitness
		self.best = 0
		self.ratios = []
		self.fitnesses = []
		self.fitness_sum = 0
		self.roulette = roulette
		if empty is None: self.evaluatePop()

	def add(self, individual):
		'''Only for use in generational GAs, this adds a member to the population'''
		if len(self.members) >= self.size: raise Exception("Cannot add to a full population")
		if not isinstance(individual, self.chromosome): raise Exception("Individual is of the wrong type")
		#now that we've checked that the population isn't full and the
		#new individual is of the right type, add him
		self.members.append(individual)
		
	def evaluatePop(self):
		'''Evaluate the fitness of every member of the population and determine their ratio'''
		fitnesses = []
		fitness_sum = 0
		best_fitness = 0
		for member in self.members:
			n = self.fitness_function(member)
			fitnesses.append(n)
			fitness_sum += n
			if n > best_fitness: 
				best_fitness = n
		if self.roulette is not None:
			ratios = [] #to be used for roulette wheel selection
			ratios.append(fitnesses[0]/fitness_sum)
			for i in range(1,self.size):
				ratios.append((fitnesses[i]/fitness_sum) + ratios[i-1])
			self.ratios = ratios
		self.fitnesses = fitnesses
		self.fitness_sum = fitness_sum
		self.best = best_fitness
	
	
	def rouletteWheel(self):
		'''Returns a member of the population wheel selected by the roulette wheel scheme'''
	 	num = random.random()
		for i in range(self.size):
			if num < self.ratios[i]: return self.members[i]
			
	def binaryTournament(self):
		'''Returns a member of the population selected by a binary tournament'''
		num1 = random.randrange(self.size)
		num2 = random.randrange(self.size)
		if self.fitnesses[num1] > self.fitnesses[num2]:
			return self.members[num1]
		else:
			return self.members[num2]
	
	def ternaryTournament(self):
		
		num1 = random.randrange(self.size)
		num2 = random.randrange(self.size)
		num3 = random.randrange(self.size)
		maxfi = max([self.fitnesses[num1],self.fitnesses[num2],self.fitnesses[num3]])
		for num in [num1,num2,num3]:
			if self.fitnesses[num] == maxfi:
				return self.members[num]
	
	def quaternaryTournament(self):
		num1 = random.randrange(self.size)
		num2 = random.randrange(self.size)
		num3 = random.randrange(self.size)
		num4 = random.randrange(self.size)
		maxfi = max([self.fitnesses[num1],self.fitnesses[num2],self.fitnesses[num3],self.fitnesses[num4]])
		for num in [num1,num2,num3,num4]:
			if self.fitnesses[num] == maxfi:
				return self.members[num]