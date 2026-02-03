import time
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QScrollArea, QGroupBox, QLineEdit, QPlainTextEdit
from pathlib import Path

_UI_PATH = Path(__file__).resolve().parent / "ui" / "terminal_ui.ui"

class TerminalWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        print(f"Loading UI from: {_UI_PATH}")
        uic.loadUi(_UI_PATH, self)   # loads into THIS widget
