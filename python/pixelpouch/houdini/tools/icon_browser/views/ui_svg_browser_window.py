# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'svg_browser_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.3
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QSizePolicy, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(978, 755)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit_search_edit = QLineEdit(Form)
        self.lineEdit_search_edit.setObjectName(u"lineEdit_search_edit")

        self.verticalLayout.addWidget(self.lineEdit_search_edit)

        self.lineEdit_selected_edit = QLineEdit(Form)
        self.lineEdit_selected_edit.setObjectName(u"lineEdit_selected_edit")

        self.verticalLayout.addWidget(self.lineEdit_selected_edit)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lineEdit_search_edit.setPlaceholderText(QCoreApplication.translate("Form", u"Search SVG...", None))
    # retranslateUi

