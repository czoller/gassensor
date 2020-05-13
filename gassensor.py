import os
import argparse
import serial
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from scipy import stats, signal
import plotly.graph_objects as go
from PyPDF2 import PdfFileMerger, PdfFileReader
from builtins import str

LOGFILE_DIR = 'logs'
SERIALPORT = '/dev/ttyACM0'
BAUDRATE = 115200
DEFAULT_DURATION = 10

def buildLogFilePath(args):
    if args.test:
        return LOGFILE_DIR + "/gassensor.log"
    else:
        logFileTime = datetime.now().strftime("%Y%m%d-%H%M")
        if args.hours:
            duration = str(args.hours) + 'h'
        elif args.minutes:
            duration = str(args.minutes) + 'm'
        elif args.seconds:
            duration = str(args.seconds) + 's'
        else:
            duration = str(DEFAULT_DURATION) + 's'
        return LOGFILE_DIR + "/gassensor-" + logFileTime + "-" + duration + ".log"

def parseMarkerTime(args):
    if args.line:
        try:
            return datetime.strptime(args.line, '%H:%M')
        except:
            print("WARNING: Uhrzeit für Markierung nicht erkannt.")
    return None

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
        if 'UNITS' in line or line.count(',') != 7:
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
    
def createPlots(data, pdfFilePath, markerTime):
    file0 = pdfFilePath.replace('.pdf', '.0.pdf')
    file1 = pdfFilePath.replace('.pdf', '.1.pdf')
    file2 = pdfFilePath.replace('.pdf', '.2.pdf')
    createPlot(data, file0, ['NH3', 'NO2', 'H2', 'C2H5OH'], 'Ammoniak (NH3), Stickstoffdioxid (NO2), molek. Wasserstoff (H2), Ethanol (C2H5OH)', markerTime)
    createPlot(data, file1, ['CO'], 'Kohlenmonoxid (CO)', markerTime)
    createPlot(data, file2, ['C3H8', 'C4H10', 'CH4'], 'Propan (C3H8), Butan (C4H10), Methan (CH4)', markerTime)
    joinPdf([file0, file1, file2], pdfFilePath)
    
def createPlot(data, pdfFilePath, gases, title, markerTime):
    fig = go.Figure()
    for gas in gases:
        d = filterData(data, gas) 
        fig.add_trace(go.Scatter(x=d.index, y=d[gas], name=gas))
    fig.update_yaxes(title_text='ppm')
    
    shapes = []
    annotations = []
    if (data.index[-1] - data.index[0]).total_seconds() > 10 * 60:
        x10min = data.index[0] + timedelta(minutes = 10)
        shapes.append(dict(type='line', xref='x', yref='paper', x0=x10min, y0=0, x1=x10min, y1=1.1, line=dict(color='grey',dash='dot')))
        annotations.append(dict(text='Gassensor<br>aufwärmen', x=x10min, y=1.1, xref='x', yref='paper', xanchor='right', align='right', showarrow=False, font=dict(color='grey')))
    if markerTime:
        markerTime = datetime.combine(d.index[0].date(), markerTime.time())
        if markerTime < d.index[0]:
            markerTime = datetime.combine(d.index[-1].date(), markerTime.time())
        shapes.append(dict(type='line', xref='x', yref='paper', x0=markerTime, y0=0, x1=markerTime, y1=1.1))
        annotations.append(dict(text='Standheizung<br>einschalten', x=markerTime, y=1.1, xref='x', yref='paper', xanchor='left', align='left', showarrow=False))
    
    fig.update_layout(margin=dict(l=20, r=20, t=100, b=20), showlegend=True, title=title, shapes=shapes, annotations=annotations)
    fig.write_image(pdfFilePath)
    
def filterData(data, gas):
    d = data[[gas]]
    d = d[(np.abs(stats.zscore(d)) < 3).all(axis=1)]
    
    wl = int(np.ceil(len(d) / 50) // 2 * 2 + 1)
    if wl > 3:
        d[gas] = signal.savgol_filter(d[gas], wl, 3)
    
    return d
    
def joinPdf(sourceFiles, destFile):
    mergedObject = PdfFileMerger(strict=False)
    for sourceFile in sourceFiles:
        mergedObject.append(PdfFileReader(sourceFile, 'rb'))
    mergedObject.write(destFile)
    for sourceFile in sourceFiles:
        os.remove(sourceFile)

def readCsvFile(csvfile):
    return pd.read_csv(csvfile, index_col=0, parse_dates=True)    

def parseArguments():
    argParser = argparse.ArgumentParser(description="Liest Daten vom Gassensor.");
    durationArg = argParser.add_mutually_exclusive_group(required=False)
    durationArg.add_argument('-S', '--seconds', type=int, help='Messdauer in Sekunden', required=False);
    durationArg.add_argument('-M', '--minutes', type=int, help='Messdauer in Minuten', required=False);
    durationArg.add_argument('-H', '--hours', type=float, help='Messdauer in Stunden', required=False);
    argParser.add_argument('-t', '--test', action="store_true", help='Test-Logfile ohne Zeitstempel überschreiben')
    argParser.add_argument('-i', '--input', type=str, help='Prozessiert ein Zwischenprodukt anstatt eine Messung vorzunehmen, Formate: .log oder .csv')
    argParser.add_argument('-l', '--line', type=str, help='Uhrzeit, an der eine Markierung gesetzt werden soll')
    return argParser.parse_args(); 

def main():
    args = parseArguments()
    if args.input and args.input.endswith('.csv'):
        csvFilePath = args.input
    else:
        if args.input and args.input.endswith('.log'):
            logFilePath = args.input
        else:
            duration = getDurationInSeconds(args)
            logFilePath = buildLogFilePath(args)
            logData(logFilePath, duration)
        csvFilePath = logFilePath.replace('.log', '.csv')
        createCsv(logFilePath, csvFilePath)
    data = readCsvFile(csvFilePath)
    pdfFilePath = csvFilePath.replace('.csv', '.pdf')
    markerTime = parseMarkerTime(args)
    createPlots(data, pdfFilePath, markerTime)
    
if __name__ == "__main__":
    main()