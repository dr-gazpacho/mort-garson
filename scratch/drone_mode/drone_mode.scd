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
		var red, blue, green, clear, volume, is_checked, clear_single, greatest_color;
		//these are the raw values
		red = msg[1];
		blue = msg[2];
		green = msg[3];
		clear = msg[4];
		volume = msg[5];
		is_checked = msg[6];
		//and the computed values
		clear_single = msg[7];
		greatest_color = msg[8];


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
			s.freeAll;
			//~red_fm.free;
			//~green_fm.free;
			//~blue_fm.free;

		};

		if(~started) {
		// NOW this is where we start the mess
			if(~v.volume != volume) {
				~v.volume = volume;
			};

			~red_fm.set(\freq, red.midicps, \mRatio, clear_single);
			~green_fm.set(\freq, green.midicps, \mRatio, clear_single);
			~blue_fm.set(\freq, blue.midicps, \mRatio, clear_single);

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


		};
	}, '/drone_mode');
});
)