import serial
from datetime import datetime

SERIALPORT = '/dev/ttyACM0';
BAUDRATE = 115200

def buildLogFilePath():
    #logFileTime = datetime.now().strftime("%Y%m%d-%H%M")
    #return "logs/gassensor-" + logFileTime + ".log"
    return "logs/gassensor.log"

def logData(logFilePath):
    logfile = open(logFilePath, "w")
    ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=0)
    doLog = False
    while (1):
        line = ser.readline().decode("utf-8")
        if line != "":
            print(line)
            linetime = datetime.now().strftime("%H:%M:%S")
            if "GASES" in line:
                doLog = True
            if doLog:
                line = line.replace('GASES', 'GASES,' +linetime)
                line = line.replace('UNITS', 'UNITS,' + linetime)
                line = line.replace('DATA', 'DATA,' + linetime)
                logfile.write(line)
            
    logfile.close()

def main():
    logFilePath = buildLogFilePath()
    logData(logFilePath)

if __name__ == "__main__":
    main()