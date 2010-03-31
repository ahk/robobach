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

# for some reason there is a serious refusal to load kick_05_s which is a stereo wav,
# but elec_sample3 loads just fine ... difference is that elec_sample3 was originally recorded by SC?
score = r'''TempoClock.default.tempo = 1;
g = [
    [0.0, [\b_allocRead, 0, "%(sample1)s"]],
    [0.0, [\b_allocRead, 1, "%(sample2)s"]],
    [0.1, [\s_new, \sine, 1000, 0, 0, \freq, %(freq1)i]],
    [0.2, [\s_new, \sine, 1001, 0, 0, \freq, %(freq2)i]],
    [0.3, [\s_new, \sine, 1002, 0, 0, \freq, %(freq3)i]],
    [1.0, [\s_new, \playSample, 1003, 0, 0, \bufnum, 0]],
    [2.0, [\s_new, \playSample, 1004, 0, 0, \bufnum, 1]],
    [5.0, [\c_set, 0, 0]] // finish
];
''' % { 'sample1': sample_dir + "kick_05_s.wav",
        'sample2': sample_dir + "kick_06_s.wav",
        'freq1': random.randint(440, 700),
        'freq2': random.randint(170,660),
        'freq3': random.randint(220, 1000) }

ending = r'''//convert it to a binary OSC file for use with NRT
Score.write(g, "composition.osc");
"composition successfully compiled".postln;
'''

output = synths + score + ending
outf = open('composition.scd', 'w')
outf.write(output)
outf.close()