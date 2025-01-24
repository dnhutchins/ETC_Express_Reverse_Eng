

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
NOTE: This schematic is the product of tracing connections on this circuit, it is only meant to serve as a reference for signaling, it does not include descrete components such as bypass caps, pull up/down resistors, etc.

![Schematic](https://raw.githubusercontent.com/dnhutchins/ETC_Express_Reverse_Eng/refs/heads/main/kicad/ExpressForEOS/ExpressForEOS.svg)
There is no external or internal clock signal in this section, states are read/written real-time, and individual ICs are clocked independently using (mostly) seperate signals.
#### Integrated Circuits
1. U1-U4 = 74HC4051 (Analog Multiplexer and Demultiplexers) [datasheet](datasheets/cd74hc4051-ep.pdf)
1. U5 = CD4066 (Quad Bilateral Switch) [datasheet](datasheets/cd4066b.pdf)
1. U6 = 74LS138 (3-LINE TO 8-LINE DECODERS/DEMULTIPLEXER) [datasheet](datasheets/sn74s138a.pdf)
1. U7-U8 = 74LS374 (OCTAL EDGE-TRIGGERED FLIP-FLOP) [datasheet](datasheets/sn54ls373-sp.pdf)
1. U9 = 74LS245 (Octal Bus Transceiver With 3-State Outputs) [datasheet](datasheets/sn74ls245.pdf)
1. U10 = 74LS08 (Quad 2-Input AND Gate) [datasheet](datasheets/74F08-196092.pdf)
1. U11-U12 = 74LS156 (DUAL 2-LINE TO 4-LINE DECODERS/DEMULTIPLEXER) [datasheet](datasheets/sn74ls156.pdf)
1. U13 = 74LS373 (OCTAL D-TYPE TRANSPARENT LATCH) [datasheet](datasheets/sn54ls373-sp.pdf)
1. U14 = ICM7218 (8 Digit LED Display Driver) [datasheet](datasheets/ICM7218-ICM7228.pdf)
1. U15 = MAX150 (CMOS High Speed 8 Bit A/D Converter with Reference and Track/Hold) [datasheet](datasheets/MAX150_MX7820-3468900.pdf)
1. U16 = LM358 (Dual Operational Amplifier) [datasheet](datasheets/lm358.pdf)
#### 8-bit Bus
1. Connection to the CPU module is buffered via U9.
1. Pin 19 from the interface connector selects the direction of U9 as well as RD/WR on U15
1. The bus sets U7 and U8, SN74LS374, to select which CD74HC4051-EP analog multiplexer/demultiplexer is enabled 
	* (One mux/demux is used to decode the analog faders, as well as additional mux/demuxes for additional faders not installed in the 24/48 I have access to)
1. U13 sets the bus, this appears to be used to decode key presses
1. The bus sets U14 used to drive the in-key leds
1. U15 sets the bus with value of the fader being routed via the analog mux/demux

#### Digital Muxes (Addressing and Keyboard scanning)
1. U6 - SN74LS138 (3-LINE TO 8-LINE DECODERS/DEMULTIPLEXER)
	* This demux is used to signal Write on U14, Cp on U7 and U8, CS on U15, and A2,B1 on either U11 or U12
	* Pins 11, 23, and 13 from the interface connector control the 3 address inputs
	* Pin 22 from the interface connector controls enable for U6 as well as U9
	* When either U11 or U12 is selected, U13 is activated via one of U10s AND gates, to latch key presses to the bus.
1. U11 - SN74LS156 (DUAL 2-LINE TO 4-LINE DECODERS/DEMULTIPLEXER)
	* Selects one of 8 keyboard "rows"
	* Pins 8, 26, and 28 from the interface connector control the 3 address inputs
	* Chip enable is from U6/0
1. U12 - SN74LS156 (DUAL 2-LINE TO 4-LINE DECODERS/DEMULTIPLEXER)
	* Selects one of 8 keyboard "rows" (4 of which route to the extrenal connector for a larger board configuration)
	* Pins 8, 26, and 28 from the interface connector control the 3 address inputs
	* Chip enable is from U6/1
#### Control Latches (Analog mux selection, addressing, and TP switching)
1. U7 - 74LS374 (OCTAL EDGE-TRIGGERED FLIP-FLOP) **Control register**
	* Operates SW1-4 of U5 CD4066 Quad Bilateral Switch
	* Address and selection signals to U4 Analog Multiplexer (Responsible for on-board faders and touch pad)
1. U8 - 74LS374 (OCTAL EDGE-TRIGGERED FLIP-FLOP) **Control register**
	* Address and selection signals to U4 Analog Multiplexer (Responsible for off-board faders, unused "external" connector
#### Keyboard "Column" Latches
1. U13 - 74LS373 (OCTAL D-TYPE TRANSPARENT LATCH)
	* U13 enables output to the bus, of the 8 columns for the row selected by U11/U12
	* This is enabled in the unlatched "following" state whenever either U11/U12 is selected by U6
	* LE is tied to VCC, so there is no actual latching, just switching the keyboard columns onto the bus.
#### Analog Muxes (Fader Section)
1. U1-U4 - 74HC4051 (Analog Multiplexer and Demultiplexers)
	* Faders are sampled using a single ADC, the analog muxes U1, U2, U3 and U4 are used to route one of up to 32 faders to the ADC.
	* U1, U2, and U3 all route to the external (unused on my board) connector.
	* U4 is connected to the Master, A, B, C, and D faders, as well as the touchpad.
	* U5 (quad analog switch) plays a role in routing the touch pad, where 2 of the switches short short the signal sides, including either pin 2 or 4 of U4 to ground, while the other switch on/off VCC (through a pull up resistor) to the other sides of the touch pad.
	* The output of the mux is connected to U15 through U16, to be sampled.
#### ADC
1. U15 - MAX150
	* Pin 16 from the interface connector controls the RD signal to the ADC
	* CS is driven from U6
	* Data is put directly on the bus
	* WR/WR follows the control from P19 along with the the buffer U9
#### LED Driver
1. U14 - ICM7218 (8 Digit LED Display Driver)
	* Pin 28 from the interface connector controls the MODE signal
	* U6/3 controls the WRITE signal
	* Mode is raised to send control word, then lowered to pulse in each of the 8 banks of 8 leds


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

## Misc. Links

https://github.com/ETCLabs/lighthack/?tab=readme-ov-file

