import sys
from struct import unpack
import matplotlib
from numpy import round

matplotlib.use('Qt5Agg')

from PySide6.QtCore import QTimer, QByteArray
from PySide6.QtWidgets import QApplication, QWidget

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.pyplot import Line2D
from matplotlib.animation import FuncAnimation

import numpy as np

from EarsDesktop.ui.canvasWidget_UI import Ui_canvasWidget

def emitter(p=0.1):
    """Return a random value in [0, 1) with probability p, else 0."""
    while True:
        v = np.random.rand()
        if v > p:
            return 0.
        else:
            return np.random.rand()

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, dt=0.02):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.dt = dt  # diff time for update
        self.dt_window = 2
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-200, 200)
        self.ax.set_xlim(0, self.dt_window) 

    def update_plot(self, y):
        """ 
        Return the line object with his new data. 
        Causually updating the displayed axe, if the curve go further 
        the max displayed time value.
        """
        lastt = self.tdata[-1]  # Last point calculate
        # We update the window to display the curve
        if lastt >= self.tdata[0] + self.dt_window:
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.dt_window)
            self.ax.figure.canvas.draw()

        # This slightly more complex calculation avoids floating-point issues
        # from just repeatedly adding `self.dt` to the previous value.
        t = self.tdata[0] + len(self.tdata) * self.dt
        if isinstance(y, QByteArray):
            array = unpack('b', y.data())
            for el in array:
                self.ydata.append(el)
                self.tdata.append(t)
        else:
            self.ydata.append(y)
            self.tdata.append(t)

        self.ydata.append(y)
        self.tdata.append(t)

        self.line.set_data(self.tdata, round(self.ydata, 3))
        
        self.draw()

class canvasWidget(QWidget, Ui_canvasWidget):

    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow

        self.setupUi(self)
        self.Source = MplCanvas()
        self.verticalLayout.addWidget(self.Source, stretch=1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Animated Canvas Test")

    w = canvasWidget()
    w.show()
    
    app.exec()