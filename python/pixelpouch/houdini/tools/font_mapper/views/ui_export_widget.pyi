from PySide6.QtWidgets import QHBoxLayout as QHBoxLayout, QLabel as QLabel, QLineEdit as QLineEdit, QPushButton as QPushButton, QVBoxLayout as QVBoxLayout

class Ui_Form:
    verticalLayout: QVBoxLayout
    horizontalLayout: QHBoxLayout
    label: QLabel
    lineEdit_exportpath: QLineEdit
    pushButton_set_exportpath: QPushButton
    def setupUi(self, Form) -> None: ...
    def retranslateUi(self, Form) -> None: ...
