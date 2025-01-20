import sys
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, Slot, qWarning
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
        QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QMessageBox


SAMPLE_COUNT = 2000
RESOLUTION = 4


class recorderChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self._series = QLineSeries()
        self._chart = QChart()
        self._chart.addSeries(self._series)
        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, SAMPLE_COUNT)
        self._axis_x.setLabelFormat("%g")
        self._axis_x.setTitleText("Samples")
        self._axis_y = QValueAxis()
        self._axis_y.setRange(-1, 1)
        self._axis_y.setTitleText("Audio level")
        self._chart.setAxisX(self._axis_x, self._series)
        self._chart.setAxisY(self._axis_y, self._series)
        self._chart.legend().hide()
        self._chart.setTitle(f"Data from the microphone")

        self._chart_view = QChartView(self._chart)
        
        self.centralWidget = QWidget(self)
        self.layout = QVBoxLayout(self.centralWidget)        
        self.layout.addWidget(self._chart_view)

        self.setCentralWidget(self.centralWidget)

        self._buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self._series.append(self._buffer)

        self.device = QMediaDevices.defaultAudioInput()
        #self.format = self.device.preferredFormat()
        print(self.device.preferredFormat())
        self.format = QAudioFormat()
        self.format.setChannelCount(1)
        self.format.setSampleRate(6000)
        self.format.setSampleFormat(QAudioFormat.UInt8)

        
        self._audio_input = QAudioSource(self.device, self.format, self)
        self._io_device = self._audio_input.start()
        self._io_device.readyRead.connect(self._readyRead)

    def setconfiguration(self, device, format):
        self.device = device
        self.format = format

    def start(self):
        self._audio_input = QAudioSource(self.device, self.format, self)
        self._io_device = self._audio_input.start()
        self._io_device.readyRead.connect(self._readyRead)

    def stop(self):
        if self._audio_input is not None:
            self._audio_input.stop()

    def _readyRead(self):
        data = self._io_device.readAll()
        available_samples = data.size() // RESOLUTION
        start = 0
        if (available_samples < SAMPLE_COUNT):
            start = SAMPLE_COUNT - available_samples
            for s in range(start):
                self._buffer[s].setY(self._buffer[s + available_samples].y())
        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            value = (ord(data[data_index]) - 128) / 128
            self._buffer[s].setY(value)
            data_index = data_index + RESOLUTION
        self._series.replace(self._buffer)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    input_devices = QMediaDevices.audioInputs()
    if not input_devices:
        QMessageBox.warning(None, "audio", "There is no audio input device available.")
        sys.exit(-1)
    main_win = recorderChart()
    main_win.setconfiguration(input_devices[0], input_devices[0].preferredFormat())
    main_win.setWindowTitle("audio")
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 3 / 4
    main_win.resize(size, size)
    main_win.show()

    main_win.start()
    sys.exit(app.exec())