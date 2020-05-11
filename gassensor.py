import serial
from datetime import datetime

def logData():
    logfiletime = datetime.now().strftime("%Y%m%d-%H%M")
    logfilepath = "logs/gassensor-" + logfiletime + ".log"
    logfile = open(logfilepath, "w")
    
    ser = serial.Serial(COMPORT, BAUDRATE, timeout=0)
    while (1):
        line = ser.readline().decode("utf-8")
        if (line != ""):
            logfile.write(line)
            
    logfile.close()

""" -------------------------------------------
MAIN APPLICATION
"""  

print("Start Serial Monitor")
print

COMPORT = '/dev/ttyACM0';
BAUDRATE = 115200

def main():
    logData()

if __name__ == "__main__":
    main()