# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'font_assigne_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1432, 755)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_target_role = QLabel(Form)
        self.label_target_role.setObjectName(u"label_target_role")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_target_role.sizePolicy().hasHeightForWidth())
        self.label_target_role.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.label_target_role)

        self.comboBox_fontfamily = QComboBox(Form)
        self.comboBox_fontfamily.setObjectName(u"comboBox_fontfamily")

        self.horizontalLayout.addWidget(self.comboBox_fontfamily)

        self.comboBox_style = QComboBox(Form)
        self.comboBox_style.setObjectName(u"comboBox_style")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_style.sizePolicy().hasHeightForWidth())
        self.comboBox_style.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.comboBox_style)

        self.pushButton_set_font = QPushButton(Form)
        self.pushButton_set_font.setObjectName(u"pushButton_set_font")
        sizePolicy1.setHeightForWidth(self.pushButton_set_font.sizePolicy().hasHeightForWidth())
        self.pushButton_set_font.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.pushButton_set_font)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_target_role.setText(QCoreApplication.translate("Form", u"Target Role", None))
        self.pushButton_set_font.setText(QCoreApplication.translate("Form", u"Set", None))
    # retranslateUi

