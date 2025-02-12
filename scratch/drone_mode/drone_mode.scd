(
//init/cleanup
s.reboot;
s.boot;
s.newBusAllocators;
s.freeAll;
OSCdef.freeAll;
~v = s.volume;
//until you reboot SC, current environment has references to processes on all servers

s.waitForBoot({
    s.plotTree;
    SynthDef(\fm, {
        arg freq=500, mRatio=1, cRatio=1, index=1, amp=0.2;
        var car, mod, env;
        mod = SinOsc.ar(freq * mRatio, mul:freq * mRatio);
        car = SinOsc.ar(freq * cRatio + mod) * amp;
        //direct out/reverb send
        Out.ar(0, car);
    }).add;

	OSCdef.new(\entry, {
		|msg, time, addr, recvPort|
		var red, blue, green, clear, volume, is_checked;
		red = msg[1];
		blue = msg[2];
		green = msg[3];
		clear = msg[4];
		volume = msg[5];
		is_checked = msg[6];

		postln(msg)

		postln(red, blue, green, clear, volume, is_checked);

	}, '/entry');

	OSCdef.new(\create, {
		|msg, time, addr, recvPort|
		var name = msg[1];
		var freq = msg[2];

		//avoid overwriting references to synths
		//if I make 'test' and then another 'test', the first UGEN keeps playing (cont.)
		//I just just my reference to the first one

		if(currentEnvironment.at(name.asSymbol).notNil) {
			currentEnvironment.at(name.asSymbol).free;
			currentEnvironment.removeAt(name.asSymbol);
		};
		//this would be the same I think as ~name
		currentEnvironment.put(
			name.asSymbol,
			Synth(\fm, [\freq, freq])
		);
    }, '/synth/create');

	//update frequency of synth with given name
	OSCdef.new(\update, {
		|msg, time, addr, recvPort|
		var name = msg[1];
		var val = msg[2];
		var property = msg[3];
		switch(property.asString,
			"carrier", { currentEnvironment.at(name.asSymbol).set(\freq, val) },
			"carrierRatio", { currentEnvironment.at(name.asSymbol).set(\cRatio, val) },
			"modulatorRatio", { currentEnvironment.at(name.asSymbol).set(\mRatio, val) },
			{ "Unknown parameter".postln }
		);
	}, '/synth/params');

    //remove synth with a given name
    OSCdef.new(\free, {
        |msg, time, addr, recvPort|
        var name = msg[1];
        if(currentEnvironment.at(name.asSymbol).notNil) {
            currentEnvironment.at(name.asSymbol).free;
			currentEnvironment.removeAt(name.asSymbol);
        };
    }, '/synth/free');

	OSCdef.new(\volume, {
		|msg, time, addr, recvPort|
		var value = msg[1];
		~v.volume = value;
	}, '/volume')

});
)