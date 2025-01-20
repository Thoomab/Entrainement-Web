import sys
import traceback
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import QPointF, QRunnable, QThreadPool, QObject, Signal, QTimer
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
        QAudioSource, QMediaDevices, QAudioSink, QAudioSource)
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QVBoxLayout, QPushButton


SAMPLE_COUNT = 2000
RESOLUTION = 4

class WorkerSignals(QObject):
    finished = Signal()
    result = Signal(object)
    error = Signal(tuple)


class Worker(QRunnable):
    def __init__(self, buffer, series, parent=None):
        super().__init__(parent)

        self.buffer = buffer
        self.series = series
        self.signals = WorkerSignals()
        self.isRunning = True

    def run(self):
        device = QMediaDevices.defaultAudioInput()
        #format = device.preferredFormat()
        format = QAudioFormat()
        format.setChannelCount(1)
        format.setSampleRate(8000)
        format.setSampleFormat(QAudioFormat.Int16)
        
        buffer = self.buffer
        series = self.series

        try:
            audioSource = QAudioSource(device, format, parent=None)
            io = audioSource.start()
            #self._io_device.readyRead.connect(self._readyRead)
            while self.isRunning:
                data = io.readAll()
                available_samples = data.size() // RESOLUTION
                start = 0
                if (available_samples < SAMPLE_COUNT):
                    start = SAMPLE_COUNT - available_samples
                    for s in range(start):
                        buffer[s].setY(buffer[s + available_samples].y())

                data_index = 0
                for s in range(start, SAMPLE_COUNT):
                    value = (ord(data[data_index]) - 128) / 128
                    buffer[s].setY(value)
                    data_index = data_index + RESOLUTION
                
                series.replace(buffer)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.finished.emit()

    def stop(self):
        self.io_device.stop()
        self.isRunning = False

    def _readyRead(self, io, buffer):
        data = io.readAll()
        available_samples = data.size() // RESOLUTION
        start = 0
        if (available_samples < SAMPLE_COUNT):
            start = SAMPLE_COUNT - available_samples
            for s in range(start):
                buffer[s].setY(buffer[s + available_samples].y())

        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            value = (ord(data[data_index]) - 128) / 128
            buffer[s].setY(value)
            data_index = data_index + RESOLUTION
        #self._series.replace(buffer)


class MainWindow(QWidget):
    def __init__(self, device, format=None):
        super().__init__()
        self.device = device

        self.layout = QVBoxLayout(self)

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
        name = device.description()
        self._chart.setTitle(f"Data from the microphone ({name})")

        self._chart_view = QChartView(self._chart)
        self.layout.addWidget(self._chart_view)

        self._buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self._series.append(self._buffer)

        self.threadpool = QThreadPool(parent=None)
        self.start()

    def start(self):
        self.recorderWorker = Worker(self._buffer, self._series)
        self.recorderWorker.signals.finished.connect(self.thread_complete)
        self.threadpool.start(self.recorderWorker)

    def stop(self):
        self.recorderWorker.stop()

    def thread_complete(self):
        print("THREAD COMPLETE !")

        


if __name__ == '__main__':
    app = QApplication(sys.argv)

    input_devices = QMediaDevices.audioInputs()
    if not input_devices:
        QMessageBox.warning(None, "audio", "There is no audio input device available.")
        sys.exit(-1)
    main_win = MainWindow(input_devices[0])
    #main_win.setWindowTitle("audio")
    available_geometry = main_win.screen().availableGeometry()
    size = available_geometry.height() * 3 / 4
    main_win.resize(size, size)
    main_win.show()
    sys.exit(app.exec())