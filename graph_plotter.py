import sys
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.Qt import *


class PlotWidget(QWidget):
    function_text = "sin(x)"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navToolbar = NavigationToolbar(self.canvas, self)
        self.mainLayout.addWidget(self.canvas)
        self.mainLayout.addWidget(self.navToolbar)

    def solve_func(self):
        function_text = self.parent().parent().nameTextbox.text()
        if function_text:
            self.function_text = function_text
            self.plot()

    def function(self, x):
        return eval(self.function_text, {
            'x': x,
            'sin': np.sin,
            'cos': np.cos,
            'tg': np.tan,
            'ctg': lambda x: 1 / np.tan(x),
            'e': np.exp,
            'sqrt': np.sqrt,
            'ln': np.log,
            'log': np.log10,
        })

    def plot(self):
        x = np.linspace(-100, 100, 20000)
        y = self.function(x)
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#DCDCDC')
        ax.axhline(y=0, xmin=-10.25, xmax=10.25, color='#000000')
        ax.axvline(x=0, ymin=-10, ymax=10, color='#000000')
        ax.set_ylim([-2, 2])
        ax.set_xlim([-5, 5])
        if self.function_text in ('sin(x)', 'cos(x)'):
            ax.axhline(y=1, xmin=-10.25, xmax=10.25, color='b', linestyle='--')
            ax.axhline(y=-1, xmin=-10.25, xmax=10.25, color='b', linestyle='--')
        ax.plot(x, y, linestyle='-', color='#008000', label=self.function_text)
        ax.legend(loc='upper right')
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()

    def initUi(self):
        self.centralWidget = QWidget(self)
        self.l = QVBoxLayout(self.centralWidget)
        self.bl = QHBoxLayout(self.centralWidget)
        self.plotWidget = PlotWidget(self)
        self.nameTextLabel = QLabel('f(x)=')
        self.nameTextbox = QLineEdit("")
        self.nameTextbox.setToolTip("Input: sin(x)\n"
                                    "4*x+2\n"
                                    "x^2-->x**2\n"
                                    "1/√x-->1/sqrt(x)\n"
                                    "e^x-->e(x)")
        self.plotButton = QPushButton('Plot', self)
        self.plotButton.clicked.connect(self.plotWidget.solve_func)
        self.clearButton = QPushButton('Clear')
        self.clearButton.clicked.connect(self.clear)
        self.plotButton.setStyleSheet('font-size: 12pt; font-weight: 530;')
        self.clearButton.setStyleSheet('font-size: 12pt; font-weight: 530;')
        self.bl.addWidget(self.nameTextLabel)
        self.bl.addWidget(self.nameTextbox)
        self.bl.addWidget(self.plotButton)
        self.bl.addWidget(self.clearButton)
        self.l.addLayout(self.bl)
        self.l.addWidget(self.plotWidget)
        self.setCentralWidget(self.centralWidget)

    def clear(self):
        self.plotWidget.figure.clear()
        self.plotWidget.canvas.draw()
        self.nameTextbox.clear()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?\n"
                                     "All unsaved data will be lost",
                                     QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    p = MainWindow()
    p.show()
    sys.exit(app.exec_())
