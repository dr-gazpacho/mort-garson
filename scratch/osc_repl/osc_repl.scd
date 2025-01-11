s.boot;

SynthDef.new(\basicSine, {
	| freq = 440, out = 0 |
	Out.ar(out, SinOsc.ar(freq.lag(2), 0, 0.1))
}).add;

s.plotTree;

//create synth with given name
OSCFunc({
	|msg, time, addr, recvPort|
    var name = msg[1];
	var freq = msg[2];
	//this would be the same I think as ~name
    currentEnvironment.put(
        (name).asSymbol,
        Synth(\basicSine, [\freq, freq])
    );
}, '/synth/create');

// Simple test OSC handler that just prints
OSCFunc({ |msg, time, addr, recvPort|
    "Got test message!".postln;
    msg.postln;
}, '/test/simple');

//update frequency of synth with given name
OSCFunc({
	|msg, time, addr, recvPort|
	var name = msg[1];
    var freq = msg[2];
	currentEnvironment.at(name.asSymbol).set(\freq, freq)
}, '/synth/params');

//remove synth with a given name
OSCFunc({
	|msg, time, addr, recvPort|
	var name = msg[1];
	currentEnvironment.at(name.asSymbol).free;
}, '/synth/free');

//kill all processes
OSCFunc({
	|msg|
	CmdPeriod.run;
}, '/synth/freeAll');



