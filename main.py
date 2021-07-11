import sys
import os
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QFileDialog, QLabel, QHBoxLayout)
from PySide6.QtGui import QPixmap, QImage
from SettingsManager import get_working_directory
from PopUp import prep_popup, PopUp
import ImageManager as IM
from CoordinateInputField import CoordinateInputField
import GraphGenerator


def quit_program():
    quit(1)


# Opens a dialogue to open an image
def get_file():
    file_name = QFileDialog.getOpenFileName(form, "Select Image", get_working_directory(), "Image Files (*.jpg *.png)")
    return file_name


class Menu(QDialog):

    def __init__(self, parent=None):
        super(Menu, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.widgets = []
        self.layouts = []

        self.to_start_menu()

    def add_widget(self, widget, layout=-1):
        self.widgets.append(widget)
        if layout == -1:
            self.layout.addWidget(widget)
        else:
            layout.addWidget(widget)

    def add_layout(self, layout):
        self.layouts.append(layout)
        self.layout.addLayout(layout)

    def wipe_screen(self):
        for w in self.widgets:
            w.deleteLater()
        self.widgets = []
        for l in self.layouts:
            l.deleteLater()
        self.layouts = []

    def display(self):
        self.setLayout(self.layout)
        self.show()

    def to_start_menu(self):
        self.wipe_screen()

        print("TO START MENU")

        # Prepares the start button
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.to_blank_loading)
        self.add_widget(start_button)

        # Prepares the quit button
        quit_button = QPushButton("Quit")
        self.add_widget(quit_button)
        quit_button.clicked.connect(quit_program)

        self.display()

    def to_blank_loading(self):
        self.wipe_screen()

        instructions = QLabel()
        instructions.setText("Click below to select your blank image. \nIt is assumed to have a volume of 0 and a "
                             "concentration of 0")
        self.add_widget(instructions)

        select_blank_button = QPushButton("Select Blank")
        select_blank_button.clicked.connect(self.load_blank)
        self.add_widget(select_blank_button)
        self.display()

    def load_blank(self):
        print("LOADING BLANK")

        loaded_file = get_file()[0]
        if os.path.exists(loaded_file):
            self.to_blank_specification(loaded_file)
        else:
            prep_popup(self, "Invalid Image File")

    def to_blank_specification(self, file_name):
        self.wipe_screen()

        self.add_widget(CoordinateInputField(file_name, self.to_standard_loading, CoordinateInputField.BLANK_INPUT))

        self.display()

    def to_standard_loading(self):
        self.wipe_screen()

        instructions = QLabel()
        instructions.setText(
            "Click below to select your standard image. \nYou will have to supply a known concentration")
        self.add_widget(instructions)

        select_standard_button = QPushButton("Select Standard")
        select_standard_button.clicked.connect(self.load_standard)
        self.add_widget(select_standard_button)
        self.display()

    def load_standard(self):
        loaded_file = get_file()[0]
        if os.path.exists(loaded_file):
            self.to_standard_specification(loaded_file)
        else:
            prep_popup(self, "Invalid Image File")

    def to_standard_specification(self, loaded_file):
        self.wipe_screen()

        self.add_widget(CoordinateInputField(loaded_file, self.to_image_loading, CoordinateInputField.STANDARD_INPUT))

        self.display()

    def to_image_loading(self):
        self.wipe_screen()

        instructions = QLabel()
        instructions.setText(
            "Click below to add an image, or head to results. \nYou will have to supply the added volume for any "
            "added images")
        self.add_widget(instructions)

        added = QLabel()
        added.setText(IM.get_state())
        self.add_widget(added)

        select_image_button = QPushButton("Load Another Image")
        select_image_button.clicked.connect(self.load_image)

        further_instructions = QLabel()
        further_instructions.setText("Select below to display the graph, or output your results to a .csv (spreadsheet)"
                                     " file")

        to_results_button = QPushButton("Display Graph")
        to_results_button.clicked.connect(self.to_results)

        save_results_button = QPushButton("Save As CSV")
        save_results_button.clicked.connect(self.save_csv)

        self.add_widget(select_image_button)
        self.add_widget(to_results_button)
        self.add_widget(save_results_button)

        self.display()

    def load_image(self):
        loaded_file = get_file()[0]
        if os.path.exists(loaded_file):
            self.to_image_specification(loaded_file)
        else:
            prep_popup(self, "Invalid Image File")

    def to_image_specification(self, loaded_file):
        self.wipe_screen()

        self.add_widget(CoordinateInputField(loaded_file, self.to_image_loading, CoordinateInputField.NORMAL_INPUT))

        self.display()

    def to_results(self):
        GraphGenerator.generate_graph()

    def save_csv(self):
        GraphGenerator.generate_csv()

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Menu()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec())
