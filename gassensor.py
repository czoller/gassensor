import argparse
import serial
from datetime import datetime

SERIALPORT = '/dev/ttyACM0';
BAUDRATE = 115200
DEFAULT_DURATION = 10

def buildLogFilePath():
    logFileTime = datetime.now().strftime("%Y%m%d-%H%M")
    return "logs/gassensor-" + logFileTime + ".log"
    #return "logs/gassensor.log"

def logData(logFilePath, duration):
    logfile = open(logFilePath, "w")
    ser = serial.Serial(SERIALPORT, BAUDRATE, timeout=0)
    doLog = False
    startTime = None
    now = None
    while (not now or not startTime or (now - startTime).total_seconds() < duration):
        line = ser.readline().decode("utf-8")
        if line != "":
            print(line)
            now = datetime.now()
            linetime = now.strftime("%H:%M:%S")
            if not doLog and "G" in line:
                doLog = True
                startTime = now
            if doLog:
                line = line.replace('=', ',' + linetime + ',')
                logfile.write(line)
    logfile.close()


def parseArguments():
    argParser = argparse.ArgumentParser(description="Liest Daten vom Gassensor.");
    durationArg = argParser.add_mutually_exclusive_group(required=False)
    durationArg.add_argument('-s', '--seconds', type=int, help='Messdauer in Sekunden', required=False);
    durationArg.add_argument('-m', '--minutes', type=int, help='Messdauer in Minuten', required=False);
    durationArg.add_argument('-o', '--hours', type=int, help='Messdauer in Stunden', required=False);
    return argParser.parse_args(); 

def getDurationInSeconds(args):
    if args.hours:
        return args.hours * 60 * 60
    elif args.minutes:
        return args.minutes * 60
    elif args.seconds:
        return args.seconds
    else:
        return DEFAULT_DURATION

def main():
    args = parseArguments()
    duration = getDurationInSeconds(args)
    logFilePath = buildLogFilePath()
    logData(logFilePath, duration)
    
if __name__ == "__main__":
    main()