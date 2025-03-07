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
		mod = SinOsc.ar((freq * mRatio).lag(2), mul:freq * mRatio);
		car = SinOsc.ar((freq * cRatio).lag(2) + mod) * amp;
        //direct out/reverb send
        Out.ar(0, car);
    }).add;

	OSCdef.new(\entry, {
		|msg, time, addr, recvPort|
		var params = Dictionary.new, i;

		// Skip first element (OSC address)
		i = 1;
		while({i < msg.size}, {
			params.put(msg[i].asSymbol, msg[i+1]);
			i = i + 2;
		});


		if(params[\proximity] > 0 && ~started.not) {
			~started = true;

			currentEnvironment.put(
				\red_fm,
				Synth(\fm, [\freq, params[\red].midicps])
			);
			currentEnvironment.put(
				\blue_fm,
				Synth(\fm, [\freq, params[\blue].midicps])
			);
			currentEnvironment.put(
				\green_fm,
				Synth(\fm, [\freq, params[\green].midicps])
			);

		};

		if(params[\proximity] == 0 && ~started) {
			~started = false;
			s.freeAll;
			//~red_fm.free;
			//~green_fm.free;
			//~blue_fm.free;

		};

		if(~started) {
		// NOW this is where we start the mess
			if(~v.volume != params[\volume]) {
				~v.volume = params[\volume];
			};

			~red_fm.set(\freq, params[\red].midicps);
			~green_fm.set(\freq, params[\green].midicps);
			~blue_fm.set(\freq, params[\blue].midicps);

			/*
			postln(greatest_color.class);
			switch(greatest_color,
				\red, {
					~red_fm.set(\cRatio, clear_single);
				},
				\green, {
					~green_fm.set(\cRatio, clear_single);
				},
				\blue, {
					~blue_fm.set(\cRatio, clear_single);
				}
			);
			*/


		};
	}, '/drone_mode');
});
)