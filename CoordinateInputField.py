import sys
import os
from PySide6.QtWidgets import (QLineEdit, QPushButton, QApplication,
                               QVBoxLayout, QDialog, QFileDialog, QLabel, QHBoxLayout)
from PySide6.QtGui import QPixmap, QImage
from SettingsManager import get_working_directory
from PopUp import prep_popup, PopUp
import ImageManager as IM


class CoordinateInputField(QDialog):

    BLANK_INPUT = 'BLANK_INPUT'
    STANDARD_INPUT = 'STANDARD_INPUT'
    NORMAL_INPUT = 'NORMAL_INPUT'

    def __init__(self, file_name:str, on_finish_callback, input_mode, parent=None):
        super(CoordinateInputField, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.file_name = file_name
        self.image = IM.Image(file_name)
        self.on_finish_callback = on_finish_callback
        self.mode = input_mode

        self.x_min_line = ''
        self.x_max_line = ''
        self.y_min_line = ''
        self.y_max_line = ''

        self.cropped_label = ''
        self.original_label = ''
        self.volume_line = ''
        self.concentration_line = ''
        self.units_line = ''

        if input_mode == CoordinateInputField.BLANK_INPUT:
            self.to_blank_specification()
        elif input_mode == CoordinateInputField.STANDARD_INPUT:
            self.to_standard_specification()
        else:
            self.to_normal_specification()
            pass

    def to_blank_specification(self):

        file_name_display = QLabel()
        file_name_display.setText('Loaded from:\t' + self.file_name)

        self.layout.addWidget(file_name_display)

        image_row = QHBoxLayout()

        self.original_label = QLabel()

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_marked_scaled_original()))
        self.original_label.setPixmap(pix_map)

        image_row.addWidget(self.original_label)

        self.cropped_label = QLabel()

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_scaled_cropped()))
        self.cropped_label.setPixmap(pix_map)

        image_row.addWidget(self.cropped_label)

        self.layout.addLayout(image_row)

        instruction_label = QLabel()
        instruction_label.setText("Input the desired coordinates to read from.\nOn the left is your original "
                                  "image\nOn the right is a preview of the cropped image")

        self.layout.addWidget(instruction_label)

        entry_row_upper = QHBoxLayout()
        x_min_label = QLabel()
        x_min_label.setText("X Min")
        self.x_min_line = QLineEdit()
        self.x_min_line.setText(str(self.image.min_x))
        x_max_label = QLabel()
        x_max_label.setText("X Max")
        self.x_max_line = QLineEdit()
        self.x_max_line.setText(str(self.image.max_x))

        entry_row_upper.addWidget(x_min_label)
        entry_row_upper.addWidget(self.x_min_line)
        entry_row_upper.addWidget(x_max_label)
        entry_row_upper.addWidget(self.x_max_line)

        self.layout.addLayout(entry_row_upper)

        entry_row_lower = QHBoxLayout()
        y_min_label = QLabel()
        y_min_label.setText("Y Min")
        self.y_min_line = QLineEdit()
        self.y_min_line.setText(str(self.image.min_y))
        y_max_label = QLabel()
        y_max_label.setText("Y Max")
        self.y_max_line = QLineEdit()
        self.y_max_line.setText(str(self.image.max_y))

        entry_row_lower.addWidget(y_min_label)
        entry_row_lower.addWidget(self.y_min_line)
        entry_row_lower.addWidget(y_max_label)
        entry_row_lower.addWidget(self.y_max_line)

        self.layout.addLayout(entry_row_lower)

        button_row = QHBoxLayout()
        preview_button = QPushButton()
        preview_button.clicked.connect(self.preview_inputs)
        preview_button.setText("Preview")

        confirm_button = QPushButton()
        confirm_button.clicked.connect(self.confirm_inputs)
        confirm_button.setText("Confirm")

        button_row.addWidget(preview_button)
        button_row.addWidget(confirm_button)

        self.layout.addLayout(button_row)

        self.setLayout(self.layout)

        self.show()

    def to_standard_specification(self):

        file_name_display = QLabel()
        file_name_display.setText('Loaded from:\t' + self.file_name)

        self.layout.addWidget(file_name_display)

        image_row = QHBoxLayout()

        self.original_label = QLabel()

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_marked_scaled_original()))
        self.original_label.setPixmap(pix_map)

        image_row.addWidget(self.original_label)

        self.cropped_label = QLabel()

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_scaled_cropped()))
        self.cropped_label.setPixmap(pix_map)

        image_row.addWidget(self.cropped_label)

        self.layout.addLayout(image_row)

        instruction_label = QLabel()
        instruction_label.setText("Input the desired coordinates to read from.\nOn the left is your original "
                                  "image\nOn the right is a preview of the cropped image")

        self.layout.addWidget(instruction_label)

        entry_row_upper = QHBoxLayout()
        x_min_label = QLabel()
        x_min_label.setText("X Min")
        self.x_min_line = QLineEdit()
        self.x_min_line.setText(str(self.image.min_x))
        x_max_label = QLabel()
        x_max_label.setText("X Max")
        self.x_max_line = QLineEdit()
        self.x_max_line.setText(str(self.image.max_x))

        entry_row_upper.addWidget(x_min_label)
        entry_row_upper.addWidget(self.x_min_line)
        entry_row_upper.addWidget(x_max_label)
        entry_row_upper.addWidget(self.x_max_line)

        self.layout.addLayout(entry_row_upper)

        entry_row_lower = QHBoxLayout()
        y_min_label = QLabel()
        y_min_label.setText("Y Min")
        self.y_min_line = QLineEdit()
        self.y_min_line.setText(str(self.image.min_y))
        y_max_label = QLabel()
        y_max_label.setText("Y Max")
        self.y_max_line = QLineEdit()
        self.y_max_line.setText(str(self.image.max_y))

        entry_row_lower.addWidget(y_min_label)
        entry_row_lower.addWidget(self.y_min_line)
        entry_row_lower.addWidget(y_max_label)
        entry_row_lower.addWidget(self.y_max_line)

        self.layout.addLayout(entry_row_lower)

        concentration_row = QHBoxLayout()
        concentration_label = QLabel()
        concentration_label.setText("Concentration")
        self.concentration_line = QLineEdit()
        units_label = QLabel()
        units_label.setText("Units")
        self.units_line = QLineEdit()

        concentration_row.addWidget(concentration_label)
        concentration_row.addWidget(self.concentration_line)
        concentration_row.addWidget(units_label)
        concentration_row.addWidget(self.units_line)

        self.layout.addLayout(concentration_row)

        button_row = QHBoxLayout()
        preview_button = QPushButton()
        preview_button.clicked.connect(self.preview_inputs)
        preview_button.setText("Preview")

        confirm_button = QPushButton()
        confirm_button.clicked.connect(self.confirm_inputs)
        confirm_button.setText("Confirm")

        button_row.addWidget(preview_button)
        button_row.addWidget(confirm_button)

        self.layout.addLayout(button_row)

        self.setLayout(self.layout)

        self.show()

    def to_normal_specification(self):

        file_name_display = QLabel()
        file_name_display.setText('Loaded from:\t' + self.file_name)

        self.layout.addWidget(file_name_display)

        image_row = QHBoxLayout()

        self.original_label = QLabel()

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_marked_scaled_original()))
        self.original_label.setPixmap(pix_map)

        image_row.addWidget(self.original_label)

        self.cropped_label = QLabel()

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_scaled_cropped()))
        self.cropped_label.setPixmap(pix_map)

        image_row.addWidget(self.cropped_label)

        self.layout.addLayout(image_row)

        instruction_label = QLabel()
        instruction_label.setText("Input the desired coordinates to read from.\nOn the left is your original "
                                  "image\nOn the right is a preview of the cropped image")

        self.layout.addWidget(instruction_label)

        entry_row_upper = QHBoxLayout()
        x_min_label = QLabel()
        x_min_label.setText("X Min")
        self.x_min_line = QLineEdit()
        self.x_min_line.setText(str(self.image.min_x))
        x_max_label = QLabel()
        x_max_label.setText("X Max")
        self.x_max_line = QLineEdit()
        self.x_max_line.setText(str(self.image.max_x))

        entry_row_upper.addWidget(x_min_label)
        entry_row_upper.addWidget(self.x_min_line)
        entry_row_upper.addWidget(x_max_label)
        entry_row_upper.addWidget(self.x_max_line)

        self.layout.addLayout(entry_row_upper)

        entry_row_lower = QHBoxLayout()
        y_min_label = QLabel()
        y_min_label.setText("Y Min")
        self.y_min_line = QLineEdit()
        self.y_min_line.setText(str(self.image.min_y))
        y_max_label = QLabel()
        y_max_label.setText("Y Max")
        self.y_max_line = QLineEdit()
        self.y_max_line.setText(str(self.image.max_y))

        entry_row_lower.addWidget(y_min_label)
        entry_row_lower.addWidget(self.y_min_line)
        entry_row_lower.addWidget(y_max_label)
        entry_row_lower.addWidget(self.y_max_line)

        self.layout.addLayout(entry_row_lower)
        volume_row = QHBoxLayout()
        volume_label = QLabel()
        volume_label.setText("Volume")
        self.volume_line = QLineEdit()
        self.units_line = QLineEdit()

        volume_row.addWidget(volume_label)
        volume_row.addWidget(self.volume_line)

        self.layout.addLayout(volume_row)

        button_row = QHBoxLayout()
        preview_button = QPushButton()
        preview_button.clicked.connect(self.preview_inputs)
        preview_button.setText("Preview")

        confirm_button = QPushButton()
        confirm_button.clicked.connect(self.confirm_inputs)
        confirm_button.setText("Confirm")

        button_row.addWidget(preview_button)
        button_row.addWidget(confirm_button)

        self.layout.addLayout(button_row)

        self.setLayout(self.layout)

        self.show()

    def validate_inputs(self):
        try:
            max_x = int(self.x_max_line.text())
            min_x = int(self.x_min_line.text())
            max_y = int(self.y_max_line.text())
            min_y = int(self.y_min_line.text())

            if max_x <= min_x or max_y <= min_y:
                raise ValueError

            if self.mode == CoordinateInputField.STANDARD_INPUT:
                float(self.concentration_line.text())

            if self.mode == CoordinateInputField.NORMAL_INPUT:
                float(self.volume_line.text())

        except ValueError:
            prep_popup(self, "INVALID INPUTS!: All inputs must be an integer, such that Max X > Min X, and Max Y > "
                             "Min Y")
            return False

        return True

    def preview_inputs(self):
        if not self.validate_inputs():
            return False

        max_x = int(self.x_max_line.text())
        min_x = int(self.x_min_line.text())
        max_y = int(self.y_max_line.text())
        min_y = int(self.y_min_line.text())

        self.image.set_coordinates(min_x, min_y, max_x, max_y)

        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_scaled_cropped()))
        self.cropped_label.setPixmap(pix_map)
        pix_map = QPixmap.fromImage(IM.get_pix_map(self.image.get_marked_scaled_original()))
        self.original_label.setPixmap(pix_map)
        self.show()

    def confirm_inputs(self):
        if not self.validate_inputs():
            return False

        max_x = int(self.x_max_line.text())
        min_x = int(self.x_min_line.text())
        max_y = int(self.y_max_line.text())
        min_y = int(self.y_min_line.text())

        self.image.set_coordinates(min_x, min_y, max_x, max_y)

        if self.mode == CoordinateInputField.BLANK_INPUT:
            IM.add_blank(self.image)
            print("I ADDED THE BLANK")
        elif self.mode == CoordinateInputField.STANDARD_INPUT:
            IM.add_standard(self.image, float(self.concentration_line.text()), self.units_line)
            print("I ADDED THE STANDARD")
        else:
            self.image.set_volume(float(self.volume_line.text()))
            IM.add_image(self.image)
            print("I ADDED A NORMAL IMAGE")
        self.on_finish_callback()
