# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'canvasWidget_UI.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

class Ui_canvasWidget(object):
    def setupUi(self, canvasWidget):
        if not canvasWidget.objectName():
            canvasWidget.setObjectName(u"canvasWidget")
        canvasWidget.resize(791, 390)
        self.verticalLayoutWidget = QWidget(canvasWidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 771, 371))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.retranslateUi(canvasWidget)

        QMetaObject.connectSlotsByName(canvasWidget)
    # setupUi

    def retranslateUi(self, canvasWidget):
        canvasWidget.setWindowTitle(QCoreApplication.translate("canvasWidget", u"Form", None))
    # retranslateUi

