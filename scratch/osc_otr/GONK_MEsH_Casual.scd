//INITILIZATION
s.boot;


//  THIS DOESN'T WORK RIGHT NOW
// 	var desiredBPM = 1;  // INPUT BPM
//	var quarterNoteDur = 60 / desiredBPM;  // Duration of one quarter note in seconds
//	TempoClock.default.tempo = desiredBPM;  // Set TempoClock's tempo



(
s.waitForBoot({
    SynthDef(\custom_synth, {
        |freq=440, amp=0.2,

		//PASS IN VARIABLES FROM FLEX KEYS FOR ADSR
		atk=0.5,
		dec=0.8,
		sus=0.33,
		rel=0.7,

		//NOTE LENGTH
		gate=1,  // 1 = 100% NOTE LENGTH

		//INPUT WAVE SELECTION
		waveform=3,  //0sin, 1saw, 2sqr, 3fm

		//PASS IN VARIABLES FROM 9960 FOR MODULATION
		cutoff=800,
		resonance=0.9,
		accent=1,
		overdrive= 0.4,

		//GLOBAL LFO **PASS IN VARIABLES FOR 'ALGORITHM' MODULATION
		lfo_depth=0.5,

		// AUDIO OUTPUT CHANNEL 0= generic stereo output.
		out=0| //**CHANGE FOR MORE COMPLEX AUDIO IMAGING (OPTIONAL)

        // ADSR ENV
        var env = EnvGen.kr(Env.adsr(atk, dec, sus, rel), gate, doneAction: 2);

        // LFO TO MODULATE PHASE DISTORTION
        var lfo = SinOsc.kr(0.1).range(0, lfo_depth); // LFO at 0.1 Hz, controlling phase distortion

		// LFO TO MODULATE CUTOFF
        var modulatedCutoff = cutoff + (lfo * cutoff);

        // OSCILLATOR INDEX
        var osc = Select.ar(waveform, [
            SinOsc.ar(freq + lfo),        // 0: Sine wave with phase modulation
            Saw.ar(freq + lfo),           // 1: Saw wave with phase modulation
            Pulse.ar(freq + lfo, 0.5),    // 2: Square wave with phase modulation
            SinOsc.ar(freq * 2 + lfo, 0, SinOsc.ar(freq * 0.5) * 0.5) // 3: Simple FM with phase modulation
        ]);

        // Low-pass filter with cutoff and resonance
        var filteredSig = RLPF.ar(osc, cutoff, resonance);

        // Overdrive (distortion) effect using Clip
        var distortedSig = Clip.ar(filteredSig * accent, -0.9, 0.9);

        // Final signal
        var sig = distortedSig * env * amp;

        // OUTUT
        Out.ar(out, sig);
    }).add;

    s.sync;

    // LEAD MELODY EXAMPLE
    Pbind(
        \instrument, \custom_synth,
        \dur, 1/8, //EIGTH NOTES
        \midinote, Pseq([63, 56, 61, 63, 58, 61, 61, 58, 61, 58, 61, 63, 58, 61, 56, 58, 58, 56, 56, 58, 54, 56, 49, 54, 54, 49, 51, 54, 56, 51, 56, 66], 4),
		// (32x4 = 128 step)
        \amp, 0.2,
        \waveform, 0,
        \cutoff, Prand([800, 1000, 1200, 1500], inf),
        \resonance, Pseq([0.3, 0.5, 0.7, 1.0], inf),
        \accent, Pseq([1, 1.5, 2, 1], inf),
        \overdrive, Prand([0, 0.1, 0.2, 0.3], inf),
        \lfo_depth, 0.8 // DEPTH OF PHASE DISTORTION
    ).play;


	// LEAD BASS EXAMPLE
    Pbind(
        \instrument, \custom_synth,
        \dur, 1/4, //QUARTER NOTES
		\midinote, Pseq([51, 51, 51, 51, 49, 49, 49, 49, 46, 46, 46, 46, 42, 42, 44, 49], 2), // (16x2 = 32 step)
        \amp, 0.2,
		\waveform, 0,
        \cutoff, Pseq([80, 100, 300, 200], inf),
        \resonance, Prand([0.1, 0.5, 0.7, 1.0], inf),
        \accent, Pseq([1, 3, 5, 7], inf),
        \overdrive, Prand([0, 0.9, 0.7, 0.3], inf),
        \lfo_depth, 0.1 // DEPTH OF PHASE DISTORTION
    ).play;

});
).play;