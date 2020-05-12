import argparse
import serial
from datetime import datetime

LOGFILE_DIR = 'logs'
SERIALPORT = '/dev/ttyACM0'
BAUDRATE = 115200
DEFAULT_DURATION = 10

def buildLogFilePath(test):
    if test:
        return LOGFILE_DIR + "/gassensor.log"
    else:
        logFileTime = datetime.now().strftime("%Y%m%d-%H%M")
        return LOGFILE_DIR + "/gassensor-" + logFileTime + ".log"

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
                logline =    line.replace('G', linetime + ' G')
                logline = logline.replace('U', linetime + ' U')
                logline = logline.replace('D', linetime + ' D')
                logfile.write(logline)
    logfile.close()
    
def createCsv(logFilePath, csvFilePath):
    logfile = open(logFilePath, "r")
    csvfile = open(csvFilePath, "w")
    for line in logfile:
        if 'UNITS' in line or not ',' in line:
            continue
        elif 'GASES' in line:
            csvline = 'time,' + line.split('=')[1]
        else:
            csvline = line.replace(' DATA=', ',')
        csvfile.write(csvline)
    csvfile.close()
    logfile.close()
    

def getDurationInSeconds(args):
    if args.hours:
        return args.hours * 60 * 60
    elif args.minutes:
        return args.minutes * 60
    elif args.seconds:
        return args.seconds
    else:
        return DEFAULT_DURATION

def parseArguments():
    argParser = argparse.ArgumentParser(description="Liest Daten vom Gassensor.");
    durationArg = argParser.add_mutually_exclusive_group(required=False)
    durationArg.add_argument('-S', '--seconds', type=int, help='Messdauer in Sekunden', required=False);
    durationArg.add_argument('-M', '--minutes', type=int, help='Messdauer in Minuten', required=False);
    durationArg.add_argument('-H', '--hours', type=float, help='Messdauer in Stunden', required=False);
    argParser.add_argument('-t', '--test', action="store_true", help='Test-Logfile ohne Zeitstempel überschreiben')
    return argParser.parse_args(); 

def main():
    args = parseArguments()
    duration = getDurationInSeconds(args)
    logFilePath = buildLogFilePath(args.test)
    logData(logFilePath, duration)
    csvFilePath = logFilePath.replace('.log', '.csv')
    createCsv(logFilePath, csvFilePath)
    
if __name__ == "__main__":
    main()