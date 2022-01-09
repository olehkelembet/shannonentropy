import sys
import math
import argparse

import numpy as np
import plotext as tplot

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.__fileSize=None
        self.__entropy=None
        self.__freqList=[]
        self.__fileName=''
        self.__fileName=sys.argv[1]

        self.setAcceptDrops(True)
        self.setWindowTitle(self.__fileName)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        self.canvas = FigureCanvas(Figure(figsize=(6, 4), dpi=100))
        layout.addWidget(self.canvas)
        self.calculate_entropy(self.__fileName)
        self.create_plot()
        self.canvas.draw()

    def calculate_entropy(self, file):
        with open(file, 'rb') as f:
            byteArr = list(f.read())
        f.close()
        self.__fileSize = len(byteArr)
        for b in range(256):
            ctr = 0
            for byte in byteArr:
                if byte == b:
                    ctr += 1
            self.__freqList.append(float(ctr) / self.__fileSize)
        ent = 0.0
        for freq in self.__freqList:
            if freq > 0:
                ent = ent + freq * math.log(freq, 2)
        ent = -ent
        self.__entropy=ent

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

    def create_cli_plot(self):
        n=len(self.__freqList)
        ind=np.arange(n)
        tplot.bar(ind, self.__freqList)
        tplot.title("Frequency of bytes from  0 to 255\nFILENAME: " + self.__fileName)
        tplot.show()

    def set_new_file_name(self, file_name):
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
        self.canvas.figure.clf()
        self.set_new_file_name(new_file)
        self.setWindowTitle(new_file)
        self.calculate_entropy(new_file)
        self.create_plot()
        self.canvas.draw()

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = Window()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
