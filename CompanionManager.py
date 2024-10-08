#CompanionManager.py

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QFrame,
                              QRadioButton, QButtonGroup, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os

class CompanionManager(QWidget):
    # TODO find a way to build out rows with the same companion to be placed in a row together. 
    # TODO fix an issue where only the first instance of a companion will be displayed.
    # TODO the files need to go somewhere. Add in a feature so that dropped files can be stored.

    def __init__(self, parent=None):
        super(CompanionManager, self).__init__(parent)
        self.right_layout = QVBoxLayout()
        self.setLayout(self.right_layout)
        self.setAcceptDrops(True)  # Enable drag-and-drop for this widget


    # Handles creation of Companion Buttons to the right layout
    def create_companion_buttons(self, companions):
        # Clear existing companion buttons
        for i in reversed(range(self.right_layout.count())):
            widget = self.right_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)  # Remove widget from the layout
                widget.deleteLater()    # Schedule it for deletion

        companion_buttons = {}
        companion_buttons_list = []
        companions_text = []

        for companion, type_data in companions.items():
            # Create a frame to contain the companion button and radio buttons
            companion_container = QFrame()
            companion_container.setFrameShape(QFrame.StyledPanel)
            container_layout = QVBoxLayout()
            companion_container.setLayout(container_layout)

            companion_button = QPushButton(companion)
            companion_button.setStyleSheet("background-color: #9C9C9C; color: black;") # Button color grey
            companion_button.setEnabled(True)
            companion_button.setVisible(True)
            companion_button.clicked.connect(self.companion_button_click)
            companions_text.append(companion_button.text())

            # Add button widget to layout
            container_layout.addWidget(companion_button)
            # self.right_layout.addWidget(companion_button)
            # Add frame to the main layout
            self.right_layout.addWidget(companion_container)
            
            # Store the frame and its type data
            companion_buttons[companion_container] = type_data
            companion_buttons_list.append(companion_button)

        return companion_buttons, companion_buttons_list


    def update_companion_buttons(self, button, sub_series_path):
        # Join current path from tree and series buttons to the current companion button.
        full_path = os.path.join(sub_series_path, button.text()) 
        if os.path.exists(full_path): # If built path is found
            button.setStyleSheet("background-color: #0B8ED4; color: white") # Folder exists, button is blue.
        else: # Path not found
            button.setStyleSheet("background-color: #C63F3F; color: white") # No folder found, button is red.


    # Handles creation of radio buttons below each associated companion button
    def create_radio_buttons(self, companion_buttons):
        for container, data in companion_buttons.items():
            button_group = QButtonGroup(self)  # Group radio buttons together
            
            # Iterate over each type-variable and create corresponding radio buttons
            for type_var in data['type-variable']:
                radio_button = QRadioButton(type_var)
                button_group.addButton(radio_button)

                # Add radio button to the frame layout
                hbox_layout = QHBoxLayout()
                hbox_layout.addWidget(radio_button)
                container.layout().addLayout(hbox_layout)
                radio_button.clicked.connect(self.type_button_click)


    # Handles creation of uni buttons for enabling of unique uni part groups
    def create_uni_input_widgets(self, companion_data, clicked_radio):
        # TODO BUG when input changes from uni to custom and vice-versa the system needs to override the currently displayed inputs
        #print("Companion Dict Data: ", companion_data)
        print("Clicked Radio: ", clicked_radio.text())
        # Create a horizontal layout to contain the UNI buttons
        uni_button_layout = QVBoxLayout()
            # Create and add UNI buttons to the layout
        for uni_data in companion_data:
            uni_button_text = "->".join(uni_data)

            # for entry in uni_data:
            uni_button = QPushButton(uni_button_text)
            uni_button.setStyleSheet("background-color: #9C9C9C; color: black;")
            uni_button_layout.addWidget(uni_button)
            uni_button.clicked.connect(self.uni_button_click)

        # Insert the UNI buttons layout right after the clicked radio button
        parent_layout = clicked_radio.parent().layout()
        index = parent_layout.indexOf(clicked_radio)
        parent_layout.insertLayout(index + 1, uni_button_layout)


    def update_uni_button(self, clicked_uni):
        print("Update UNI Button: ", clicked_uni.text())
        # TODO build logic to check status of uni part groups -- folder? file? .txt??


    # Handles creation of file image file drop widgets
    def create_custom_file_input_widgets(self, companion_data, companion_name, sub_series_button, clicked_radio):
        print("\nCreating Custom File Inputs")
        print("Sub Series Data: ", sub_series_button)

        # Create layouts for labels and drop areas
        label_layout = QHBoxLayout()
        hbox_layout = QHBoxLayout()

        for series, sub_series_data in companion_data.items():
            print("Series: ", series)
            for sub_series, companions in sub_series_data.items():
                if sub_series == sub_series_button:  # Only display sub series that match current button input
                    print("Sub Series: ", sub_series)
                    for comp_name, details in companions.items():
                        print(f"Comparing Name: {comp_name} to Name: {companion_name}")
                        if comp_name == companion_name:
                            print(f"\nCompanion {comp_name} match to {companion_name}")

                            if 'C=CUSTOM' in details['type-variable']:
                                print("Building input widgets")
                                for selection in details['selections']:
                                    print("Selection: ", selection)
                                    selection_label = QLabel(f"Selection: {selection['selection_1']} / {selection['selection_2']}")

                                    # Add the label to the label layout
                                    label_layout.addWidget(selection_label)

                                    # Create a drop area label
                                    drop_area = QLabel("Drop image here")
                                    drop_area.setStyleSheet("border: 2px dashed gray; padding: 10px;")
                                    drop_area.setAlignment(Qt.AlignCenter)
                                    drop_area.setFixedSize(105, 105)  # Adjust size as needed
                                    drop_area.setProperty("companion_name", comp_name)
                                    drop_area.installEventFilter(self)

                                    # Add the drop area to the horizontal layout
                                    hbox_layout.addWidget(drop_area)

                                # Find the correct parent layout to insert the label and drop area
                                parent_layout = clicked_radio.parent().layout()
                                index = parent_layout.indexOf(clicked_radio)

                                # Insert the label layout first (optional, if you want the labels above the drop areas)
                                parent_layout.insertLayout(index + 1, label_layout)
                                # Insert the drop areas layout directly beneath the radio button
                                parent_layout.insertLayout(index + 2, hbox_layout)

                            break  # Break out of the loop if a match is found

        
        # Insert the Custom Input drop layout right after the clicked radio button
        parent_layout = clicked_radio.parent().layout()
        index = parent_layout.indexOf(clicked_radio)
        parent_layout.insertLayout(index + 1, hbox_layout)


    # Handle File drop events
    def eventFilter(self, source, event):
        if event.type() == event.DragEnter and source.property("companion_name"):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()
        elif event.type() == event.Drop and source.property("companion_name"):
            if event.mimeData().hasUrls():
                urls = event.mimeData().urls()
                if urls:
                    file_path = urls[0].toLocalFile()
                    self.handle_dropped_file(source, file_path)
                event.acceptProposedAction()
        return super(CompanionManager, self).eventFilter(source, event)


    # Handles proper storage of dropped image file
    def handle_dropped_file(self, drop_area, file_path):
        companion_name = drop_area.property("companion_name")
        # Handle the dropped file (e.g., show it in the label)
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            drop_area.setPixmap(pixmap.scaled(drop_area.size(), Qt.AspectRatioMode.KeepAspectRatio))
        print(f"File dropped for {companion_name}: {file_path}")
        # Additional handling, such as storing the file path or uploading, can be done here
        # TODO finish building logic to actually store dropped image files
