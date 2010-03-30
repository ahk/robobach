#!/usr/bin/env python

import os
from time import sleep
from subprocess import Popen, PIPE
from datetime import datetime
import re

now = datetime.now().strftime("%y-%m-%d_%H-%M-%S-%f")
client_proc = Popen(['./sclang', 'composition.scd', '&'], stdout=PIPE)

terminating_pat = re.compile('composition successfully compiled')
client_out = ''
while not re.search(terminating_pat, client_out):
    client_out += client_proc.stdout.readline()
client_proc.kill()

outcmd = './scsynth -N composition.osc _ ' + now + '.composition.wav 44100 WAVE int16'
server_proc = Popen(outcmd, shell=True)

server_proc.wait()