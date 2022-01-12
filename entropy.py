import sys
import math
import argparse

import numpy as np
import plotext as tplot

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class Window(QtWidgets.QMainWindow):

    def __init__(self, file_name:str, freq_list:list):
        super().__init__()

        self.__fileName = file_name
        self.__freqList = freq_list

        self.setAcceptDrops(True)
        self.setWindowTitle(self.__fileName)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        self.canvas = FigureCanvas(Figure(figsize=(6, 4), dpi=100))
        layout.addWidget(self.canvas)
        self.create_plot()

    def calculate_entropy(self):

        with open(self.__fileName, 'rb') as f:
            byteArr = list(f.read())
        f.close()

        freqList = []
        fileSize = len(byteArr)
        for b in range(256):
            ctr = 0
            for byte in byteArr:
                if byte == b:
                    ctr += 1
            freqList.append(float(ctr) / fileSize)
        if len(self.__freqList):
            self.__freqList.clear()
            self.__freqList = freqList

        ent = 0.0
        for freq in freqList:
            if freq > 0:
                ent = ent + freq * math.log(freq, 2)
        ent = -ent

    def create_plot(self):
        n=len(self.__freqList)
        ind=np.arange(n)
        width=1.0

        ax = self.canvas.figure.add_subplot(111)
        ax.bar(ind, self.__freqList, width)

        ax.set_autoscalex_on(False)
        ax.set_xlim([0,255])
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Byte')
        ax.set_title('Frequency of bytes from 0 to 255')

    def set_file_name(self, file_name):
        self.__fileName=file_name

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self,e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        new_file=''
        for f in files:
            new_file=f

        self.set_file_name(new_file)
        self.canvas.figure.clf()
        self.setWindowTitle(new_file)
        self.calculate_entropy()
        self.create_plot()
        self.canvas.draw()



def calculate_entropy(file:str):

    with open(file, 'rb') as f:
        byteArr = list(f.read())
    f.close()

    freqList = []
    fileSize = len(byteArr)
    for b in range(256):
        ctr = 0
        for byte in byteArr:
            if byte == b:
                ctr += 1
        freqList.append(float(ctr) / fileSize)

    ent = 0.0
    for freq in freqList:
        if freq > 0:
            ent = ent + freq * math.log(freq, 2)
    ent = -ent

    return ent, freqList

def create_cli_plot(file_name:str, freq_list:list):

    n=len(freq_list)
    ind=np.arange(n)
    tplot.bar(ind, freq_list)
    tplot.title("Frequency of bytes from  0 to 255\nFILENAME: " + file_name)
    tplot.show()


def create_parser():

    parser = argparse.ArgumentParser(description='Shannon entropy calculation.')
    parser.add_argument('--file', '-f', required=False, help='target file')
    parser.add_argument('--entropy', '-e', required=False, action='store_true', help='ptint entropy to shell')
    parser.add_argument('--console', '-c', required=False, action='store_true', help='draw histogram in console')
    parser.add_argument('--window', '-w', required=False, action='store_true', help='create gui window')

    return parser.parse_args()


def parse_arguments(args):

    entropy, freq_list = calculate_entropy(args.file)
    if args.entropy:
        print(f'Shannon entropy is: {entropy}.')
    if args.console:
        create_cli_plot(args.file, freq_list)
    if args.window:
        qapp = QtWidgets.QApplication(sys.argv)
        app = Window(args.file, freq_list)
        app.show()
        app.activateWindow()
        app.raise_()
        qapp.exec_()



if __name__ == "__main__":
    
    args = create_parser()
    parse_arguments(args)

