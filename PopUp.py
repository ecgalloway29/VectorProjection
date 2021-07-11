from PySide6.QtWidgets import (QLabel, QDialog, QPushButton, QVBoxLayout)


class PopUp(QDialog):

    def __init__(self, description:str, parent=None):
        super(PopUp, self).__init__(parent)
        self.layout = QVBoxLayout()

        description_label = QLabel()
        description_label.setText(description)

        close_button = QPushButton()
        close_button.setText("Close")
        close_button.clicked.connect(self.close)

        self.layout.addWidget(description_label)
        self.layout.addWidget(close_button)

        self.setLayout(self.layout)


def prep_popup(parent, message):
    pop = PopUp(message, parent)
    pop.show()