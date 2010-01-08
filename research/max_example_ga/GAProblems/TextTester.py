#!/usr/bin/env python
# encoding: utf-8
"""
TextTester.py

Created by Max Martin on 2008-01-30.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import sys
import os


def main():
	array = []
	for i in range(10):
		array.append([])
		for j in range(30):
			array[i].append(j)
			
	resultfile = open('TestResults','a')
			
	for sub in array:
		for ind in sub:
			resultfile.write(str(ind) + ",")
			
	resultfile.close()
		

if __name__ == '__main__':
	main()

