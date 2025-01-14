# mort-garson
Music for Advertising


A non-traditional step sequencer

Run program in a straight line - Hardware/input -> read/map -> send message -> process message/generate sound

![Last we Talked](./docs/design-v1.png)

Lectures: https://www.youtube.com/@elifieldsteel

Flex Sensor Data sheet: https://cdn-shop.adafruit.com/datasheets/SpectraFlex2inch.pdf

OSC Client in C: https://github.com/mhroth/tinyosc
 - This could be relevant/have done some of the hard work for us

Unrelated project that streams SC output over the World Wide Web: https://github.com/khilnani/supercollider.web/tree/master


Hardware - 
 - Raspberry pi 4 8gb (TODO: in this section, we need more granular and specific specs to replicate this if we make more than one)
 - needs parts list/manifest/datasheets
 - SOUND CARD: we can't just rely on this PiShop peripheral, we might need to build our own

Sofware -
 - PI os version (we should get a few more pis and build these totally headlessly with latest bookworm)