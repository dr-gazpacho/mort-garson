s.boot;

SynthDef.new(\rest, {
	| freq = 440, out = 0 |
	Out.ar(out, SinOsc.ar(freq, 0, 0.2))
}).add;

s.plotTree;
/*~rest = Synth.new(\rest);*/

/*~rest.set(\freq, 220);*/

OSCFunc({
	|msg, time, addr, recvPort|
    var freq = msg[1];
	~rest.set(\freq, freq)
}, '/synth/params');

OSCFunc({
	|msg, time, addr, recvPort|
	~rest.free;
}, '/synth/free');


/*~rest.free;*/
