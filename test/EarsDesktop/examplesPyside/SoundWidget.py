import sys
from pathlib import Path
from math import pi, sin
from struct import pack

import numpy as np

from PySide6.QtCore import (QByteArray, QIODevice, QBuffer, QSysInfo, QTimer,
                            qWarning)
from PySide6.QtMultimedia import (QAudio, QAudioDevice, QAudioFormat,
                                  QAudioSink, QAudioSource, QMediaDevices)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                               QMainWindow, QPushButton, QSlider,
                               QVBoxLayout, QWidget, QLineEdit)

from EarsDesktop.sound.soundFunctions import TYPE_FUNCTION
from EarsDesktop.examplesPyside.example_input import AudioInfo

from EarsDesktop.examplesPyside.audioChart import recorderChart
from EarsDesktop.examplesPyside.soundWidget_UI import Ui_soundWidget

SAMPLE_COUNT = 2000
RESOLUTION = 4


# TODO : Add slot to autocomplete users enter with "s" and "Hz" for LineEdit object
# TODO : Add canvas for input
# TODO : Add ouput type fonctionnality (sinus, carrée, ...)
class soundWidget(QWidget, Ui_soundWidget):
    DEFAULT_IN_DEVICE = QMediaDevices.defaultAudioInput()
    DEFAULT_IN_SAMPLE_RATE = 8000

    DEFAULT_OUT_DEVICE = QMediaDevices.defaultAudioOutput()
    DEFAULT_TYPE_FUNCTION = TYPE_FUNCTION(1)
    DEFAULT_TONE = 550
    DEFAULT_DURATION = 10
    DEFAULT_OUT_SAMPLE_RATE = 20000

    def __init__(self, mainwindow=None):
        super().__init__()

        self.mainwindow = mainwindow

        # Initialize UI
        self.setupUi(self)
        self.fillWidget()
        self.recorder = recorderChart()
        self.verticalLayoutCanvas.addWidget(self.recorder)

        # Initialize input/output audio
        self.recording = False
        self.initialize_audio_input()
        self.initialize_audio_output()
        self.updateConfiguration()

    def fillWidget(self):
        # Set variable to avoid error with device_changed slot
        self.audioSource = None
        self.generator = None
        self.audioSink = None

        # Set combobox's items with input/output devices
        self.in_devices = QMediaDevices.audioInputs()
        for device in self.in_devices:
            self.microphonesComboBox.addItem(device.description(), device)
        self.out_devices = QMediaDevices.audioOutputs()
        for device in self.out_devices:
            self.speakersComboBox.addItem(device.description(), device)

        # Set combobox's items with type of signal
        for signal in TYPE_FUNCTION:
            self.typeComboBox.addItem(str(signal), signal)

        # Set values for input widget with class default values
        self.in_sampleRateLineEdit.setText(str(self.DEFAULT_IN_SAMPLE_RATE))
        self.toneLineEdit.setText(f"{str(self.DEFAULT_TONE)} Hz")
        self.durationLineEdit.setText(f"{str(self.DEFAULT_DURATION)} s")
        self.out_sampleRateLineEdit.setText(str(self.DEFAULT_OUT_SAMPLE_RATE))
    
    def initialize_audio_input(self):
        # Set format for input data
        self.in_format = QAudioFormat()
        self.in_format.setSampleRate(self.DEFAULT_IN_SAMPLE_RATE)
        self.in_format.setChannelCount(1)
        self.in_format.setSampleFormat(QAudioFormat.UInt8)

        self.in_device = QMediaDevices.defaultAudioInput()
        if not self.in_device.isFormatSupported(self.in_format):
            qWarning("Format change to device preferred format (microphone). ")
            self.in_format = self.in_device.preferredFormat()

        self.recorder.setconfiguration(self.in_device, self.in_format)
        self.recording = False

    def initialize_audio_output(self):
        self.out_format = QAudioFormat()
        self.out_format.setSampleRate(self.DEFAULT_OUT_SAMPLE_RATE)
        self.out_format.setChannelCount(1)
        self.out_format.setSampleFormat(QAudioFormat.Int16)

        self.out_device = self.DEFAULT_OUT_DEVICE
        if not self.out_device.isFormatSupported(self.out_format):
            qWarning("Format change to the device preferred format (speakers).")
            self.out_format = self.out_device.preferredFormat()

        self.generator = Generator(self.out_format, self.DEFAULT_TYPE_FUNCTION, self.DEFAULT_TONE, self.DEFAULT_DURATION, self)
        self.audioSink = None

    def play_datastream(self):
        self.audioSink = QAudioSink(self.out_device, self.out_format)

        self.generator.start()
        self.audioSink.start(self.generator)

    def start_datastream(self):
        self.recorder.start()

        def start_slot():
            len = self.audioSource.bytesAvailable()
            buffer_size = 4096
            if len > buffer_size:
                len = buffer_size
            buffer: QByteArray = self.io.read(len)
            if len > 0:
                level = self.info.calculate_level(buffer, len)
                self.mesureCanvas.update_plot(level)
            
        #self.io.readyRead.connect(self._readyRead)
    
    def stop_datastream(self):
        self.recorder.stop()

    def playandstart(self):
        self.play()
        self.start()

    def toggle_input(self):
        if not self.recording:
            self.recording = True
            self.recorder.start()
            self.StartStopButton.setText("End")
        else:
            self.recording = False
            self.recorder.stop()
            self.StartStopButton.setText("Start")

        """
        if not self.recorder._audio_input:
            self.StartStopButton.setText("End")
            self.start_datastream()
        elif (self.recorder._audio_input.state() == QAudio.SuspendedState) or (self.recorder._audio_input.state() == QAudio.StoppedState):
            self.start_datastream()
            self.StartStopButton.setText("End")
        elif self.recorder._audio_input.state() == QAudio.ActiveState:
            self.stop_datastream()
            self.StartStopButton.setText("Start")
        """

        # else no-op

    def toggle_output(self):
        if not self.audioSink:
            self.PlayPauseButton.setText("Pause")
            #self.sourceCanvas = self.mainwindow.canvasWidget.Source
            #self.sourceCanvas.startstream()
            self.play_datastream()
        elif self.audioSink.state() == QAudio.SuspendedState:
            self.PlayPauseButton.setText("Pause")
            self.audioSink.resume()
            #self.sourceCanvas.startstream()
        elif self.audioSink.state() == QAudio.ActiveState:
            self.PlayPauseButton.setText("Play")
            self.audioSink.suspend()
            #self.sourceCanvas.stopstream()
        elif self.audioSink.state() == QAudio.StoppedState:
            self.PlayPauseButton.setText("Pause")
            self.audioSink.resume()
            #self.sourceCanvas.startstream()

    def toggle_both(self):
        if not self.audioSource or not self.audioSink:
            self.playandstart()
            self.BothButton.setText("End both")
        elif (self.audioSource.state() != QAudio.ActiveState) or (self.audioSink.state() != QAudio.ActiveState):
            self.audioSource.resume()
            self.audioSink.resume()
            self.playandstart()
        else:
            self.audioSink.suspend()
            self.audioSource.suspend()
            self.BothButton.setText("Begin both")

    def in_device_changed(self, index: int):
        if self.audioSource:  # To avoid error at combobox's items initialization
            self.audioSource.stop()

        self.in_device = self.microphonesComboBox.currentData()

    def out_device_changed(self, index: int):
        if self.generator:  # To avoid error at combobox's items initialization
            self.generator.stop()
            self.audioSink.stop()

        self.out_device = self.speakersComboBox.currentData()

    def updateConfiguration(self):
        self.type = self.typeComboBox.currentData()
        if self.toneLineEdit.text() != '':
            self.tone = int(self.toneLineEdit.text().split(" ")[0])
        if self.durationLineEdit.text() != '':
            self.duration = int(self.durationLineEdit.text().split(" ")[0])
        if self.out_sampleRateLineEdit.text() != '':
            self.out_sampleRate = int(self.out_sampleRateLineEdit.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Audio Output Test")

    audio = soundWidget()
    audio.setWindowTitle("audio")
    
    audio.show()

    sys.exit(app.exec())
