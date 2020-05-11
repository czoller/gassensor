import sys, os, serial, threading

def monitor():
    ser = serial.Serial(COMPORT, BAUDRATE, timeout=0)
    text_file = open("gassensor.log", "w")
    while (1):
        line = ser.readline().decode("utf-8")
        if (line != ""):
            print(line)
            text_file.write(line)
            
    print("Stop Monitoring")
    text_file.close()

""" -------------------------------------------
MAIN APPLICATION
"""  

print("Start Serial Monitor")
print

COMPORT = '/dev/ttyACM0';
BAUDRATE = 115200

monitor()
