# This isn't a real shell/python script, but it would like to be! Can you help me become automatable?

./sclang composition.scd &
sleep 3
./scsynth -N composition.osc _ composition.wav 44100 WAVE int16
