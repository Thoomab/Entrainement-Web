"""PySide6 port of the multimedia/audiooutput example from Qt v5.x, originating from PyQt"""

import sys
from pathlib import Path
from math import pi, sin
from struct import pack

import numpy as np

from PySide6.QtCore import (QByteArray, QIODevice, QBuffer, QSysInfo, QTimer,
                            qWarning, Slot)
from PySide6.QtMultimedia import (QAudio, QAudioDevice, QAudioFormat,
                                  QAudioSink, QMediaDevices)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
                               QMainWindow, QPushButton, QSlider,
                               QVBoxLayout, QWidget, QLineEdit)

from EarsDesktop.sound.soundFunctions import TYPE_FUNCTION


class Generator(QIODevice):    
    def __init__(self, format, type, frequency, duration, parent=None):
        super().__init__(parent)

        self.m_pos = 0
        self.buffer = QByteArray()

        self.format = format
        ""
        if type == TYPE_FUNCTION(1):
            self.typefunction = lambda x: self.generate_sinusoide(x)
        elif type == TYPE_FUNCTION(2):
            self.typefunction = self.generate_square
        elif type == TYPE_FUNCTION(3):
            self.typefunction = self.generate_white_noise
        elif type == TYPE_FUNCTION(4):
            self.typefunction = self.generate_pink_noise
        elif type == TYPE_FUNCTION(5):
            self.typefunction = self.generate_pink_noise
        elif type == TYPE_FUNCTION(6):
            self.typefunction = self.generate_sawtooth
        else:
            self.typefunction = lambda x: self.generate_sinusoide(x)
        """
        
        self.frequency = frequency
        self.duration = duration

        self.scaler = lambda x: x
        self.pack_format = ''

        self.initializeWriteFormat()

    def start(self, filepath = None):
        if filepath:
            try:
                self.generate_data_from_file(filepath)
            except:
                print("No data available")
        else:
            self.generate_data()

        self.open(QIODevice.ReadOnly)

    def stop(self):
        self.m_pos = 0
        self.close()

    def initializeWriteFormat(self):
        self.pack_format = ''

        # Choose the format needed
        sample_size = self.format.bytesPerSample() * 8  # Sample size (bits)
        if sample_size == 8:  # One sample is composed by 1 byte
            if self.format.sampleFormat() == QAudioFormat.UInt8:
                # Format is unsigned int : We transform value to positive value by
                # adding 1.0. Since values are in [0.0, 2.0] we scale them up to
                # 8 bits = 256 possible values
                self.scaler = lambda x: ((1.0 + x) / 2 * 255)
                self.pack_format = 'B'
            elif self.format.sampleFormat() == QAudioFormat.Int16:
                self.scaler = lambda x: x * 127
                self.pack_format = 'b'
        elif sample_size == 16:  # One sample is composed by 2 bytes
            little_endian = QSysInfo.ByteOrder == QSysInfo.LittleEndian
            if self.format.sampleFormat() == QAudioFormat.UInt8:
                self.scaler = lambda x: (1.0 + x) / 2 * 65535
                self.pack_format = '<H' if little_endian else '>H'
            elif self.format.sampleFormat() == QAudioFormat.Int16:
                self.scaler = lambda x: x * 32767
                self.pack_format = '<h' if little_endian else '>h'

        assert(self.pack_format != '')

    def generate_data(self):
        # Total length is composed by : 
        # duration * number of samples per second * number of channel * number of bytes per sample
        # Then, we divide by 100 000 to prevent the futur scale of the value according 
        # to the choosen fmt.sampleFormat
        length = (self.format.sampleRate() * self.format.channelCount() * self.format.bytesPerSample()) * self.duration
        self.buffer.clear()

        sample_index = 0
        while length >= 0:
            t = (sample_index % self.format.sampleRate()) / self.format.sampleRate()
            # We use self.typefunction, a lambda-expression to use the the rigth function to generate data
            value = self.generate_sinusoide(t)
            packed = pack(self.pack_format, int(self.scaler(value)))

            for _ in range(self.format.channelCount()):
                self.buffer.append(packed)
                length -= self.format.bytesPerSample()

            sample_index += 1

    def readData(self, maxlen):
        data = QByteArray()
        total = 0

        while maxlen > total:
            chunk = min(self.buffer.size() - self.m_pos, maxlen - total)
            data.append(self.buffer.mid(self.m_pos, chunk))
            self.m_pos = (self.m_pos + chunk) % self.buffer.size()
            total += chunk

        return data.data()

    def generate_data_from_file(self, filepath):
        # Load the .wav file into a QByteArray
        self.buffer.clear()
        with open(filepath, "rb") as f:
            self.buffer.append(f.read())
        
        return 0

    def bytesAvailable(self):
        return self.buffer.size() + super(Generator, self).bytesAvailable()

    def generate_sinusoide(self, t):
        """ Génère un son sinusoïdal : A * sin(2𝜋ft) """
        return np.sin(2 * np.pi * self.frequency * t)

    def generate_square(self, t):
        """ Génère un son carré : 𝐴 * (-1)^n * randn(𝑡) """
        return np.sign(np.sin(2 * np.pi * self.frequency * t))

    def generate_white_noise(self, t):
        """ Génère un bruit blanc : A * randn """
        return np.random.normal(size=int(self.format.sampleRate * self.duration))

    def generate_pink_noise(self, t):
        """ 
        Génère un bruit rose par la méthode de Voss-McCartney : ∑𝑖N=1*𝐴𝑖/𝑓𝑖
        """
        num_samples = int(self.format.sampleRate() * self.duration)
        num_rows = 16
        array = np.random.randn(num_rows, num_samples)
        array = np.cumsum(array, axis=1)
        array = array / np.arange(1, num_samples + 1)
        
        return np.sum(array, axis=0)
    
    def generate_triangle(self, t):
        """ Génère un son triangle : 2𝐴/𝜋*arcsin(sin(2𝜋𝑓𝑡)) """
        return (2 * np.abs(2 * (t * self.frequency - np.floor(t * self.frequency + 0.5))) - 1)
    
    def generate_sawtooth(self, t):
        """ Génère un son en dent de scie : 2𝐴/𝜋(𝑓𝑡−⌊𝑓𝑡+1/2⌋) """
        return (2 * (t * self.frequency - np.floor(t * self.frequency + 0.5)))

class AudioTest(QMainWindow):
    SUSPEND_LABEL = "Suspend playback"
    RESUME_LABEL = "Resume playback"

    DURATION_SECONDS = 10
    frequency = 600
    sampleRate = 48000

    def __init__(self, devices):
        super().__init__()

        self.devices = devices
        self.device = self.devices[0]
        self.output = None

        self.initialize_window()
        self.initialize_audio()

    def initialize_window(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.deviceBox = QComboBox()
        self.deviceBox.activated[int].connect(self.device_changed)
        for deviceInfo in self.devices:
            self.deviceBox.addItem(deviceInfo.description(), deviceInfo)

        layout.addWidget(self.deviceBox)

        self.m_suspendResumeButton = QPushButton()
        self.m_suspendResumeButton.clicked.connect(self.toggle_suspend_resume)
        self.m_suspendResumeButton.setText("Play")

        layout.addWidget(self.m_suspendResumeButton)

        self.setCentralWidget(central_widget)

    def initialize_audio(self):
        self.m_format = QAudioFormat()
        self.m_format.setSampleRate(self.sampleRate)
        self.m_format.setChannelCount(1)
        self.m_format.setSampleFormat(QAudioFormat.Int16)

        info = self.devices[0]
        if not info.isFormatSupported(self.m_format):
            qWarning("Default format not supported - trying to use nearest")
            self.m_format = info.nearestFormat(self.m_format)

        self.m_generator = Generator(self.m_format, TYPE_FUNCTION(1), self.frequency, self.DURATION_SECONDS, self)
        self.m_audioSink = None

    def create_audio_output(self):
        self.m_audioSink = QAudioSink(self.device, self.m_format)
        self.m_audioSink.stateChanged.connect(self.handle_state_changed)

        self.m_generator.start("io.raw")
        self.m_audioSink.start(self.m_generator)
        

    @Slot(int)
    def device_changed(self, index):
        self.m_generator.stop()
        self.m_audioSink.stop()
        self.device = self.deviceBox.itemData(index)

        self.create_audio_output()

    @Slot()
    def toggle_suspend_resume(self):
        if not self.m_audioSink:
            qWarning(f"status : Play")
            self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)
            self.create_audio_output()
            qWarning(f"state : {self.m_audioSink.state()}")
        elif self.m_audioSink.state() == QAudio.SuspendedState:
            qWarning("status: Suspended, resume()")
            self.m_audioSink.resume()
            self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)
        elif self.m_audioSink.state() == QAudio.ActiveState:
            qWarning("status: Active, suspend()")
            self.m_audioSink.suspend()
            self.m_suspendResumeButton.setText(self.RESUME_LABEL)
        elif self.m_audioSink.state() == QAudio.StoppedState:
            qWarning("status: Stopped, resume()")
            self.m_audioSink.resume()
            self.m_suspendResumeButton.setText(self.SUSPEND_LABEL)
        elif self.m_audioSink.state() == QAudio.IdleState:
            qWarning("status: IdleState")

    state_map = {
        QAudio.ActiveState: "ActiveState",
        QAudio.SuspendedState: "SuspendedState",
        QAudio.StoppedState: "StoppedState",
        QAudio.IdleState: "IdleState"}

    @Slot(QAudio.State)
    def handle_state_changed(self, state):
        state = self.state_map.get(state, 'Unknown')
        qWarning(f"state = {state}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Audio Output Test")

    devices = QMediaDevices.audioOutputs()
    if not devices:
        print('No audio outputs found.', file=sys.stderr)
        sys.exit(-1)

    audio = AudioTest(devices)
    audio.show()

    sys.exit(app.exec())