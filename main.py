from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pandas as pd
from matplotlib import pyplot as plt
import sys

#TODO After fixing other todos you can pull out Strategies into a file and import them at the top!

class MainWindow(QMainWindow):
    
        def __init__(self, plotting_strategy: Strategy):
            super(MainWindow, self).__init__()
            self.setGeometry(50, 50 , 500 , 300)
            self.setWindowTitle("MY Awsome App")
            self.UI()
            self._plotting_strategy = plotting_strategy

        @property
        def strategy(self) -> Strategy:
            """
            The Context maintains a reference to one of the Strategy objects. The
            Context does not know the concrete class of a strategy. It should work
            with all strategies via the Strategy interface.
            """
            return self._strategy

        @strategy.setter
        def strategy(self, strategy: Strategy):
            """
            Usually, the Context allows replacing a Strategy object at runtime.
            """
            self._strategy = strategy

        def UI(self):
            self.combo = QComboBox(self)
            self.combo.move(150 , 100)
            names = self.list_craft();
            for i in names:
                self.combo.addItem(i)
            self.combo2 = QComboBox(self)
            self.combo2.move(150 , 160)
            names = self.list_craft();
            for i in names:
                self.combo2.addItem(i)
            self.button = QPushButton("Plot",self)
            self.button.move(150,130)
            self.button.clicked.connect(self.plot2_per)

            self.show()

        def list_craft(self):
            list1 = []
            file = open("countries.csv", "rt")
            countries = set()
            for line in file:
                country = line[:line.find(',')]
                if country not in countries:
                    list1 += [country]
                countries.add(country)
            file.close()
            return list1

        def plot(self):
            self.strategy.plot()

class Strategy():
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    @abstractmethod
    def plot(self):
        pass

#TODO: Instead of self (from MainWindow) pass some object... 
class PlotGraphA(Strategy):
    def plot(self):
        self.data = pd.read_csv('countries.csv')
        comboText = self.combo.currentText()
        comboText2 = self.combo2.currentText()
        self.cuntry1 = self.data[self.data.country == comboText]
        self.cuntry2 = self.data[self.data.country == comboText2]
        plt.plot(self.cuntry1.year, self.cuntry1.population / 10 ** 6)
        plt.plot(self.cuntry2.year, self.cuntry2.population / 10 ** 6)
        plt.legend([comboText, comboText2])
        plt.title('Population change')
        plt.xlabel('years')
        plt.ylabel('Number of people in mln')
        plt.show()

#TODO: Instead of self (from MainWindow) pass some object... 
class PlotGraphB(Strategy):
    def plot(self, data: List):
        self.data = pd.read_csv('countries.csv')
        comboText = self.combo.currentText()
        comboText2 = self.combo2.currentText()
        self.cuntry1 = self.data[self.data.country == comboText]
        self.cuntry2 = self.data[self.data.country == comboText2]
        self.cuntry1_growth = self.cuntry1.population / self.cuntry1.population.iloc[0] * 100
        self.cuntry2_growth = self.cuntry2.population / self.cuntry2.population.iloc[0] * 100
        plt.plot(self.cuntry1.year, self.cuntry1_growth)
        plt.plot(self.cuntry2.year, self.cuntry2_growth )
        plt.legend([comboText, comboText2])
        plt.title('Population growth change')
        plt.xlabel('years')
        plt.ylabel('Population growth change')
        plt.show()

def run():
    app = QApplication(sys.argv)
    #TODO some logic to choose between plot A or B 
    window = MainWindow(PlotGraphA())
    #window = MainWindow(PlotGraphB())
    window.show()
    app.exec_()

if __name__ == "__main__":
    run()
