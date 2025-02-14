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

	SynthDef(\basicSine, {
		arg freq = 440, amp = 0.5, mod = 0;
		var sig;
		sig = SinOsc.ar(freq + mod) * amp;
		Out.ar(0, [sig, sig]);
	}).add;

	SynthDef(\lfo, {
		arg freq = 0, amp = 0.5;
		var sig;
		sig = SinOsc.kr(freq) * amp;
		Out.kr(0, [sig, sig]);
	}).add;


	OSCdef.new(\entry, {
		|msg, time, addr, recvPort|
		var red, blue, green, clear, volume, is_checked, clear_single, greatest_color, red_lfo, green_lfo, blue_lfo;
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
		red_lfo = msg[9];
		green_lfo = msg[10];
		blue_lfo = msg[11];



		if(is_checked && ~started.not) {
			~started = true;

			currentEnvironment.put(
				\red_sine,
				Synth(\basicSine, [\freq, red.midicps, \mod, Synth(\lfo, [\freq, clear_single])])
			);
			currentEnvironment.put(
				\green_sine,
				Synth(\basicSine, [\freq, green.midicps, \mod, Synth(\lfo, [\freq, clear_single])])

			);
			currentEnvironment.put(
				\blue_sine,
				Synth(\basicSine, [\freq, blue.midicps, \mod, Synth(\lfo, [\freq, clear_single])])
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

			~red_sine.set(\freq, red.midicps, \mod, clear_single);
			~green_sine.set(\freq, green.midicps, \mod, clear_single);
			~blue_sine.set(\freq, blue.midicps, \mod, clear_single);

		};
	}, '/drone_mode');
});
)