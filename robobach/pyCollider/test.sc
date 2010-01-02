f = File("Cmds.osc","w");


// start a sine oscillator at 0.2 seconds.
c = [ 0.2, [\s_new, \NRTsine, 1001, 0, 0]].asRawOSC;
f.write(c.size); // each bundle is preceeded by a 32 bit size.
f.write(c); // write the bundle data.

// stop sine oscillator at 3.0 seconds.
c = [ 3.0, [\n_free, 1001]].asRawOSC;
f.write(c.size);
f.write(c);

// scsynth stops processing immediately after the last command, so here is
// a do-nothing command to mark the end of the command stream.
c = [ 3.2, [0]].asRawOSC;
f.write(c.size);
f.write(c);

f.close;

// the 'NRTsine' SynthDef
(
SynthDef("NRTsine",{ arg freq = 440;
 Out.ar(0,
   SinOsc.ar(freq, 0, 0.2)
 )
}).writeDefFile;
)
