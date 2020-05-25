import sys
from typing import Callable
import numpy as np
import sympy as sy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.Qt import *

functions_list = []


def save_functions(function_text):
    functions_list.append(function_text)
    f = open(r'functions.txt', 'w')
    for element in functions_list:
        f.write(element)
        f.write('\n')
    f.close()


class PlotWidget(QWidget):
    function_text = "sin(x)"
    x = sy.Symbol('x')

    def __init__(self, parent=None):
        super().__init__(parent)

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
            try:
                self.plot()
            except Exception as e:
                print(e)

    def function(self, x, funs: dict = None) -> Callable:
        try:
            return eval(self.function_text, funs or {
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
        except Exception as e:
            print(e)
            return lambda x: 1

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

        if isinstance(y, int):
            y = np.array([y] * len(x))

        if self.function_text in ('sin(x)', 'cos(x)'):
            ax.axhline(y=1, xmin=-10.25, xmax=10.25, color='b', linestyle='--')
            ax.axhline(y=-1, xmin=-10.25, xmax=10.25, color='b', linestyle='--')

        ax.plot(x, y, linestyle='-', color='#008000', label=self.function_text)
        ax.legend(loc='upper right')
        self.canvas.draw()

        self.limits(self.function)
        self.derivative1(self.function)
        self.derivative2(self.function)
        save_functions(self.function_text)

    def limits(self, x):
        x = sy.Symbol('x')
        limitx0 = sy.limit(self.function(x, {
            'x': x,
            'sin': sy.sin,
            'cos': sy.cos,
            'tg': sy.tan,
            'ctg': lambda x: 1 / sy.tan(x),
            'e': sy.exp,
            'sqrt': sy.sqrt,
            'ln': sy.log,
        }), x, 0)
        self.parent().parent().valueLimit.setText(str(limitx0))
        print(limitx0)

    def derivative1(self, x):
        x = sy.Symbol('x')
        derivative = sy.diff(self.function(x, {
            'x': x,
            'sin': sy.sin,
            'cos': sy.cos,
            'tg': sy.tan,
            'ctg': lambda x: 1 / sy.tan(x),
            'e': sy.exp,
            'sqrt': sy.sqrt,
            'ln': sy.log,
        }), x)
        self.parent().parent().valueDerivative1.setText(str(derivative))
        print(derivative)

    def derivative2(self, x):
        x = sy.Symbol('x')
        derivative = sy.diff(self.function(x, {
            'x': x,
            'sin': sy.sin,
            'cos': sy.cos,
            'tg': sy.tan,
            'ctg': lambda x: 1 / sy.tan(x),
            'e': sy.exp,
            'sqrt': sy.sqrt,
            'ln': sy.log,
        }), x, 2)
        self.parent().parent().valueDerivative2.setText(str(derivative))
        print(derivative)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUi()

    def initUi(self):
        self.centralWidget = QWidget(self)
        self.l = QVBoxLayout(self.centralWidget)
        self.bl = QHBoxLayout(self.centralWidget)
        self.bll = QHBoxLayout(self.centralWidget)
        self.plotWidget = PlotWidget(self)
        self.nameTextLabel = QLabel('f(x)=')
        self.nameTextbox = QLineEdit(self)
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
        self.resultLimit = QLabel("Lim x-->0: ")
        self.valueLimit = QLabel(self)
        self.resultDerivative1 = QLabel("       f'(x)= ")
        self.valueDerivative1 = QLabel(self)
        self.resultDerivative2 = QLabel('       f"(x)= ')
        self.valueDerivative2 = QLabel(self)
        self.bl.addWidget(self.nameTextLabel)
        self.bl.addWidget(self.nameTextbox)
        self.bl.addWidget(self.plotButton)
        self.bl.addWidget(self.clearButton)
        self.bll.addWidget(self.resultLimit)
        self.bll.addWidget(self.valueLimit)
        self.bll.addWidget(self.resultDerivative1)
        self.bll.addWidget(self.valueDerivative1)
        self.bll.addWidget(self.resultDerivative2)
        self.bll.addWidget(self.valueDerivative2)
        self.l.addLayout(self.bl)
        self.l.addLayout(self.bll)
        self.l.addWidget(self.plotWidget)
        self.setCentralWidget(self.centralWidget)

    def clear(self):
        self.plotWidget.figure.clear()
        self.plotWidget.canvas.draw()
        self.nameTextbox.clear()
        self.valueLimit.clear()
        self.valueDerivative1.clear()
        self.valueDerivative2.clear()

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
