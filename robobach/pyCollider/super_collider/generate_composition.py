#!/usr/bin/env python

import random

output = r'''SynthDef(\sine, { arg freq = 440;
    Out.ar(0,
        SinOsc.ar(freq, 0, 0.2) * Line.kr(1, 0, 0.5, doneAction: 2)
    )
}).load(s);

SynthDef(\playSample, { arg bufnum = 0;
	Out.ar(0, DiskIn.ar(2, bufnum));
}).load(s);

TempoClock.default.tempo = 1;
g = [
    [0.0, [\b_allocRead, 0, "/Users/andrew/Desktop/SC Trax/Samples/elec_sample3.wav"]],
    [0.1, [\s_new, \sine, 1000, 0, 0, \freq, %(freq1)i]],
    [0.2, [\s_new, \sine, 1001, 0, 0, \freq, %(freq2)i]],
    [0.3, [\s_new, \sine, 1002, 0, 0, \freq, %(freq3)i]],
    [1.0, [\s_new, \playSample, 1003, 0, 0, \bufnum, 0]],
    [5.0, [\c_set, 0, 0]] // finish
];

//convert it to a binary OSC file for use with NRT
Score.write(g, "composition.osc");
"composition successfully compiled".postln;
''' % {'freq1': random.randint(440, 700), 'freq2': random.randint(170,660), 'freq3': random.randint(220, 1000)}

outf = open('composition.scd', 'w')
outf.write(output)
outf.close()