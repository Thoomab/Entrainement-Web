from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QMainWindow, QMessageBox

import numpy as np
import pandas as pd

from EarsDesktop.sound.example_in_out import InOutWidget

from EarsDesktop.ui.UI import Ui_MainWindow
from EarsDesktop.ui.canvasWidget import MplCanvas
from EarsDesktop.ui.questionDialog import questionDialog

# TODO : Add Canvas to plot output / input signal
# TODO : Complete experimentation
class Logiciel(QMainWindow, Ui_MainWindow):
    FILE_PATH_PER_STATE = ["EarsDesktop\\sound\\mesureSilence.raw", #Pas de bruit, verifier si sim brancher correctement
                        "EarsDesktop\\sound\\mesureSaine.raw",#Bruit simple oreille bien
                        "EarsDesktop\\sound\\mesureChaineCassee.raw",#oreille physique cassé, oreilleavec état comme patient
                        "EarsDesktop\\sound\\mesureApresChir.raw"] #apres chirurgie
    #regarder satus bar
    def __init__(self): 
        super().__init__() 

        # Set UI
        self.setupUi(self)

        self.soundWidget = InOutWidget(self)
        self.soundWidgetLayout.addWidget(self.soundWidget)

        self.canvasWidget = MplCanvas()
        #self.verticalLayout.addWidget(self.canvasWidget)
        

        # Set experiment
        self.experimentationMode = False
        self.experimentationState = 0
        self.data = []

    def launchExperiment(self):
        self.experimentationMode = True
        self.state()
        
    def state(self):
        self.experimentationMode = True
        self.experimentationState += 1
        if self.experimentationState == 5:
            self.evaluation()
            self.experimentationState = 0
            self.experimentationMode = False
        else:
            dialog = questionDialog(self.experimentationState)
            if dialog.exec() == QMessageBox.Yes:
                filepath = self.FILE_PATH_PER_STATE[self.experimentationState - 1]
                self.statusBar().showMessage("Sound sending...")
                if self.experimentationState == 1:
                    self.soundWidget.toggle_input(filepath)
                elif self.experimentationState == 2:
                    self.soundWidget.toggle_input(filepath)
                elif self.experimentationState == 3:
                    self.soundWidget.toggle_input(filepath)
                elif self.experimentationState == 4:
                    self.soundWidget.toggle_input(filepath)
            else:
                self.statusBar().showMessage("Experience canceled")
                self.experimentationState -= 1
                self.experimentationMode = False

    def evaluation(self):
        # TODO : Définir un format d'écriture/lecture spécifique

        self.verticalLayout.addWidget(self.canvasWidget)
        #audio = AudioInfo(self.soundWidget.in_format)
        for state in range(self.experimentationState - 1):
            with open(self.FILE_PATH_PER_STATE[state], 'rb') as f:
                bytes = f.read()
                data = np.frombuffer(bytes, dtype=np.uint8).astype(float) * 5 / 256
            self.data.append(data)
        print(data.shape)
        self.canvasWidget.ax.plot(data[0])
        self.canvasWidget.ax.fig.canvas.draw()
        self.experimentationState = 0
        self.experimentationMode = False

