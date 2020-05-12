import os
import argparse
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
from PyPDF2 import PdfFileMerger, PdfFileReader

def createCharts(data, pdfFilePath):
    file0 = pdfFilePath.replace('.pdf', '.0.pdf')
    file1 = pdfFilePath.replace('.pdf', '.1.pdf')
    file2 = pdfFilePath.replace('.pdf', '.2.pdf')
    createChart(data, file0, ['NH3', 'NO2', 'H2', 'C2H5OH'])
    createChart(data, file1, ['CO'])
    createChart(data, file2, ['C3H8', 'C4H10', 'CH4'])
    joinPdf([file0, file1, file2], pdfFilePath)
    
def createChart(data, pdfFilePath, gases):
    fig = go.Figure()
    for gas in gases:
        d = filterData(data, gas) 
        fig.add_trace(go.Scatter(x=d.index, y=d[gas], name=gas))
    fig.update_yaxes(title_text='ppm')
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), showlegend=True)
    fig.write_image(pdfFilePath)
    
def filterData(data, gas):
    d = data[[gas]]
    return d[(np.abs(stats.zscore(d)) < 3).all(axis=1)]
    
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
    argParser = argparse.ArgumentParser(description="Erzeugt Graphen von Gassensordaten.");
    argParser.add_argument('csvfile', help='Pfad der CSV-Datei')
    return argParser.parse_args(); 

def main():
    args = parseArguments()
    data = readCsvFile(args.csvfile)
    pdfFilePath = args.csvfile.replace('.csv', '.pdf')
    createCharts(data, pdfFilePath)
    
if __name__ == "__main__":
    main()