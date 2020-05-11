import serial
from datetime import datetime

def buildLogFilePath():
    #logFileTime = datetime.now().strftime("%Y%m%d-%H%M")
    #return "logs/gassensor-" + logFileTime + ".log"
    return "logs/gassensor.log"

def logData(logFilePath):
    logfile = open(logFilePath, "w")
    ser = serial.Serial(COMPORT, BAUDRATE, timeout=0)
    while (1):
        line = ser.readline().decode("utf-8")
        if (line != ""):
            linetime = datetime.now().strftime("%H:%M:%S")
            line = line.replace('\n', '\n' + linetime + ',')
            print(line)
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
    logFilePath = buildLogFilePath()
    logData(logFilePath)

if __name__ == "__main__":
    main()