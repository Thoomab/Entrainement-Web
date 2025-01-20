from PySide6.QtWidgets import QMessageBox

class questionDialog(QMessageBox):
    def __init__(self, experimentationState: int, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle("Question")
        if (experimentationState == 1) :
            self.setText(f"Ready for the step {experimentationState} ? \n"
                         "Click on 'Yes' to start the acquisition ! 1")
        elif (experimentationState == 2) :
            self.setText(f"Ready for the step {experimentationState} ? \n"
                         "Click on 'Yes' to start the acquisition ! 2")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setIcon(QMessageBox.Icon.Question)