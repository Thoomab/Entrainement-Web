import sys
from pathlib import Path
from math import pi, sin
from struct import pack

import numpy as np

from PySide6.QtCore import (QByteArray, QIODevice, QSysInfo,
                            qWarning, QFile, QMargins, Qt)
from PySide6.QtMultimedia import (QAudio, QAudioFormat,
                                  QAudioSink, QAudioSource, QMediaDevices)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QPushButton,
                               QVBoxLayout, QWidget)
from PySide6.QtGui import QPainter, QPalette, QPaintEvent

from EarsDesktop.sound.soundFunctions import TYPE_FUNCTION

class AudioInfo:
    def __init__(self, format: QAudioFormat):
        super().__init__()
        self.m_format = format
        self.m_level = 0.0

    def calculate_level(self, data: bytes, length: int) -> float:
        channel_bytes: int = int(self.m_format.bytesPerSample())
        sample_bytes: int = int(self.m_format.bytesPerFrame())
        num_samples: int = int(length / sample_bytes)

        maxValue: float = 0
        m_offset: int = 0

        for i in range(num_samples):
            for j in range(self.m_format.channelCount()):
                value = 0
                if len(data) > m_offset:
                    data_sample = data[m_offset:]
                    value = self.m_format.normalizedSampleValue(data_sample)
                maxValue = max(value, maxValue)
                m_offset = m_offset + channel_bytes

        return maxValue


class RenderArea(QWidget):
    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        self.m_level = 0
        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)
        self.setMinimumHeight(30)
        self.setMinimumWidth(200)

    def set_level(self, value):
        self.m_level = value
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(Qt.black)
        frame = painter.viewport() - QMargins(10, 10, 10, 10)

        painter.drawRect(frame)

        if self.m_level == 0.0:
            # QPainter needs an explicit end() in PyPy. This will become a context manager in 6.3.
            painter.end()
            return

        pos: int = round((frame.width() - 1) * self.m_level)
        painter.fillRect(
            frame.left() + 1, frame.top() + 1, pos, frame.height() - 1, Qt.red
        )
        # QPainter needs an explicit end() in PyPy. This will become a context manager in 6.3.
        painter.end()


class Generator(QIODevice):    
    def __init__(self, format, type, frequency, duration, parent=None):
        super().__init__(parent)

        self.m_pos = 0
        self.buffer = QByteArray()

        self.format = format
        """
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


class InOutWidget(QWidget):
    def __init__(self, mainwindow = None):
        super().__init__()

        self.mainwindow = mainwindow

        self.initialize_window()
        self.initialize_audio_input()
        self.initialize_audio_output()
    
    def initialize_window(self):
        self.layout = QVBoxLayout(self)

        self.canvas = RenderArea(self)
        self.layout.addWidget(self.canvas)

        self.in_device_combobox = QComboBox()
        self.devices = QMediaDevices.audioInputs()
        for device in self.devices:
            self.in_device_combobox.addItem(device.description(), device)
        self.in_device_combobox.currentTextChanged.connect(self.setInDevice)
        self.layout.addWidget(self.in_device_combobox)

        self.out_device_combobox = QComboBox()
        self.devices = QMediaDevices.audioOutputs()
        for device in self.devices:
            self.out_device_combobox.addItem(device.description(), device)
        self.out_device_combobox.currentTextChanged.connect(self.setOutDevice)
        self.layout.addWidget(self.out_device_combobox)

        self.horizontalLayout = QHBoxLayout()

        self.PlayPauseButton = QPushButton()
        self.PlayPauseButton.clicked.connect(self.toggle_output)
        self.PlayPauseButton.setText("Play")
        self.horizontalLayout.addWidget(self.PlayPauseButton)

        self.StartEndButton = QPushButton()
        self.StartEndButton.clicked.connect(self.toggle_input)
        self.StartEndButton.setText("Start")
        self.horizontalLayout.addWidget(self.StartEndButton)

        self.BothButton = QPushButton()
        self.BothButton.clicked.connect(self.toggle_both)
        self.BothButton.setText("Begin both")
        self.horizontalLayout.addWidget(self.BothButton)

        self.layout.addLayout(self.horizontalLayout)

    def initialize_audio_input(self):
        self.in_format = QAudioFormat()
        self.in_format.setSampleRate(48000)
        self.in_format.setChannelCount(1)
        self.in_format.setSampleFormat(QAudioFormat.Int16)

        self.info = AudioInfo(self.in_format)

        self.in_device = QMediaDevices.audioInputs()[0]
        if not self.in_device.isFormatSupported(self.in_format):
            qWarning("Format not supported by the input device (microphone).")
        
        self.io = None
        self.audioSource = None

    def initialize_audio_output(self):
        self.out_format = QAudioFormat()
        self.out_format.setSampleRate(48000)
        self.out_format.setChannelCount(1)
        self.out_format.setSampleFormat(QAudioFormat.Int16)

        self.out_device = QMediaDevices.audioOutputs()[0]
        if not self.out_device.isFormatSupported(self.out_format):
            qWarning("Format not supported by the output device (speakers).")

        self.generator = None  # Generator(self.out_format, "sinusoide", 550, 10, self)
        self.audioSink = None

    def play(self):
        self.generator = Generator(self.out_format, "sinusoide", 550, 10, self)
        self.audioSink = QAudioSink(self.out_device, self.out_format)

        self.generator.start("io.raw")
        self.audioSink.start(self.generator)

    def stopplaying(self):
        self.audioSink.stop()
        self.generator.stop()

    def start(self, filename: str = "io.raw"):
        self.io = QFile()
        self.io.setFileName(filename)
        self.io.open(QIODevice.OpenModeFlag.ReadWrite | QIODevice.OpenModeFlag.Truncate)
        self.audioSource = QAudioSource(self.in_device, self.in_format)
        self.audioSource.start(self.io)

        def start_slot():
            len = self.audioSource.bytesAvailable()
            buffer_size = 4096
            if len > buffer_size:
                len = buffer_size
            buffer: QByteArray = self.io.read(len)
            if len > 0:
                level = self.info.calculate_level(buffer, len)
                self.canvas.set_level(level)
                self.io.write(str(level))

        self.io.readyRead.connect(start_slot)

    def stoprecording(self):
        self.audioSource.stop()
        self.io.close()
        if self.mainwindow and self.mainwindow.experimentationMode:
            self.mainwindow.state()

    def playandstart(self):
        self.play()
        self.start()

    def toggle_input(self, event, filename = "io.raw"):
        if not self.audioSource:
            self.StartEndButton.setText("End")
            self.start(filename)
        elif self.audioSource.state() == QAudio.StoppedState:
            self.StartEndButton.setText("End")
            self.start(filename)
        elif self.audioSource.state() == QAudio.ActiveState:
            self.StartEndButton.setText("Start")
            self.stoprecording()
        # else no-op

    def toggle_output(self):
        if not self.audioSink:
            self.PlayPauseButton.setText("Pause")
            self.play()
        elif self.audioSink.state() == QAudio.ActiveState:
            self.stopplaying()
            self.PlayPauseButton.setText("Play")
        elif self.audioSink.state() == QAudio.StoppedState:
            self.play()
            self.PlayPauseButton.setText("Pause")

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

    def setInDevice(self):
        self.in_device = self.in_device_combobox.currentData()
    
    def setOutDevice(self):
        self.out_device = self.out_device_combobox.currentData()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Audio Output Test")

    audio = InOutWidget()
    audio.show()

    sys.exit(app.exec())