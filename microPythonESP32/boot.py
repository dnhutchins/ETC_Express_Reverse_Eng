from machine import Pin
from time import sleep_ms
from neopixel import NeoPixel
import random

# Setup the "neoPixel" RGB-LED on the ESP-32-S3 dev board 
pinl = Pin(48, Pin.OUT) # Might be different on other boards
np = NeoPixel(pinl, 1)
# initialize the pixel
np[0] = (5,5,5)
np.write()

# define which pins are used for connecting to the 8-bit bus (Data0....Data7)
d_bus_pins = [4,5,6,7,15,16,17,18]
d_bus = []

# define pins for the control pin bus (not really an address bus)
a_bus = {"P11": Pin(46, Pin.OUT),
         "P23": Pin(9, Pin.OUT),
         "P13": Pin(10, Pin.OUT),
         "P22": Pin(3, Pin.OUT),
         "P19": Pin(8, Pin.OUT),
         "P16": Pin(11, Pin.OUT),
         "P8": Pin(14, Pin.OUT),
         "P28": Pin(13, Pin.OUT),
         "P26": Pin(12, Pin.OUT)
         }

# Just to create a sane state, raise all pins, and then pull them down
for pin in a_bus:
    a_bus[pin].on()
sleep_ms(500)
for pin in a_bus:
    a_bus[pin].off()
sleep_ms(500)

# Initalize the bus
for i in range(0,8):
    d_bus.append(Pin(d_bus_pins[i], Pin.IN))
a_bus['P19'].on()

# Sets the bus to outout (ESP32 -> Control Surface)
def set_data_out():
    for i in range(0,8):
        d_bus[i] = Pin(d_bus_pins[i], Pin.OUT, value=0)
    a_bus['P19'].off()

# Puts data on the bus, and enables the I/O buffer
def put_data(data): # Array of booleans
    for i in range(0,8):
        if data[i]:
            d_bus[i].on()
        else:
            d_bus[i].off()
    a_bus['P22'].off()

# Sets the bus to input (Control Surface -> ESP32)
def set_data_in():
    a_bus['P22'].on()
    for i in range(0,8):
        d_bus[i] = Pin(d_bus_pins[i], Pin.IN)
    a_bus['P19'].on()

# Pulse U7 to latch data
def pulse_U7():
    a_bus['P22'].on()
    a_bus['P11'].on()
    a_bus['P23'].off()
    a_bus['P13'].on()
    a_bus['P22'].off()

# Pulse the write for the LED Driver
def pulse_LEDS():
    a_bus['P22'].on()
    a_bus['P11'].on()
    a_bus['P23'].on()
    a_bus['P13'].off()
    a_bus['P22'].off()

# Select the ADC
def select_ADC():
    a_bus['P22'].on()
    a_bus['P11'].off()
    a_bus['P23'].off()
    a_bus['P13'].on()
    a_bus['P22'].off()

# Read data from the bus and return the value as an int
def read_data():
    read = 0
    for i in range(7, -1, -1):
        read = (read << 1) | d_bus[i].value()
    return int(read)

# Gets the value of a fader
def fetch_fader(index):
    set_data_out()
    if index == 0:
        put_data([True,False,False,True,False,False,False,True]) # Route Master through mux to ADC
    elif index == 1:
        put_data([False,True,False,True,False,False,False,True]) # Route A through mux to ADC
    elif index == 2:
        put_data([True,True,False,True,False,False,False,True]) # Route B through mux to ADC
    elif index == 3:
        put_data([False,False,True,True,False,False,False,True]) # Route C through mux to ADC
    elif index == 4:
        put_data([False,False,False,True,False,False,False,True]) # Route D through mux to ADC
    pulse_U7() # Lock the mux into the control register
    set_data_in()
    
    select_ADC()

    a_bus['P16'].off()
    data_value = read_data()
    a_bus['P16'].on()

    return data_value

def set_lights_on():
    for bank in leds.keys():
        leds[bank] = [True, True, True, True, True, True, True, True]
    
def set_lights_off():
    for bank in leds.keys():
        leds[bank] = [False, False, False, False, False, False, False, False]

def set_lights_random():
    leds[1]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[2]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[3]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[4]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[5]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[6]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[7]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]
    leds[8]=[bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1)),bool(random.getrandbits(1))]


leds = {1: [False, False, False, False, False, False, False, False],
        2: [False, False, False, False, False, False, False, False],
        3: [False, False, False, False, False, False, False, False],
        4: [False, False, False, False, False, False, False, False],
        5: [False, False, False, False, False, False, False, False],
        6: [False, False, False, False, False, False, False, False],
        7: [False, False, False, False, False, False, False, False],
        8: [False, False, False, False, False, False, False, False]
    }

# Send control word and data to the LED driver, note that bit 8 needs to be flipped as it is inverted in the driver (used as "." in displays)
def set_lights():
    a_bus['P28'].off()
    set_data_out()
    put_data([False,False,False,False,True,True,True,True])
    a_bus['P28'].on()
    pulse_LEDS()
    a_bus['P28'].off()
    for bank in leds.keys():
        to_bus = [leds[bank][0], leds[bank][1], leds[bank][2], leds[bank][3], leds[bank][4], leds[bank][5], leds[bank][6],not leds[bank][7]]
        put_data(to_bus)
        pulse_LEDS()

# Mappings used to scan keys (demux addresses), associate them with their LEDs (led driver addresses), and record their up/down status 
keys = {1: {'mux': 0, 'bits': [False, False, False], 'keys': ["M1","M2","M3","M*","Left","Down","Right","Up"], 'leds': [[3,4],[3,2],[3,3],[3,8],None,None,None,None], 'status': [False, False, False, False, False, False, False, False]},
        2: {'mux': 0, 'bits': [True, False, False], 'keys': ["S1","S2","S3","S4","S5","S6","S7","S8"], 'leds': [None,None,None,None,None,None,None,None], 'status': [False, False, False, False, False, False, False, False]},
        3: {'mux': 0, 'bits': [False, True, False], 'keys': ["Clear_CD","Page","Cue","7","8","9","Chan","Dim"], 'leds': [[4,4],None,[4,2],None,None,None,[4,3],[4,8]], 'status': [False, False, False, False, False, False, False, False]},
        4: {'mux': 0, 'bits': [True, True, False], 'keys': ["Rate_CD","Type","Sub","4","5","6","Thru","At"], 'leds': [[5,4],None,[5,2],None,None,None,[5,3],[5,8]], 'status': [False, False, False, False, False, False, False, False]},
        5: {'mux': 0, 'bits': [False, False, True], 'keys': ["Back_CD","Link","Group","1","2","3","And","Full"], 'leds': [[6,4],None,[6,2],None,None,None,[6,3],None], 'status': [False, False, False, False, False, False, False, False]},
        6: {'mux': 0, 'bits': [True, False, True], 'keys': ["GO_CD","Wait","Time","-","0","+","Except","Level"], 'leds': [[7,5],None,None,None,None,None,[6,8],None], 'status': [False, False, False, False, False, False, False, False]},
        7: {'mux': 0, 'bits': [False, True, True], 'keys': ["Hold_CD","Track","Record","Clear",".","Enter","Rel","FocusPoint"], 'leds': [[7,1],[7,4],[7,2],None,None,None,[7,3],[7,8]], 'status': [False, False, False, False, False, False, False, False]},
        8: {'mux': 0, 'bits': [True, True, True], 'keys': ["Setup","Patch","Blind","Stage","Hold_AB","GO_AB","BlackOut","UNK"], 'leds': [[3,1],[3,5],[3,6],[3,7],[7,6],[7,7],[5,7],None], 'status': [False, False, False, False, False, False, False, False]},
        9: {'mux': 1, 'bits': [False, False, False], 'keys': ["EnterMacro","Help","Learn","About","Back_AB","Rate_AB","Clear_AB","UNK"], 'leds': [[4,1],[4,5],[4,6],[4,7],[5,1],[5,5],[5,6],None], 'status': [False, False, False, False, False, False, False, False]}
        }

def flip_led(bank, key):
    led = keys[bank]['leds'][key]
    if led:
        leds[led[0]][led[1]-1] = not leds[led[0]][led[1]-1]

# scan the keyboard
def get_key(bank):
    set_data_in()
    # Use data in the keys dict to set the demux address
    if keys[bank]['bits'][0]:
        a_bus['P28'].on()
    else:
        a_bus['P28'].off()
    if keys[bank]['bits'][1]:
        a_bus['P8'].on()
    else:
        a_bus['P8'].off()
    if keys[bank]['bits'][2]:
        a_bus['P26'].on()
    else:
        a_bus['P26'].off()
    # Use data in the keys dict to choose which demux 
    if keys[bank]['mux'] == 0:
        a_bus['P11'].off()
    else:
        a_bus['P11'].on()
    a_bus['P23'].off()
    a_bus['P13'].off()
    a_bus['P22'].off()
    
    # Read the data, and decode the key press using the tables in the keys dict
    data = int(read_data())
    if not data & 0b10000000:
        if not keys[bank]['status'][0]:
            keys[bank]['status'][0] = True
            print(keys[bank]['keys'][0] + " Down")
    else:
        if keys[bank]['status'][0]:
            keys[bank]['status'][0] = False
            print(keys[bank]['keys'][0] + " Up")
            key_up(keys[bank]['keys'][0],bank,0)
    if not data & 0b01000000:
        if not keys[bank]['status'][1]:
            keys[bank]['status'][1] = True
            print(keys[bank]['keys'][1] + " Down")
    else:
        if keys[bank]['status'][1]:
            keys[bank]['status'][1] = False
            print(keys[bank]['keys'][1] + " Up")
            key_up(keys[bank]['keys'][1],bank,1)
    if not data & 0b00100000:
        if not keys[bank]['status'][2]:
            keys[bank]['status'][2] = True
            print(keys[bank]['keys'][2] + " Down")
    else:
        if keys[bank]['status'][2]:
            keys[bank]['status'][2] = False
            print(keys[bank]['keys'][2] + " Up")
            key_up(keys[bank]['keys'][2],bank,2)
    if not data & 0b00010000:
        if not keys[bank]['status'][3]:
            keys[bank]['status'][3] = True
            print(keys[bank]['keys'][3] + " Down")
    else:
        if keys[bank]['status'][3]:
            keys[bank]['status'][3] = False
            print(keys[bank]['keys'][3] + " Up")
            key_up(keys[bank]['keys'][3],bank,3)
    if not data & 0b00001000:
        if not keys[bank]['status'][4]:
            keys[bank]['status'][4] = True
            print(keys[bank]['keys'][4] + " Down")
    else:
        if keys[bank]['status'][4]:
            keys[bank]['status'][4] = False
            print(keys[bank]['keys'][4] + " Up")
            key_up(keys[bank]['keys'][4],bank,4)
    if not data & 0b00000100:
        if not keys[bank]['status'][5]:
            keys[bank]['status'][5] = True
            print(keys[bank]['keys'][5] + " Down")
    else:
        if keys[bank]['status'][5]:
            keys[bank]['status'][5] = False
            print(keys[bank]['keys'][5] + " Up")
            key_up(keys[bank]['keys'][5],bank,5)
    if not data & 0b00000010:
        if not keys[bank]['status'][6]:
            keys[bank]['status'][6] = True
            print(keys[bank]['keys'][6] + " Down")
    else:
        if keys[bank]['status'][6]:
            keys[bank]['status'][6] = False
            print(keys[bank]['keys'][6] + " Up")
            key_up(keys[bank]['keys'][6],bank,6)
    if not data & 0b00000001:
        if not keys[bank]['status'][7]:
            keys[bank]['status'][7] = True
            print(keys[bank]['keys'][7] + " Down")
    else:
        if keys[bank]['status'][7]:
            keys[bank]['status'][7] = False
            print(keys[bank]['keys'][7] + " Up")
            key_up(keys[bank]['keys'][7],bank,7)

cmd_seq = 0
tbank = 1
tled = 1

# take actions on key up (mostly just stuff to test with)
def key_up(key, bank, keynum):
    flip_led(bank, keynum)
    global cmd_seq, tbank, tled
    if key == "Type":
        set_lights_on()
    if key == "Link":
        set_lights_off()
    if key == "Wait":
        set_lights_random()
        
    if cmd_seq == 0:
        if key in ['1','2','3','4','5','6','7','8']:
            tbank = int(key)
            print("Target Bank: " + key)
            cmd_seq = 1
    elif cmd_seq == 1:
        if key in ['1','2','3','4','5','6','7','8']:
            tled = int(key)
            print("Target LED: " + key)
            cmd_seq = 2
    elif cmd_seq == 2:
        if key in ['Clear', 'Enter']:
            if key == 'Clear':
                leds[tbank][tled-1] = False
                cmd_seq = 0
            elif key == 'Enter':
                leds[tbank][tled-1] = True
                cmd_seq = 0
   
cnt = 0
for i in range(0,900000):
    for bank in keys.keys():
        get_key(bank)
    fetch_fader(4)
    fd_m = fetch_fader(0)
    fd_a = fetch_fader(1)
    fd_b = fetch_fader(2)
    fd_c = fetch_fader(3)
    fd_d = fetch_fader(4)
    np[0] = (fd_m, fd_a, fd_b)
    np.write()
    cnt = cnt + 1
    if cnt >= (255-fd_c)/2:
        set_lights()
        set_lights()
        cnt = 0



        