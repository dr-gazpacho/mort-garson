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
        arg freq=500, mRatio=1, cRatio=1, index=1, tremeloFreq=0.1, tremeloPhase=0;
        var car, mod, env, tremolo, withTremolo;
		tremolo = (SinOsc.kr(freq: tremeloFreq, phase: tremeloPhase) * 0.5) + 0.5;
		//multiplying by .5 reduces the amplitude to -.5 to .5
		//adding .5 to make it oscillate from 0 to 1, off to on
		//phase should take an argument in x*pi where pi shifts cycle by half, starting on quiet instead of loud
		mod = SinOsc.ar((freq * mRatio).lag(2), mul:freq * mRatio);
		car = SinOsc.ar((freq * cRatio).lag(2) + mod);
		withTremolo = car * tremolo;

        Out.ar(0, withTremolo ! 2);
    }).add;

	OSCdef.new(\entry, {
		|msg, time, addr, recvPort|
		var params = Dictionary.new, i;

		// Skip first element (OSC address)
		// all values in the osc_message in the python app are getting chucked into this dictionary "params"
		// you can reference things using the property name as a symbol
		i = 1;
		while({i < msg.size}, {
			params.put(msg[i].asSymbol, msg[i+1]);
			i = i + 2;
		});


		if(params[\proximity] > 0 && ~started.not) {
			~started = true;

			currentEnvironment.put(
				\red_fm,
				Synth(\fm, [
					\freq, params[\red].midicps,
					\tremeloFreq, params[\red_tremolo_frequency],
					\tremeloPhase, params[\red_phase_offset]
				])
			);
			currentEnvironment.put(
				\green_fm,
				Synth(\fm, [
					\freq, params[\green].midicps,
					\tremeloFreq, params[\green_tremolo_frequency],
					\tremeloPhase, params[\green_phase_offset]
				])
			);
			currentEnvironment.put(
				\blue_fm,
				Synth(\fm, [
					\freq, params[\blue].midicps,
					\tremeloFreq, params[\blue_tremolo_frequency],
					\tremeloPhase, params[\blue_phase_offset]
				])
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

			~red_fm.set(
				\freq, params[\red].midicps,
				\tremeloFreq, params[\red_tremolo_frequency],
				\tremeloPhase, params[\red_phase_offset]
			);
			~green_fm.set(
				\freq, params[\green].midicps,
				\tremeloFreq, params[\green_tremolo_frequency],
				\tremeloPhase, params[\green_phase_offset]
			);
			~blue_fm.set(
				\freq, params[\blue].midicps,
				\tremeloFreq, params[\blue_tremolo_frequency],
				\tremeloPhase, params[\blue_phase_offset]
			);

			/*
			postln(greatest_color.class);
			switch(greatest_color,
				\red, {
					~red_fm.set(\cRatio, white_single);
				},
				\green, {
					~green_fm.set(\cRatio, white_single);
				},
				\blue, {
					~blue_fm.set(\cRatio, white_single);
				}
			);
			*/


		};
	}, '/drone_mode');
});
)