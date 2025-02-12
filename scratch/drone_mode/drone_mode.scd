(
//init/cleanup
s.reboot;
s.boot;
s.newBusAllocators;
s.freeAll;
OSCdef.freeAll;
~v = s.volume;
~started = false;
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

		if(is_checked && ~started.not) {
			~started = true;

			currentEnvironment.put(
				\red_fm,
				Synth(\fm, [\freq, red.midicps])
			);
			currentEnvironment.put(
				\blue_fm,
				Synth(\fm, [\freq, blue.midicps])
			);
			currentEnvironment.put(
				\green_fm,
				Synth(\fm, [\freq, green.midicps])
			);

		};

		if(is_checked.not && ~started) {
			~started = false;

			currentEnvironment.at(\red_fm).free;
			currentEnvironment.at(\green_fm).free;
			currentEnvironment.at(\blue_fm).free;

		};

		if(~started) {
		// NOW this is where we start the mess
			if(~v.volume != volume) {
				~v.volume = volume;
			};

			currentEnvironment.at(\red_fm).set(\freq, red.midicps);
			currentEnvironment.at(\green_fm).set(\freq, green.midicps);
			currentEnvironment.at(\blue_fm).set(\freq, blue.midicps);

		};
	}, '/entry');

	//update frequency of synth with given name
/*	OSCdef.new(\update, {
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
	}, '/synth/params');*/


});
)