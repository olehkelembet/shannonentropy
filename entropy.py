import sys
import math

import numpy as np
import plotext as tplot

from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


class Window(QtWidgets.QMainWindow):
    fileSize=0
    entropy=0
    freqList=[]

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)
        self.canvas = FigureCanvas(Figure(figsize=(6, 4), dpi=100))
        layout.addWidget(self.canvas)
        self.calculate_entropy()
        self.create_plot()
        self.canvas.draw()

    def calculate_entropy(self):
        with open(sys.argv[1], 'rb') as f:
            byteArr = list(f.read())
        f.close()
        self.fileSize = len(byteArr)
        for b in range(256):
            ctr = 0 
            for byte in byteArr:
                if byte == b:
                    ctr += 1
            self.freqList.append(float(ctr) / self.fileSize)
        ent = 0.0
        for freq in self.freqList:
            if freq > 0:
                ent = ent + freq * math.log(freq, 2)
        ent = -ent
        self.entropy=ent

    def create_plot(self):
        n=len(self.freqList)
        ind=np.arange(n)
        width=1.0

        ax = self.canvas.figure.add_subplot(111)
        ax.bar(ind, self.freqList, width)

        ax.set_autoscalex_on(False)
        ax.set_xlim([0,255])
        ax.set_ylabel('Frequency')
        ax.set_xlabel('Byte')
        ax.set_title('Frequency of bytes from 0 to 255')

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
        for f in files:
            print(f)


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = Window()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
