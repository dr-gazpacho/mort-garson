s.boot;
OSCdef.freeAll;
//until you reboot SC, current environment has references to processes on all servers
currentEnvironment.clear;

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
	//avoid overwriting references to synths
	//if I make 'test' and then another 'test', the first UGEN keeps playing (cont.)
	//I just just my reference to the first one
	if(currentEnvironment.at(name.asSymbol).notNil) {
		postln(currentEnvironment);
        currentEnvironment.at(name.asSymbol).free;
    };
	//this would be the same I think as ~name
    currentEnvironment.put(
        name.asSymbol,
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



