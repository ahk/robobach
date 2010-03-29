// see this doc for a starting point:
// http://supercollider.svn.sourceforge.net/viewvc/supercollider/trunk/build/Help/Control/Score.html

// currently we can't get at the newly defined synths. there is something OSC can do, like
// \d_load, <path-to-synth> that I oughta check on before ruling out synth defining

SynthDef("testSin",{ arg freq = 440;
	Out.ar(0,
		 SinOsc.ar(freq, 0, 0.2) * Line.kr(1, 0, 0.5, doneAction: 2)
	)
}).load(s);

// write a sample file for testing
TempoClock.default.tempo = 1;
g = [
	[0.1, [\s_new, \testSin, 1000, 0, 0, \freq, 440]],	[0.2, [\s_new, \testSin, 1001, 0, 0, \freq, 660]],
	[0.3, [\s_new, \testSin, 1002, 0, 0, \freq, 220]],
	[1, [\c_set, 0, 0]] // finish
];

//convert it to a binary OSC file for use with NRT
Score.write(g, "composition.osc");
"composition successfully compiled".postln;