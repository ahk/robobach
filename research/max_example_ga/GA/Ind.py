#!/usr/bin/env python
# encoding: utf-8
"""
Individual.py

Created by Max Martin on 2008-01-26.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import random
import sys
import os


class Individual:
	'''Abstract class to represent an individual. Must be implemented for a specific chromosome.'''
	def __init__(self, length):
		self.age = 1
		self.length = length
		
	def mutate(self, index):
		""
		raise Exception("Mutator must be specified in subclass.")

	def crossover(self, other):
		raise Exception("Crossover must be specified in subclass.")
		
class IntArray(Individual):
	'''Class to represent an array of integers'''
	def __init__(self,length,mut,cross,constraints,empty=None):
		Individual.__init__(self,length)
		genome = []
		
		if len(constraints) != (2*length):
			Exception("Constraints must be provided for every allele.")
		#split the constraints list into minimums & maximums
		mins = []
		maxs = []
		self.constraints = constraints[:]
		for i in range(length):
			mins.append(constraints.pop(0))
			maxs.append(constraints.pop(0))
		
		if empty is None:
			for i in range(length):
				genome.append(random.randint(mins[i],maxs[i]))
		
		self.mins = mins
		self.maxs = maxs
		self.genome = genome
		self.mut = mut
		self.cross = cross
		
	def copy(self):
		mycopy = IntArray(self.length,self.mut,self.cross,self.constraints[:],1)
		mycopy.genome.extend(self.genome)
		return mycopy
		
	def setGene(self,index,value):
		self.genome[index] = value
		return
	
	def mutate(self,index):
		'''Uniform random mutation'''
		if (self.mut == "default") or (self.mut == "uniform"):
			self.genome[index] = random.randint(self.mins[index],self.maxs[index])
			
		if self.mut == "age-based":
			ran = self.maxs[index] - self.mins[index]
			base = random.randint(-ran,ran)
			change = base/self.age
			if (self.genome[index] + change) < self.maxs[index]:
				if (self.genome[index] + change) > self.mins[index]:
					self.genome[index] += change
				else:
					self.genome[index] = self.mins[index]
			else:
				self.genome[index] = self.maxs[index]
	
	def crossover(self,other):
		'''1-point crossover for IntArrays. Returns two new individuals'''
		if (self.cross == "default") or (self.cross == "1point"):
			#Generate the crossover point
			point = random.randint(1,(self.length-1))
			#Create two new individuals with empty genomes via optional second argument
			new_individual1 = IntArray(self.length,self.mut,self.cross,self.constraints[:],1)
			new_individual1.age = self.age + 1
			new_individual2 = IntArray(self.length,self.mut,self.cross,self.constraints[:],1)
			new_individual2.age = self.age + 1
			#Fill first individual with genetic material
			new_individual1.genome.extend(self.genome[:point])
			new_individual1.genome.extend(other.genome[point:])
			#Fill second individual with first individual's complement
			new_individual2.genome.extend(other.genome[:point])
			new_individual2.genome.extend(self.genome[point:])
			return [new_individual1, new_individual2]
			
				

class BitString(Individual):
	'''Chromosome to represent a bit string individual.'''
	def __init__(self,length,mut,cross,empty=None):
		Individual.__init__(self, length)
		genome = []
		if empty is None:
			for i in range(length):
				genome.append(random.randint(0,1))
		self.genome = genome
		self.cross = cross
		self.mut = mut

	def mutate(self, index):
		if (self.mut == "default") or (self.cross == "bitflip"):
			'''Bit-flip mutation for bitstring'''
			if self.genome[index] == 0: 
				self.genome[index] = 1
			else:
				self.genome[index] = 0
				
		if self.mut == "swap":
			if index == 0: #swap on the right
				temp = self.genome[index + 1]
				self.genome[index + 1] = self.genome[index]
				self.genome[index] = temp
			else: #swap on the left
				temp = self.genome[index]
				self.genome[index] = self.genome[index - 1]
				self.genome[index - 1] = temp

	def crossover(self, other):
		if (self.cross == "default") or (self.cross == "1point"):
			'''1-point crossover for Bitstrings. Returns two new individuals'''
			#Generate the crossover point
			point = random.randint(1,(self.length-1))
			#Create two new individuals with empty genomes via optional second argument
			new_individual1 = BitString(self.length,self.mut,self.cross,1)
			new_individual2 = BitString(self.length,self.mut,self.cross,1)
			#Fill first individual with genetic material
			new_individual1.genome.extend(self.genome[:point])
			new_individual1.genome.extend(other.genome[point:])
			#Fill second individual with first individual's complement
			new_individual2.genome.extend(other.genome[:point])
			new_individual2.genome.extend(self.genome[point:])
			return [new_individual1, new_individual2]
			
		if self.cross == "uniform":
			new_individual1 = BitString(self.length,self.mut,self.cross,1)
			new_individual2 = BitString(self.length,self.mut,self.cross,1)
			for i in range(self.length):
				if random.randint(0,1) == 0:
					new_individual1.genome.append(self.genome[i])
					new_individual2.genome.append(other.genome[i])
				else:
					new_individual1.genome.append(other.genome[i])
					new_individual2.genome.append(self.genome[i])

			return [new_individual1, new_individual2]
	
	def string(self):
		'''Returns a string representation of the individual'''
		out = ""
		for gene in self.genome:
			out += str(gene)
		return out
		
class SnakePath(Individual):
	def __init__(self,length,mut,cross,table,empty=None):
		Individual.__init__(self,length)
		genome = []
		if empty is None:
			genome.append(random.randint(0,255))
			for i in range(1,length-1):
				index = random.randint(0,7)
				genome.append(table[genome[i-1]][index])
		self.genome = genome
		self.cross = cross
		self.mut = mut
		self.table = table
	
	def setGene(self,index,value):
		self.genome[index] = value
		return
		
	def setGenes(self,index,values):
		self.genome[index:(index + len(values))] = values
		return
	
	def mutate(self,index):
		if self.mut == "default":
			elts = self.genome
			length = 2
			maxlength = 2
			illegal = []
			lengths = []
			maxillegal = []
			for i in range(2,(len(elts)-1)):
				for ad in self.table[elts[i-2]]:
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
			origfitness = maxlength
			if (index > self.length-3) or (index == 0):
				return
			for node in self.table[self.genome[index-1]]:
				if (self.genome[index+1] in self.table[node]) and (node != self.genome[index]):
					origval = self.genome[index]
					self.genome[index] = node
					
					elts = self.genome
					length = 2
					maxlength = 2
					illegal = []
					lengths = []
					maxillegal = []
					for i in range(2,(len(elts)-1)):
						for ad in self.table[elts[i-2]]:
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
					if maxlength < origfitness:
						self.genome[index] = origval
						#print "bad mutation"
						return
					else:
						#print "good mutation! old fitness " + str(origfitness) + " new fitness " + str(maxlength)
						return
					
	
	def copy(self):
		mycopy = SnakePath(self.length,self.mut,self.cross,self.table,1)
		mycopy.genome.extend(self.genome)
		return mycopy
		
	def crossover(self,other):
		if (self.cross == "default") or (self.cross == "enhanced_edge"):
			edges = []
			for i in range(256):
				edges.append([])
			for i in range(self.length - 2):
				edges[self.genome[i]].append(self.genome[i-1])
				edges[self.genome[i]].append(self.genome[i+1])
			for i in range(self.length - 2):
				if other.genome[i-1] in edges[other.genome[i]]:
					edges[other.genome[i]].remove(other.genome[i-1])
					edges[other.genome[i]].append(-other.genome[i-1])
				else:
					edges[other.genome[i]].append(other.genome[i-1])
				if other.genome[i+1] in edges[other.genome[i]]:
					edges[other.genome[i]].remove(other.genome[i+1])
					edges[other.genome[i]].append(-other.genome[i+1])
				else:
					edges[other.genome[i]].append(other.genome[i+1])
			
			new_individual = SnakePath(self.length,self.mut,self.cross,self.table[:],1)
			if random.randint(0,1) == 0:
				parent = self
			else:
				parent = other
			
			newnode = parent.genome[0]
			while len(new_individual.genome) < len(parent.genome):
				new_individual.genome.append(newnode)
				for i in range(256):
					if newnode in edges[i]:
						edges[i].remove(newnode)
					if -newnode in edges[i]:
						edges[i].remove(-newnode)
				newnew = 1000
				if edges[newnode] != []:
					if len(edges[newnode]) == 1:
						if edges[newnode][0] > 0:
							newnew = edges[newnode][0]
						else:
							newnew = -edges[newnode][0]
					for e in edges[newnode]:
						if (e < 0) and newnew == 1000:
							newnew = -e
					shor = 1000
					if newnew == 1000:
						for e in edges[newnode]:
							if len(edges[e]) < shor:
								shor = len(edges[e])
								newnew = e
					newnode = newnew
				else:
					newnew = -1
					for edge in self.table[newnode]:
						if (edge not in new_individual.genome) and (newnew < 0):
							newnew = edge
					if newnew < 0:
						newnew =  self.table[newnode][random.randint(0,7)]
					'''while newnew < 0:
						num = random.randint(0,255)
						if num not in new_individual.genome:
							newnew = num'''
					newnode = newnew
					
			
			return [new_individual]