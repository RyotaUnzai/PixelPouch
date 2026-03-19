from PySide6.QtWidgets import QComboBox as QComboBox, QHBoxLayout as QHBoxLayout, QLabel as QLabel, QPushButton as QPushButton, QVBoxLayout as QVBoxLayout

class Ui_Form:
    verticalLayout: QVBoxLayout
    horizontalLayout: QHBoxLayout
    label_target_role: QLabel
    comboBox_fontfamily: QComboBox
    comboBox_style: QComboBox
    pushButton_set_font: QPushButton
    def setupUi(self, Form) -> None: ...
    def retranslateUi(self, Form) -> None: ...
