import argparse
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go

def createCharts(data, pdfFilePath):
    createChart(data, pdfFilePath.replace('.pdf', '.0.pdf'), ['NH3', 'NO2', 'H2', 'C2H5OH'])
    createChart(data, pdfFilePath.replace('.pdf', '.1.pdf'), ['CO'])
    createChart(data, pdfFilePath.replace('.pdf', '.2.pdf'), ['C3H8', 'C4H10', 'CH4'])
    
def createChart(data, pdfFilePath, gases):
    fig = go.Figure()
    for gas in gases:
        subdata = data[[gas]]
        subdata = subdata[(np.abs(stats.zscore(subdata)) < 3).all(axis=1)] 
        fig.add_trace(go.Scatter(x=subdata.index, y=subdata[gas], name=gas))
    fig.update_yaxes(title_text='ppm')
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.write_image(pdfFilePath)

def readCsvFile(csvfile):
    return pd.read_csv(csvfile, index_col=0, parse_dates=True)
    
def parseArguments():
    argParser = argparse.ArgumentParser(description="Erzeugt Graphen von Gassensordaten.");
    argParser.add_argument('csvfile', help='Pfad der CSV-Datei')
    return argParser.parse_args(); 

def main():
    args = parseArguments()
    data = readCsvFile(args.csvfile)
    print(data)
    pdfFilePath = args.csvfile.replace('.csv', '.pdf')
    createCharts(data, pdfFilePath)
    
if __name__ == "__main__":
    main()