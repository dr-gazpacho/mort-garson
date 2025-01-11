s.boot;

(
x = {
	PinkNoise.ar * -30.dbamp; //num.dbamp (decibel to amplifier) ampdb also exists
}.play;
)


//SineOsc, Pulse, Saw, LFTri, Impulse (good for low freq), PinkNoise, WhiteNoise, BrownNoise, ClipNoise
//UGens use .ar -> audio rate - generates hearable samples at audio rate (only way for signal to speakers)
//.kr -> control rate - 1 sample per 64 audio samples - low rez .ar
//.ir -> initialization rate - UGen runs at ONE value on initialization and stays there - a const

/*(
y = {
	var mod, sig;
	mod = LFTri.kr(1) * 200;
	sig = SinOsc.ar(200 + mod);
	sig = sig * -12.dbamp;
}.play;
)*/

(
y = {
	var mod, sig, controlMod;
	// below could be done with an LFO
	// controlMod = PinkNoise.kr().range(1, 5); //can skip mul and add and just let it backfill;
	//LF 0 : non interpolated, random discrete values
	//LF 1 : linear interpolated, random discrete values connected by straight lines
	//LF 2 : quadratic interpolated, random discrete values connected by smoother & curved lines
	// {LFX.ar()}.plot(1000) to graph the shape

	//generate five noises/second
	controlMod = LFNoise2.ar(freq: 5).range(1, 10); // keep val from negative, LFTri has range from -1 to 1
	mod = LFTri.kr(controlMod) * 200; //old boy says triange waves dont like negative values sooo
	sig = SinOsc.ar(200 + mod);
	sig = sig * -12.dbamp;
}.play;
)

// x = {SinOsc.ar}.plot;


// think of LFNoise0 like a random number generator
(
z = {
	var mod, sig;
	mod = LFNoise0.ar(freq: 10).range(0, 1000);
	sig = SinOsc.ar(mod);
	sig = sig * -12.dbamp;
}.play;
)

// what about trying a wave that represents computer pulses of 0 to 1
(
a = {
	LFPulse.ar(100)
}.plot(0.05);
)

//use the on/off property to turn on/off 10/second
(
z = {
	var mod, sig;
	mod = LFPulse.kr(10);
	sig = SinOsc.ar(440) * mod;
	sig = sig * -12.dbamp;
}.play;
)

// or give it a range (look at dogs on what range does) and control tone
(
z = {
	var mod, sig;
	mod = LFPulse.kr(3).range(440, 880);
	sig = SinOsc.ar(mod);
	sig = sig * -12.dbamp;
}.play;
)


//STEREO
// SC gets an array of signals in an array, it assigns the lowest indexed entry in the array to the lowest hardware address??
(
z = {
	var sig;
	sig = [SinOsc.ar(300), SinOsc.ar(305)];
	sig = sig * -12.dbamp;
}.play;
)
//in multichannel expansion, theres an explanation for how this works, where if you pass an array in, SC creates ar.length Ugens and distributes the values
(
z = {
	var sig;
	sig = SinOsc.ar([300, 301]);
	sig = sig * -12.dbamp;
}.play;
)
//you can also use this for dbamp
(
z = {
	var sig;
	sig = SinOsc.ar([300, 401]);
	sig = sig * [-10, -20].dbamp;
}.play;
)


//what if we want to make a rudimentary mix?
(
x = {
	var sig;
	//create a decimal array of 50 elements, clustering them near the bottom of the freq band
	sig = SinOsc.ar(freq: { exprand(100, 1000) } ! 50);
	//sum the signals - this basically will sum the samples at a given point in time -
	//DIF FROM SPLAY - this will put the SAME signal in both channels
	sig = sig.sum;
	sig = sig * -40.dbamp;
	//split the signal into two channels/stereo sound
	sig = sig ! 2
}.play;
)
//or with splay
(
x = {
	var sig;
	//create a decimal array of 50 elements, clustering them near the bottom of the freq band
	//exprand(100, 1000).round(30) rounds to nearest multiple, gives harmonic series
	sig = SinOsc.ar(freq: { exprand(100, 1000) } ! 50);
	//some sort of panning algorithm?
	//Splay is a Ugen (note the ar) takes an array of signals, then outputs a stero signal thats a mix of all input signals spatially distributed across a stereophonic field e.g. sig[0] hard left and sig[sig.length -1] is hard right; it also compensates based on size of array
	//Will make true stereo - put different signals in each channel
	sig = Splay.ar(inArray: sig);
	sig = sig * -40.dbamp;
	//split the signal into two channels/stereo sound
	sig = sig ! 2
}.play;
)

// WEEK FOUR (chapter 2)
//you can use the set() method to alter a synth as it plays
(
x = {
	arg width = 0.9;
	//if arg were freq = [300, 301] it won't work, must be #[300, 301] (array literal)
	//some reason like, channels in a running synth def MUST be static
	var signal;
	signal = VarSaw.ar(freq: [300, 301], width: width);
	signal = signal * -20.dbamp;
	//super collider will try and play the last value in this expression
	//0 -> would effectively silence the sound
}.play
)

//pass symbol and value you want that set at
x.set(\width, 0.1)


// now  gotcha
(
x = {
	arg width = 0.9;
	//WIDTH here, though seemingly an integer, will become a "Control" when this is played
	//it we just evaluate the function to get a return value, it will be an integer
	//however, once the sound is playing, this argument becomes something more complex
	//be wary of using conditionals in a function to manipulate arguments
	var signal;
	signal = VarSaw.ar(freq: [300, 301], width: width);
	signal = signal * -20.dbamp;
}.play
)

//how can we interpolate between values when we use arguments?
// use the .lag(x) method, for one
// https://www.youtube.com/watch?v=Hw0MXqKMpGA at 22:00 for varlag and curvature
(
x = {
	|freq = 330, wdt = 0.5, amp = 0.1|
	var sig;
	sig = VarSaw.ar(freq: freq.lag(2) + [0, 1], width: wdt);
	sig = sig * amp;
}.play
)

x.set(\freq, 500);
x.set(\freq, 50);

x.release(1);


//ENVELOPES

(
x = {
	var sig, env;
	//make envelope with UGen
	//mostly use KR, unless you need high precision for short sounds like percussion
	env = EnvGen.kr(
		Env.new(
			levels: [0, 1, 0],
			times: [0.5, 2],
			curve: [-4, -1]
		),
		//done action (Done classs) used to clean up process https://www.youtube.com/watch?v=Hw0MXqKMpGA at 37:00
		doneAction: Done.freeSelf
	).poll;
	//poll is like post for signals,
	sig = VarSaw.ar(freq: [300, 301], width: 0.5);
	sig = sig * env;
	sig = sig * -20.dbamp;
}.play
)

//could also make an envelope like this
/*e = Env.new(
	levels: [0, 1, 0],
	times: [0.5, 2],
	curve: [-4, -1]
);

e.plot;*/


//let's retrigger
(
x = {
	var sig, env;
	//make envelope with UGen
	//mostly use KR, unless you need high precision for short sounds like percussion
	env = Env.new(
			levels: [0, 1, 0],
			times: [0.001, 0.08],
			curve: [-4, -1]
	).kr(0, \trig.kr(1));
	//poll is like post for signals,
	sig = VarSaw.ar(freq: [300, 301], width: 0.5);
	sig = sig * env;
	sig = sig * -20.dbamp;
}.play(fadeTime: 0) //fadeTime overrides default minute fade in
)

x.set(\trig, 1);

