// see this doc for a starting point:
// http://supercollider.svn.sourceforge.net/viewvc/supercollider/trunk/build/Help/Control/Score.html

// the 'NRTsine' SynthDef
SynthDef("NRTsine",{ arg freq = 440;
 Out.ar(0,
   SinOsc.ar(freq, 0, 0.2)
 )
}).writeDefFile;

g = [
 [0.1, [\s_new, \NRTsine, 1000, 0, 0, \freq, 440]],  
 [0.2, [\s_new, \NRTsine, 1001, 0, 0, \freq, 660]],
 [0.3, [\s_new, \NRTsine, 1002, 0, 0, \freq, 220]],
 [2, [\c_set, 0, 0]]
 ];
o = ServerOptions.new.numOutputBusChannels = 1; // mono output
Score.recordNRT(g, "Commands.osc", "test.aiff", options: o); // synthesize