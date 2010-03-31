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

outfile_name = now + '.composition'
outcmd = './scsynth -o 2 -N composition.osc _ %(out)s 44100 WAVE int16' % {'out': outfile_name + '.wav'}
server_proc = Popen(outcmd, shell=True)
server_proc.wait()

lamecmd = 'lame --preset extreme %(in)s %(out)s' % {'in': outfile_name + '.wav', 'out': outfile_name + '.mp3' }
lame_encode = Popen(lamecmd, shell=True)
lame_encode.wait()