# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'soundWidget_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_soundWidget(object):
    def setupUi(self, soundWidget):
        if not soundWidget.objectName():
            soundWidget.setObjectName(u"soundWidget")
        soundWidget.resize(788, 902)
        self.gridLayoutWidget = QWidget(soundWidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 771, 136))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.in_sampleRateLabel = QLabel(self.gridLayoutWidget)
        self.in_sampleRateLabel.setObjectName(u"in_sampleRateLabel")

        self.gridLayout.addWidget(self.in_sampleRateLabel, 2, 3, 1, 1)

        self.in_sampleRateLineEdit = QLineEdit(self.gridLayoutWidget)
        self.in_sampleRateLineEdit.setObjectName(u"in_sampleRateLineEdit")

        self.gridLayout.addWidget(self.in_sampleRateLineEdit, 2, 4, 1, 1)

        self.out_sampleRateLabel = QLabel(self.gridLayoutWidget)
        self.out_sampleRateLabel.setObjectName(u"out_sampleRateLabel")

        self.gridLayout.addWidget(self.out_sampleRateLabel, 4, 0, 1, 1)

        self.toneLineEdit = QLineEdit(self.gridLayoutWidget)
        self.toneLineEdit.setObjectName(u"toneLineEdit")

        self.gridLayout.addWidget(self.toneLineEdit, 2, 1, 1, 1)

        self.speakersLabel = QLabel(self.gridLayoutWidget)
        self.speakersLabel.setObjectName(u"speakersLabel")

        self.gridLayout.addWidget(self.speakersLabel, 0, 0, 1, 1)

        self.speakersComboBox = QComboBox(self.gridLayoutWidget)
        self.speakersComboBox.setObjectName(u"speakersComboBox")

        self.gridLayout.addWidget(self.speakersComboBox, 0, 1, 1, 1)

        self.typeLabel = QLabel(self.gridLayoutWidget)
        self.typeLabel.setObjectName(u"typeLabel")

        self.gridLayout.addWidget(self.typeLabel, 1, 0, 1, 1)

        self.durationLineEdit = QLineEdit(self.gridLayoutWidget)
        self.durationLineEdit.setObjectName(u"durationLineEdit")

        self.gridLayout.addWidget(self.durationLineEdit, 3, 1, 1, 1)

        self.typeComboBox = QComboBox(self.gridLayoutWidget)
        self.typeComboBox.setObjectName(u"typeComboBox")

        self.gridLayout.addWidget(self.typeComboBox, 1, 1, 1, 1)

        self.durationLabel = QLabel(self.gridLayoutWidget)
        self.durationLabel.setObjectName(u"durationLabel")

        self.gridLayout.addWidget(self.durationLabel, 3, 0, 1, 1)

        self.toneLabel = QLabel(self.gridLayoutWidget)
        self.toneLabel.setObjectName(u"toneLabel")

        self.gridLayout.addWidget(self.toneLabel, 2, 0, 1, 1)

        self.out_sampleRateLineEdit = QLineEdit(self.gridLayoutWidget)
        self.out_sampleRateLineEdit.setObjectName(u"out_sampleRateLineEdit")

        self.gridLayout.addWidget(self.out_sampleRateLineEdit, 4, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)

        self.microphonesLabel = QLabel(self.gridLayoutWidget)
        self.microphonesLabel.setObjectName(u"microphonesLabel")

        self.gridLayout.addWidget(self.microphonesLabel, 1, 3, 1, 1)

        self.microphonesComboBox = QComboBox(self.gridLayoutWidget)
        self.microphonesComboBox.setObjectName(u"microphonesComboBox")

        self.gridLayout.addWidget(self.microphonesComboBox, 1, 4, 1, 1)

        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 3)
        self.gridLayout.setColumnStretch(4, 2)
        self.horizontalLayoutWidget = QWidget(soundWidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 160, 771, 80))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.PlayPauseButton = QPushButton(self.horizontalLayoutWidget)
        self.PlayPauseButton.setObjectName(u"PlayPauseButton")

        self.horizontalLayout.addWidget(self.PlayPauseButton)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.StartStopButton = QPushButton(self.horizontalLayoutWidget)
        self.StartStopButton.setObjectName(u"StartStopButton")

        self.horizontalLayout.addWidget(self.StartStopButton)

        self.verticalLayoutWidget = QWidget(soundWidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 250, 771, 641))
        self.verticalLayoutCanvas = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayoutCanvas.setObjectName(u"verticalLayoutCanvas")
        self.verticalLayoutCanvas.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayoutCanvas.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(soundWidget)
        self.speakersComboBox.currentIndexChanged.connect(soundWidget.out_device_changed)
        self.typeComboBox.currentTextChanged.connect(soundWidget.updateConfiguration)
        self.toneLineEdit.textChanged.connect(soundWidget.updateConfiguration)
        self.durationLineEdit.textChanged.connect(soundWidget.updateConfiguration)
        self.out_sampleRateLineEdit.textChanged.connect(soundWidget.updateConfiguration)
        self.PlayPauseButton.clicked.connect(soundWidget.toggle_output)
        self.microphonesComboBox.currentIndexChanged.connect(soundWidget.in_device_changed)
        self.in_sampleRateLineEdit.textChanged.connect(soundWidget.updateConfiguration)
        self.StartStopButton.clicked.connect(soundWidget.toggle_input)

        QMetaObject.connectSlotsByName(soundWidget)
    # setupUi

    def retranslateUi(self, soundWidget):
        soundWidget.setWindowTitle(QCoreApplication.translate("soundWidget", u"Form", None))
        self.in_sampleRateLabel.setText(QCoreApplication.translate("soundWidget", u"Echantillonage", None))
        self.in_sampleRateLineEdit.setText("")
        self.out_sampleRateLabel.setText(QCoreApplication.translate("soundWidget", u"Echantillonage", None))
        self.toneLineEdit.setText("")
        self.speakersLabel.setText(QCoreApplication.translate("soundWidget", u"Sortie", None))
        self.typeLabel.setText(QCoreApplication.translate("soundWidget", u"Type", None))
        self.durationLineEdit.setText("")
        self.durationLabel.setText(QCoreApplication.translate("soundWidget", u"Dur\u00e9e", None))
        self.toneLabel.setText(QCoreApplication.translate("soundWidget", u"Fr\u00e9quence", None))
        self.out_sampleRateLineEdit.setText("")
        self.microphonesLabel.setText(QCoreApplication.translate("soundWidget", u"Entr\u00e9e", None))
        self.PlayPauseButton.setText(QCoreApplication.translate("soundWidget", u"Jouer", None))
        self.StartStopButton.setText(QCoreApplication.translate("soundWidget", u"Enregistrer", None))
    # retranslateUi

