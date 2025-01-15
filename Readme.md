

# ETC Express Control Surface Reverse Engineering

![ETC Express Control Surface](internal-photos/title_image.jpg?raw=true)

## Introduction

The ultimate goal of this work is to develop an interface to use the control surface from a legacy ETC Express 24/48 lighting controller as a modern EOSNomad compatible programming and fader wing. The CPU platform for the this board is not likely to be re-used for this project. This platform was developed in the late 1900s during the height of the Intel RISC based i960's popularity. This platform has been long abandoned, and although some tool-chains do exist, none seem to have been maintained beyond the early 2000s. As well no modern platform emulators seem to exist for the i960 architecture. Due to these challenges I decided to approach reverse engineering the interface port between the control surface and the CPU module, to hopefully implement either an OCS or HID based interface to a PC running EOS.

## Teardown & Analysis

### Internal Layout
Internal images are in the folder [internal-photos](internal-photos/)
### General System Layout
Overall, the console is comprised of two main components, the CPU/IO module, and the control surface. The two are connected by means of a 34 pin (2x17) connector. 
#### Control Surface
In the case of the 24/48 model I have access to, the surface consists of two main sections. These two sections are internally separate circuits, with each communicating with the CPU board independently. 
##### Fader & Bump Keys
On the left is the 48 fader & bump key module, consisting of 48 carbon film slide potentiometers as well as 48 momentary normally open "bump key" switches. Various multiplexers/decoders are used in conjunction with a PIC module to create a 2-wire communications link that is passed through directly to the CPU module (where it terminates at an Altera Flex FPGA) for decoding. With the bottom row of bump keys, there are 24 in-key LEDs, these are managed using an ICM7218BIPI LED control IC.
##### Design & Control keys, Master, and Cross faders
 On the right is the initial focus of this project. The primary control interface consisting of 70 N/O momentary key switches, 35 in-key LEDs, 5 carbon film slide potentiometers, and a touch-pad. These interface with the CPU module using 8 pins forming an 8 bit data bus,  7 pins as inputs to the 3 primary multiplexers/decoders, and 2 pins for control signals to the MAX150BCPP ADC. The ADC samples the state of the 5 fader potentiometers through a CD74HC4051-EP Analog Multiplexer and Demultiplexer. 
 #### CPU Module
 This is the "brains" of the lighting console. This is an old embedded Intel design, employing fairly common chipsets for SuperIO, Floppy, Parallel, Ethernet, and VGA. Alongside the more common stuff, is an Altera Flex FPGA that likely handles the more specific stuff like DMX, ETCNet, MIDI, etc. 
##### Original firmware
This project aims to interface with the control surface, and discard the original CPU/IO module, so this is just listed as a reference in-case someone reads this and want's to port Doom to the express series console's CPU module or something.   
The last version of the firmware released: [Firmware](https://www.etcconnect.com/Support/Consoles/Legacy/Express/Software.aspx)

## Circuit Operation (control surface)
Since the two sections of the surface communicate to the CPU independently the will be treated as separate entities here. 
### Control Section
![Schematic](https://raw.githubusercontent.com/dnhutchins/ETC_Express_Reverse_Eng/refs/heads/main/kicad/ExpressForEOS/ExpressForEOS.svg)
There is no external or internal clock signal in this section, states are read/written real-time. 
#### 8-bit Bus
1. Connection to the CPU module is buffered via U9, the SN74LS245N Tri-State Octal Bus Transceiver.
1. The bus sets U7 and U8, SN74LS374, to select which CD74HC4051-EP analog multiplexer/demultiplexer is enabled 
	* (One mux is used to decode the analog faders, as well as additional muxes for additional faders not installed in the 24/48 I have access to)
1. U13 sets the bus, this appears to be used to decode key presses
1. The bus sets U14 icm7218bipi 8-bit LED display driver, used to drive the in-key leds
1. U15 max150bcpp CMOS High Speed 8 Bit ADC sets the bus with value of the fader being routed via the analog mux
#### Selection Muxes
1. U6 - SN74LS138 ... TODO
1. U11 - SN74LS156... TODO
1. U12 - SN74LS156... TODO
#### ADC Control
1. U15 MAX150... TODO

### Fader Section
TODO...

## 34-pin "Face Panel Bus" Connector

This is the interface between the control surface and the CPU. The pins of this connector are connected internally as follows:

### Pinout

1. GND
2. U9 Pin-12 (B7)
3. U9 Pin-13 (B6)
4. GND
5. U9 Pin-16 (B3)
6. U9 Pin-17 (B2)
7. GND
8. U11 & U12 Pin-3 (B)
9. GND
10. N/C
11. U6 Pin-1 (A)
12. GND
13. U6 Pin-3 (C)
14. FADER-SUB-BOARD Data (PIC micro on fader board)
15. GND
16. U15 Pin-8 (_RD)
17. GND
18. VCC
19. U15 Pin-6 (_WR/RDY)
20. FADER-SUB-BOARD Data (PIC micro on fader board)
21. VCC
22. U6 Pin-4 (G1)
23. U6 Pin-2 (B)
24. VCC
25. N/C
26. U11 & U12 Pins-1,15 (1C,2C)
27. VCC
28. U11 & U12 Pin-13 (A)
29. U9 Pin-18 (B1)
30. VCC
31. U9 Pin-15 (B4)
32. U9 Pin-14 (B5)
33. VCC
34. U9 Pin-11 (B8)

### ICs with direct connection

1. U9 SNx4LS245 Octal Bus Transceivers With 3-State Outputs
	1. [Datasheet](datasheets/sn74ls245.pdf)
	1. Connected Pins (Port Pin->IC Pin):
		1. Pin-2  -> Pin-12 (B7)
		1. Pin-3  -> Pin-13 (B6)
		1. Pin-5  -> Pin-16 (B3)
		1. Pin-6  -> Pin-17 (B2)
		1. Pin-29 -> Pin-18 (B1)
		1. Pin-31 -> Pin-15 (B4)
		1. Pin-32 -> Pin-14 (B5)
		1. Pin-34 -> Pin-11 (B8)
1. U11 SN74LS156 DUAL 2-LINE TO 4-LINE DECODERS/DEMULTIPLEXERS
	1. [Datasheet](datasheets/sn74ls156.pdf)
	1. Connected Pins (Port Pin->IC Pin):
		1. Pin-8 -> Pin-3 (B)
		1. Pin-26 -> Pin-1 (1C), Pin-15 (2C)
		1. Pin-28 -> Pin-13 (A)
1. U12 SN74LS156 DUAL 2-LINE TO 4-LINE DECODERS/DEMULTIPLEXERS
	1. [Datasheet](datasheets/sn74ls156.pdf)
	1. Connected Pins (Port Pin->IC Pin):
		1. Pin-8 -> Pin-3 (B)
		1. Pin-26 -> Pin-1 (1C), Pin-15 (2C)
		1. Pin-28 -> Pin-13 (A)
1. U6 SN74LS138 3-LINE TO 8-LINE DECODERS/DEMULTIPLEXERS
	1. [Datasheet](datasheets/sn74s138a.pdf)
	1. Connected Pins (Port Pin->IC Pin):
		1. Pin-11 -> Pin-1 (A)
		1. Pin-13 -> Pin-3 (C)
		1. Pin-22 -> Pin-4 (G1)
		1. Pin-23 -> Pin-2 (B)
1. U15 MAX150 CMOS High Speed 8 Bit A/D Converter with Reference and Track/Hold Function
	1. [Datasheet](datasheets/MAX150_MX7820-3468900.pdf)
	1. Connected Pins (Port Pin->IC Pin):
		1. Pin-16 -> Pin-8 (_RD)
		1. Pin-19 -> Pin-6 (_WR/RDY)

## Misc. Links

https://github.com/ETCLabs/lighthack/?tab=readme-ov-file

