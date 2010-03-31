#!/usr/bin/env python
import os
import time

for i in range(0,20):
    os.system('./generate_composition.py')
    time.sleep(1)
    os.system('./build_composition.py')
    time.sleep(1)