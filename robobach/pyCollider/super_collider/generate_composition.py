#!/usr/bin/env python

import random
import os

sample_dir = os.getcwd() + '/samples/'
synths = r'''SynthDef(\sine, { arg freq = 440;
    Out.ar(0,
        SinOsc.ar(freq, 0, 0.2) * Line.kr(1, 0, 0.5, doneAction: 2)
    )
}).load(s);

SynthDef(\playSample, { arg bufnum = 0;
	Out.ar(0, DiskIn.ar(2, bufnum));
}).load(s);
'''

comp_length_in_beats = 64
note_set = ''
for i in range(0,comp_length_in_beats):
    note_set += r'''
        [%(b1)f, [\s_new, \sine, 1000, 0, 0, \freq, %(freq1)i]],
        [%(b2)f, [\s_new, \sine, 1001, 0, 0, \freq, %(freq2)i]],
        [%(b3)f, [\s_new, \sine, 1002, 0, 0, \freq, %(freq3)i]],
    ''' % { 'b1': i + (i * 0.1),
            'b2': i + (i * 0.13),
            'b3': i + (i * 0.15),
            'freq1': random.randint(440, 700),
            'freq2': random.randint(170,660),
            'freq3': random.randint(220, 1000) }

score = r'''TempoClock.default.tempo = 2;
g = [
    %(note_set)s
    [%(length)i, [\c_set, 0, 0]] // finishing command forces server to render everything else first before exiting
];
''' % {'note_set': note_set,
       'length': comp_length_in_beats + 1,
    }

ending = r'''//convert it to a binary OSC file for use with NRT
Score.write(g, "composition.osc");
"composition successfully compiled".postln;
'''

output = synths + score + ending
outf = open('composition.scd', 'w')
outf.write(output)
outf.close()