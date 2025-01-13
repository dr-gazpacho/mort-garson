# Big WIP
Ignore the `osc_repl.c` this is LLM garbage but leaving it here to look back on in fondness when we implement something that isn't garbage and laugh at both my stupidity and that of the robots. [THIS](https://github.com/mhroth/tinyosc) could be valuable, need to actually read it and write something like it to send messages.

The goal I have with this little section is to encapsulate some of the work. Basically going to try and build this `.scd` file up to behave like a simplified version of how we want the real project to work, then use the python app in interactive mode to send messages via the command line and test the SC implementations without having to build the whole hardware interface. I think this `PBind` method can work for our sequencer, but still pretty green on how patterns work in SC


    (
    ~globalOutput = Pbind(
	    \instrument, \nameOfInstrument,
	    \dur, Pseq(~sequence, ~loops)
    ).play;
    )
