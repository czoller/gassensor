import argparse
import pandas as pd
import plotly.graph_objects as go

def createCharts(data, pdfFilePath):
    createChart(data, pdfFilePath, ['NH3', 'NO2', 'H2', 'C2H5OH'])
    
def createChart(data, pdfFilePath, gases):
    fig = go.Figure()
    for gas in gases:
        fig.add_trace(go.Scatter(x=data['time'], y=data[gas], name=gas))
    fig.update_yaxes(title_text='ppm')
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    fig.write_image(pdfFilePath)

def readCsvFile(csvfile):
    return pd.read_csv(csvfile, parse_dates=[0])
    
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