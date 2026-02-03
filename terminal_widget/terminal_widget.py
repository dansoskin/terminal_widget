import time
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea, QGroupBox, QLineEdit, QPlainTextEdit
from PyQt5.QtCore import pyqtSignal
from pathlib import Path

import serial.tools.list_ports


_UI_PATH = Path(__file__).resolve().parent / "ui" / "terminal_ui.ui"

class TerminalWidget(QtWidgets.QWidget):
    _filters = []
    connect_pressed = pyqtSignal()
    send_pressed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        print(f"Loading UI from: {_UI_PATH}")
        uic.loadUi(_UI_PATH, self)   # loads into THIS widget

        self.btn_refresh_ports = self.findChild(QPushButton, "pushButton_3")
        self.btn_refresh_ports.clicked.connect(lambda: self.button_pressed(self.btn_refresh_ports))

        self.btn_connect = self.findChild(QPushButton, "pushButton_4")
        self.btn_connect.clicked.connect(lambda: self.button_pressed(self.btn_connect))

        self.btn_send = self.findChild(QPushButton, "pushButton")
        self.btn_send.clicked.connect(lambda: self.button_pressed(self.btn_send))

        self.btn_clear = self.findChild(QPushButton, "pushButton_2")
        self.btn_clear.clicked.connect(lambda: self.button_pressed(self.btn_clear))

        self.chkbx_auto_scroll = self.findChild(QtWidgets.QCheckBox, "checkBox")
        self.chkbx_auto_scroll.stateChanged.connect(lambda: self.checkbox_toggled(self.chkbx_auto_scroll))

        self.LE_baudrate = self.findChild(QLineEdit, "lineEdit_2")
        self.LE_baudrate.setText("115200")

        self.LE_input = self.findChild(QLineEdit, "lineEdit")
        self.LE_input.returnPressed.connect(lambda: self.button_pressed(self.btn_send))

        self.combobox_ports = self.findChild(QtWidgets.QComboBox, "comboBox")

        self.textedit_terminal = self.findChild(QPlainTextEdit, "plainTextEdit")

        # Initial population of ports
        self.button_pressed(self.btn_refresh_ports)

    def get_port(self):
        return self.combobox_ports.currentText()
    
    def set_port(self, port_str):
        index = self.combobox_ports.findText(port_str)
        if index >= 0:
            self.combobox_ports.setCurrentIndex(index)

    def get_baudrate(self):
        return int(self.LE_baudrate.text())
    
    def set_baudrate(self, baudrate):
        self.LE_baudrate.setText(str(baudrate))

    def add_filter(self, filter_str):
        self._filters.append(filter_str)

    def button_pressed(self, arg):
        txt = arg.text()

        print(f"Button pressed: {txt}")

        if txt == "Refresh":
            # Simulate refreshing ports
            self.combobox_ports.clear()
            ports = serial.tools.list_ports.comports()
            for port, desc, hwid in sorted(ports):
                # print(f"{port}: {desc} [{hwid}]")
                self.combobox_ports.addItem(port)

        elif txt == "Connect":
            self.connect_pressed.emit()

        elif txt == "Send":
            message = self.LE_input.text()
            self.append_text(message, direction="out")
            self.LE_input.clear()
            self.send_pressed.emit(message)

        elif txt == "Clear":
            self.textedit_terminal.clear()

    def checkbox_toggled(self, arg):
        print(f"Checkbox toggled: {arg.isChecked()}")

    def receive_message(self, message):
        if message not in self._filters:
            self.append_text(message, direction="in")

    def append_text(self, text, direction="in"):
        prefix = ">> " if direction == "out" else "<< "
        self.textedit_terminal.appendPlainText(prefix + text)

        if self.chkbx_auto_scroll.isChecked():
            self.textedit_terminal.verticalScrollBar().setValue(self.textedit_terminal.verticalScrollBar().maximum())