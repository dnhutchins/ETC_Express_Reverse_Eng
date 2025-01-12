
# ETC Express Control Surface Reverse Engineering

![ETC Express Control Surface](internal-photos/title_image.jpg?raw=true)

## Introduction

The ultimate goal of this work is to develop an interface to use the control surface from a legacy ETC Express 24/48 lighting controller as a modern EOSNomad compatible programming and fader wing. The CPU platform for the this board is not likely to be re-used for this project. This platform was developed in the late 1900s during the height of the Intel RISC based i960's popularity. This platform has been long abandoned, and although some tool-chains do exist, none seem to have been maintained beyond the early 2000s. As well no modern platform emulators seem to exist for the i960 architecture. Due to these challenges I decided to approach reverse engineering the interface port between the control surface and the CPU module, to hopefully implement either an OCS or HID based interface to a PC running EOS.

## Teardown & Analysis

Internal images are in the folder [internal-photos](internal-photos/)
The last version of the firmware released: [Firmware](https://www.etcconnect.com/Support/Consoles/Legacy/Express/Software.aspx)

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

