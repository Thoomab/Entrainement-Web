import sys 

from PySide6.QtWidgets import QApplication

from EarsDesktop.ui.MainWindow import Logiciel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("HearMetrics")

    fen = Logiciel()
    fen.resize(1200, 1000)
    fen.show()
 
    sys.exit(app.exec())