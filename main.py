import os
import sys
from typing import Self
import winreg
import pandas as pd
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout,
    QWidget, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QCheckBox, QLineEdit, QTabWidget, QFormLayout, QMessageBox, QGridLayout,
    QAbstractItemView, QInputDialog, QComboBox, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import win32com.client as win32
import math
import base64
import plotly.graph_objects as go
import plotly.io as pio
import webbrowser
from PyQt6.QtGui import QPixmap, QIcon, QAction
from PIL import Image
import io
import numpy as np
import lasio
import subprocess
import os
import pickle
import ctypes



class NewWellTech(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Well Technologies v1.0.0-Beta.0")
        self.setGeometry(0, 0, 1920, 1080)
        self.showMaximized()
        # Initialize your application here
        self.current_file = None
        self.data = None
        self.app_name = "New Well Technologies"
        self.app_file_path = "app_state.pkl"
        self.load_state()

        # Modern Spacey Style Theme
        self.setStyleSheet("""
        QMainWindow {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a); /* Dark Gray */
            color: #ffffff; /* White */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }

        QTabWidget::pane {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a); /* Dark Gray */
            border: none;
        }

        QTabBar::tab {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        QTabBar::tab:selected {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QTableWidget {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            border: 1px solid #3b3b3b; /* Darker Gray */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        QTableWidget::item {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 0px;
            border: none;
        }

        QTableWidget::item:selected {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QTableWidget::horizontalHeader {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            color: #ffffff; /* White */
            padding: 0px;
            border: none;
            font-size: 15pt;
            font-weight: bold;
            text-shadow: 0 0 0px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QTableWidget::verticalHeader {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            color: #ffffff; /* White */
            padding: 0px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QScrollBar:vertical {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            width: 10px;
            margin: 0px 0px 0px 0px;
        }

        QScrollBar::handle:vertical {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            min-height: 20px;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QScrollBar::add-line:vertical {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            height: 20px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }

        QScrollBar::sub-line:vertical {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            height: 20px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }

        QPushButton {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3498db, stop:1 #2ecc71); /* Gradient Blue to Green */
            color: #ffffff; /* White */
            border-radius: 10px;
            padding: 10px;
            font-size: 12pt;
            font-weight: bold;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QPushButton:hover {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2ecc71, stop:1 #3498db); /* Gradient Green to Blue */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QCheckBox {
            color: #3498db; /* White */
            font-size: 12pt;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QLineEdit {
            background-color: #3498db; /* Dark Gray */
            color: #ffffff; /* White */
            border: 1px solid #3b3b3b; /* Darker Gray */
            border-radius: 5px;
            padding: 5px;
            font-size: 12pt;
            font-weight: bold;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QLabel {
            color: #ffffff; /* White */
            font-size: 12pt;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }

        QMenuBar {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
        }

        QMenu {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
        }

        QMenu::item {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
        }

        QMenu::item:selected {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.5); /* Green Glow */
        }
        """)


        # Main container
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Well Info Tab
        self.well_info_tab = QWidget()
        self.well_info_tab.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a)")
        self.tabs.addTab(self.well_info_tab, "Well Info")

        # Survey Data Tab
        self.survey_tab = QWidget()
        self.survey_tab.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a)")
        self.tabs.addTab(self.survey_tab, "Survey Data")

        # Gamma Plot Tab
        self.gamma_plot_tab = QWidget()
        self.gamma_plot_tab.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a)")
        self.tabs.addTab(self.gamma_plot_tab, "Gamma Plot")

        # Distro List Tab
        self.distro_list_tab = QWidget()
        self.distro_list_tab.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a)")
        self.tabs.addTab(self.distro_list_tab, "Distro List")

        # Initialize
        self.init_survey_tab()
        self.init_well_info_tab()
        self.init_gamma_plot_tab()
        self.init_distro_list_tab()

        # File tracking
        self.current_file = None
        self.las_file = None
        self.folder_path = None
        self.last_modified_time = None
        self.last_las_modified_time = None

        # Data storage
        self.latest_survey_row = None
        self.plot_figure = None
        self.canvas = None
        self.latitude = None
        self.longitude = None

        # Timer to monitor file updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_file_updates)
        self.timer.start(5000) # Check every 5 seconds

        # Add logo to title bar
        self.setWindowIcon(QIcon("D:/VS_Practice_Code/AI_Parsing_Logic_MWD/LOGO_1.png"))

        # Create menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)

        # Create file menu
        self.file_menu = QMenu("File")
        self.menu_bar.addMenu(self.file_menu)

        # Create new action
        self.new_action = QAction("New")
        self.new_action.triggered.connect(self.new_window)
        self.file_menu.addAction(self.new_action)

        # Create open action
        self.open_action = QAction("Open")
        self.open_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_action)

        # Create load action
        self.load_action = QAction("Load")
        self.load_action.triggered.connect(self.load_state_from_file)
        self.file_menu.addAction(self.load_action)

        # Create save action
        self.save_action = QAction("Save")
        self.save_action.triggered.connect(self.save_file)
        self.file_menu.addAction(self.save_action)

    def init_survey_tab(self):
        layout = QVBoxLayout()

        # Button Container
        button_layout = QHBoxLayout()
        select_file_btn = QPushButton("Select Survey File")
        select_file_btn.clicked.connect(self.select_survey_file)
        select_file_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        button_layout.addWidget(select_file_btn)

        select_folder_btn = QPushButton("Select Folder")
        select_folder_btn.clicked.connect(self.select_folder)
        select_folder_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        button_layout.addWidget(select_folder_btn)

        self.upload_las_btn = QPushButton("Upload LAS File")
        self.upload_las_btn.clicked.connect(self.upload_las_file)
        self.upload_las_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        button_layout.addWidget(self.upload_las_btn)

        email_btn = QPushButton("Open Email Draft")
        email_btn.clicked.connect(self.open_email_draft)
        email_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        button_layout.addWidget(email_btn)

        layout.addLayout(button_layout)

        # Curve, Bit Depth, and Survey Table Container
        curve_bit_depth_survey_layout = QHBoxLayout()

        # Curve Input Section
        curve_layout = QGridLayout()
        self.inputs = {}
        curve_fields = ["MY", "DLN", "PTB INC", "PTB AZ", "PTB A/B", "PTB L/R"]
        for i, field in enumerate(curve_fields):
            input_container = QWidget()
            input_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
            input_layout = QVBoxLayout()
            input_layout.addWidget(QLabel(field))
            self.inputs[field] = QLineEdit()
            self.inputs[field].setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
            self.inputs[field].setFixedWidth(100) # Half-width
            input_layout.addWidget(self.inputs[field])
            input_container.setLayout(input_layout)
            curve_layout.addWidget(input_container, i, 0, 1, 2)

        curve_section = QWidget()
        curve_section.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        curve_section.setLayout(curve_layout)
        curve_section.setFixedWidth(300)
        curve_bit_depth_survey_layout.addWidget(curve_section)

        # Bit Depth Section
        bit_depth_layout = QVBoxLayout()
        bit_depth_label_container = QWidget()
        bit_depth_label_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        bit_depth_label_layout = QVBoxLayout()
        self.bit_depth_label = QLabel("Bit Depth:")
        bit_depth_label_layout.addWidget(self.bit_depth_label)
        bit_depth_label_container.setLayout(bit_depth_label_layout)

        bit_depth_value_container = QWidget()
        bit_depth_value_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        bit_depth_value_layout = QVBoxLayout()
        self.bit_depth_value = QLabel("N/A")
        self.bit_depth_value.setStyleSheet("color: #00ff00; font-size: 12pt; font-weight: bold")
        bit_depth_value_layout.addWidget(self.bit_depth_value)
        bit_depth_value_container.setLayout(bit_depth_value_layout)

        inclination_value_container = QWidget()
        inclination_value_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        inclination_value_layout = QVBoxLayout()
        self.inclination_value = QLabel("N/A")
        self.inclination_value.setStyleSheet("color: #00ff00; font-size: 12pt; font-weight: bold")
        inclination_value_layout.addWidget(self.inclination_value)
        inclination_value_container.setLayout(inclination_value_layout)

        azimuth_value_container = QWidget()
        azimuth_value_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        azimuth_value_layout = QVBoxLayout()
        self.azimuth_value = QLabel("N/A")
        self.azimuth_value.setStyleSheet("color: #00ff00; font-size: 12pt; font-weight: bold")
        azimuth_value_layout.addWidget(self.azimuth_value)
        azimuth_value_container.setLayout(azimuth_value_layout)

        ab_value_container = QWidget()
        ab_value_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        ab_value_layout = QVBoxLayout()
        self.ab_label = QLabel("A/B:")
        ab_value_layout.addWidget(self.ab_label)
        self.ab_value = QLineEdit()
        self.ab_value.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        ab_value_layout.addWidget(self.ab_value)
        ab_value_container.setLayout(ab_value_layout)

        lr_value_container = QWidget()
        lr_value_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        lr_value_layout = QVBoxLayout()
        self.lr_label = QLabel("L/R:")
        lr_value_layout.addWidget(self.lr_label)
        self.lr_value = QLineEdit()
        self.lr_value.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        lr_value_layout.addWidget(self.lr_value)
        lr_value_container.setLayout(lr_value_layout)

        bit_depth_layout.addWidget(bit_depth_label_container)
        bit_depth_layout.addWidget(bit_depth_value_container)
        bit_depth_layout.addWidget(inclination_value_container)
        bit_depth_layout.addWidget(azimuth_value_container)
        bit_depth_layout.addWidget(ab_value_container)
        bit_depth_layout.addWidget(lr_value_container)

        # Define checkboxes
        self.include_curve_checkbox = QCheckBox("Include Curve Data")
        self.include_curve_checkbox.setStyleSheet("color: #ffffff; font-size: 12pt; font-weight: bold")
        bit_depth_layout.addWidget(self.include_curve_checkbox)

        self.include_bit_depth_checkbox = QCheckBox("Include Bit Depth Data")
        self.include_bit_depth_checkbox.setStyleSheet("color: #ffffff; font-size: 12pt; font-weight: bold")
        self.include_bit_depth_checkbox.setChecked(True)
        bit_depth_layout.addWidget(self.include_bit_depth_checkbox)

        self.auto_open_email_checkbox = QCheckBox("Auto Open Email Draft")
        self.auto_open_email_checkbox.setStyleSheet("color: #ffffff; font-size: 12pt; font-weight: bold")
        self.auto_open_email_checkbox.setChecked(True)
        bit_depth_layout.addWidget(self.auto_open_email_checkbox)

        bit_depth_section = QWidget()
        bit_depth_section.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); border: 1px solid #3b3b3b; border-radius: 10px; padding: 0px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        bit_depth_section.setLayout(bit_depth_layout)
        bit_depth_section.setFixedWidth(300)
        curve_bit_depth_survey_layout.addWidget(bit_depth_section)

        # Survey Table
        self.survey_table = QTableWidget()
        self.survey_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.survey_table.setStyleSheet("""
        QTableWidget {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            border: 1px solid #3b3b3b; /* Darker Gray */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        QTableWidget::item {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 0px;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
        }
        QTableWidget::horizontalHeader {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            color: #ffffff; /* White */
            padding: 0px;
            border: none;
            font-size: 15pt;
            font-weight: bold;
        }
        QTableWidget::verticalHeader {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            color: #ffffff; /* White */
            padding: 0px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
        }
        """)
        self.survey_table.horizontalHeader().setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); color: #6b6b6b; padding: 0px; border: 10px; font-size: 12pt; font-weight: bold")
        self.survey_table.verticalHeader().setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); color: #6b6b6b; padding: 0px; border: 10px; font-size: 12pt; font-weight: bold")
        curve_bit_depth_survey_layout.addWidget(self.survey_table)

        layout.addLayout(curve_bit_depth_survey_layout)

        self.survey_tab.setLayout(layout)

    def init_well_info_tab(self):
        layout = QFormLayout()
        self.well_name_input = QLineEdit()
        self.well_name_input.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        self.well_name_input.textChanged.connect(self.update_well_name)
        layout.addRow(QLabel("Well Name:"), self.well_name_input)

        self.rig_name_input = QLineEdit()
        self.rig_name_input.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        self.rig_name_input.textChanged.connect(self.update_rig_name)
        layout.addRow(QLabel("Rig Name:"), self.rig_name_input)

        self.sensor_offset_input = QLineEdit()
        self.sensor_offset_input.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        self.sensor_offset_input.textChanged.connect(self.update_sensor_offset)
        layout.addRow(QLabel("Sensor Offset:"), self.sensor_offset_input)

        self.logo_combo = QComboBox()
        self.logo_combo.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")

        logos_dir = "D:/VS_Practice_Code/AI_Parsing_Logic_MWD"
        self.logo_files = []
        for file in os.listdir(logos_dir):
            if file.endswith(".png"):
                self.logo_files.append(file)
                self.logo_combo.addItem(os.path.splitext(file)[0])  # Store the file name without extension

        layout.addRow(QLabel("Logo:"), self.logo_combo)
        self.well_info_tab.setLayout(layout)

        # Add well name and rig name labels to the top of the application
        self.well_name_label = QLabel("Well Name: ")
        self.well_name_label.setStyleSheet("color: #ff69b4; font-size: 18pt; font-weight: bold")
        self.rig_name_label = QLabel("Rig Name: ")
        self.rig_name_label.setStyleSheet("color: #ff69b4; font-size: 18pt; font-weight: bold")
        self.status_bar = self.statusBar()
        self.status_bar.addPermanentWidget(self.well_name_label)
        self.status_bar.addPermanentWidget(self.rig_name_label)

    def update_well_name(self):
        self.well_name_label.setText(f"Well Name: {self.well_name_input.text()}")

    def update_rig_name(self):
        self.rig_name_label.setText(f"Rig Name: {self.rig_name_input.text()}")

    def update_sensor_offset(self):
        try:
            offset = float(self.sensor_offset_input.text())
            if self.latest_survey_row is not None:
                md = self.latest_survey_row.iloc[0]
                if isinstance(md, str):
                    try:
                        md = float(md)
                    except ValueError:
                        md = 0
                self.bit_depth_value.setText(f"{md + offset:.2f}")
            else:
                self.bit_depth_value.setText("N/A")
        except ValueError:
            pass


    def init_gamma_plot_tab(self):
        layout = QVBoxLayout()
        self.gamma_plot_container = QWidget()
        self.gamma_plot_container.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1d23, stop:1 #2f343a)")
        self.gamma_plot_layout = QVBoxLayout(self.gamma_plot_container)
        layout.addWidget(self.gamma_plot_container)

        self.last_values_label = QLabel("Last Values:")
        self.last_values_label.setStyleSheet("color: #ffffff; font-size: 12pt; font-weight: bold")
        layout.addWidget(self.last_values_label)

        self.gamma_plot_tab.setLayout(layout)

    def init_distro_list_tab(self):
        layout = QVBoxLayout()
        self.distro_list_table = QTableWidget()
        self.distro_list_table.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.distro_list_table.setStyleSheet("""
        QTableWidget {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            border: 1px solid #3b3b3b; /* Darker Gray */
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        QTableWidget::item {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #3b3b3b, stop:1 #5b5b5b); /* Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
        }
        QTableWidget::item:selected {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
        }
        QTableWidget::horizontalHeader {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
        }
        QTableWidget::verticalHeader {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); /* Even Darker Gray */
            color: #ffffff; /* White */
            padding: 10px;
            border: none;
            font-size: 12pt;
            font-weight: bold;
        }
        """)
        self.distro_list_table.horizontalHeader().setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); color: #ffffff; padding: 10px; border: none; font-size: 12pt; font-weight: bold")
        self.distro_list_table.verticalHeader().setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #4b4b4b, stop:1 #6b6b6b); color: #ffffff; padding: 10px; border: none; font-size: 12pt; font-weight: bold")
        layout.addWidget(self.distro_list_table)

        self.distro_list_name_input = QLineEdit()
        self.distro_list_name_input.setStyleSheet("background-color: #2f343a; color: #ffffff; border: 1px solid #3b3b3b; border-radius: 5px; padding: 5px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        self.distro_list_name_input.setPlaceholderText("Enter Distro List Name")
        layout.addWidget(self.distro_list_name_input)

        save_template_btn = QPushButton("Save Template as Excel")
        save_template_btn.clicked.connect(self.save_template_as_excel)
        save_template_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        layout.addWidget(save_template_btn)

        import_template_btn = QPushButton("Import Excel Template")
        import_template_btn.clicked.connect(self.import_excel_template)
        import_template_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        layout.addWidget(import_template_btn)

        create_distro_list_btn = QPushButton("Create Distro List")
        create_distro_list_btn.clicked.connect(self.create_distro_list)
        create_distro_list_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        layout.addWidget(create_distro_list_btn)

        add_email_btn = QPushButton("Add Email to Distro List")
        add_email_btn.clicked.connect(self.add_email_to_distro_list)
        add_email_btn.setStyleSheet("background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #6c5ce7, stop:1 #5c51a6); color: #ffffff; border-radius: 10px; padding: 10px; font-size: 12pt; font-weight: bold; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)")
        layout.addWidget(add_email_btn)

        self.distro_list_tab.setLayout(layout)


    def select_survey_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Survey File", "", "Files (*.xlsx *.xls *.csv *.txt)"
        )
        if file_path:
            self.current_file = file_path
            self.last_modified_time = os.path.getmtime(file_path)
            self.parse_survey_file()

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder

    def parse_survey_file(self):
        try:
            if self.current_file.endswith(".csv") or self.current_file.endswith(".txt"):
                df = pd.read_csv(self.current_file)
            else:
                df = pd.read_excel(self.current_file)

            # Advanced NLP Parsing: Find row containing headers
            keywords_md = ["MD", "Measured Depth", "SD"]
            keywords_inc = ["INC", "Inclination", "Inc"]
            keywords_az = ["AZ", "AZM", "Azimuth", "AZI"]
            keywords_lat = ["LAT", "Latitude", "°"]
            keywords_lon = ["LON", "Longitude", "°"]

            header_row_idx = next(
                (idx for idx, row in df.iterrows() if any(str(cell).strip() in keywords_md for cell in row)), None
            )

            if header_row_idx is not None:
                df.columns = df.iloc[header_row_idx]
                df = df.iloc[header_row_idx + 1:].reset_index(drop=True)

            # Filter out columns before MD
            md_col_idx = next((i for i, col in enumerate(df.columns) if any(keyword in col for keyword in keywords_md)), None)
            if md_col_idx is not None:
                df = df.iloc[:, md_col_idx:]

            # Extract latitude and longitude
            lat_col_idx = next((i for i, col in enumerate(df.columns) if any(keyword in col for keyword in keywords_lat)), None)
            lon_col_idx = next((i for i, col in enumerate(df.columns) if any(keyword in col for keyword in keywords_lon)), None)
            if lat_col_idx is not None and lon_col_idx is not None:
                self.latitude = df.iloc[-1, lat_col_idx]
                self.longitude = df.iloc[-1, lon_col_idx]

            self.populate_table(df)

            # Extract latest row values
            self.latest_survey_row = df.iloc[-1] if not df.empty else None
            if self.latest_survey_row is not None:
                md = self.latest_survey_row.iloc[0]
                if isinstance(md, str):
                    try:
                        md = float(md)
                    except ValueError:
                        md = 0
                offset = float(self.sensor_offset_input.text() or 0)
                self.bit_depth_value.setText(f"{md + offset:.2f}")

                # Find inclination and azimuth
                inc = self.latest_survey_row.iloc[1]
                if isinstance(inc, str):
                    try:
                        inc = float(inc)
                    except ValueError:
                        inc = 0
                az = self.latest_survey_row.iloc[2]
                if isinstance(az, str):
                    try:
                        az = float(az)
                    except ValueError:
                        az = 0

                self.inclination_value.setText(str(inc))
                self.azimuth_value.setText(str(az))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to parse file: {e}")

    def populate_table(self, df):
        self.survey_table.setRowCount(0)
        self.survey_table.setColumnCount(len(df.columns))
        self.survey_table.setHorizontalHeaderLabels(df.columns)

        for row_idx, row_data in df.iterrows():
            self.survey_table.insertRow(row_idx)
            for col_idx, cell_data in enumerate(row_data):
                self.survey_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))

    def check_file_updates(self):
        if self.current_file and os.path.exists(self.current_file):
            modified_time = os.path.getmtime(self.current_file)
            if modified_time != self.last_modified_time:
                self.last_modified_time = modified_time
                self.parse_survey_file()
                if self.auto_open_email_checkbox.isChecked():
                    self.open_email_draft()

        if self.las_file and os.path.exists(self.las_file):
            modified_time = os.path.getmtime(self.las_file)
            if modified_time != self.last_las_modified_time:
                self.last_las_modified_time = modified_time
                self.upload_las_file()
                if self.auto_open_email_checkbox.isChecked():
                    self.open_email_draft()

    def upload_las_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select LAS File", "", "LAS Files (*.las)")
        if file_path:
            self.las_file = file_path
            self.last_las_modified_time = os.path.getmtime(file_path)
            try:
                las = lasio.read(self.las_file)
                depth = las["DEPT"]
                gamma_columns = [col for col in las.curves if any(keyword in col.mnemonic.upper() for keyword in ["GR", "GR_LWD", "GAMMA RAY", "GAMMA"])]
                if not gamma_columns:
                    raise ValueError("No gamma column found in LAS file.")
                gamma = las[gamma_columns[0].mnemonic]
                df = pd.DataFrame({"Depth (ft)": depth, "Gamma": gamma})
                df = df.dropna(subset=["Gamma"])
                last_100ft = df[df["Depth (ft)"] >= df["Depth (ft)"].max() - 100]
                if self.plot_figure is None:
                    self.plot_figure = plt.figure()
                    self.canvas = FigureCanvas(self.plot_figure)
                    self.gamma_plot_layout.addWidget(self.canvas)
                plt.clf()
                plt.style.use('dark_background')
                frames = []
                for i in range(1, len(last_100ft) + 1):
                    plt.plot(last_100ft["Gamma"][:i], last_100ft["Depth (ft)"][:i], color='green')
                    plt.xlabel("Gamma")
                    plt.ylabel("Depth (ft)")
                    plt.title("Gamma Plot")
                    plt.gca().invert_yaxis()
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight')
                    buf.seek(0)
                    image = Image.open(buf).convert("RGBA")
                    frames.append(image)
                    buf.close()
                    plt.close()
                gif_buffer = io.BytesIO()
                frames[0].save(gif_buffer, format="GIF", save_all=True, append_images=frames[1:], duration=200, loop=0)
                gif_buffer.seek(0)
                gif_data = gif_buffer.read()
                with open("gamma_plot.gif", "wb") as f:
                    f.write(gif_data)
                self.canvas.draw()
                last_values = f"Last Values: Depth {last_100ft['Depth (ft)'].iloc[-1]:.2f}, Gamma {last_100ft['Gamma'].iloc[-1]:.2f}"
                self.last_values_label.setText(last_values)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to parse LAS file: {e}")


    def open_email_draft(self):
        try:
            outlook = win32.Dispatch('Outlook.Application')
            mail = outlook.CreateItem(0)

            # Subject
            subject = f"{self.rig_name_input.text()} - {self.well_name_input.text()} - "
            if self.latest_survey_row is not None:
                subject += " | ".join(self.latest_survey_row.astype(str))
            mail.Subject = subject

            # Start Email Body
            body = f"""
            <html>
            <body style="font-family: Arial; font-size: 12pt; background-color: #f7f7f7;">
            <div style="background-color: #f7f7f7; padding: 20px; border: 1px solid #cccccc; border-radius: 10px; 
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <img src="file:///{os.path.abspath(self.logo_files[self.logo_combo.currentIndex()])}" 
            alt="Logo" style="width: 50px; height: auto; float: left; margin-right: 10px">
            <h2 style="color: #333333; text-align: center; font-weight: bold; font-size: 18pt;">
            New Well Survey Report</h2>
            <hr style="border: 1px solid #cccccc; margin-top: 10px; margin-bottom: 10px;">
            <p style="color: #666666; font-size: 14pt;">Well Name: {self.well_name_input.text()}</p>
            <p style="color: #666666; font-size: 14pt;">Rig Name: {self.rig_name_input.text()}</p>
            """

            # Latest Survey Data Table
            if self.latest_survey_row is not None:
                body += """
                <h3 style="color: #333333; font-weight: bold; font-size: 16pt;">Latest Survey Data:</h3>
                <table style="border-collapse: collapse; width: 100%; margin-top: 10px;">
                <tr style="background-color: #f2f2f2; border-bottom: 1px solid #cccccc;">
                <th style="padding: 10px; border-right: 1px solid #cccccc;">Parameter</th>
                <th style="padding: 10px;">Value</th>
                </tr>
                """
                for i, (col, val) in enumerate(self.latest_survey_row.items()):
                    body += f"""
                    <tr style="background-color: {'#f2f2f2' if i % 2 == 0 else '#ffffff'}; border-bottom: 1px solid #cccccc;">
                    <td style="padding: 10px; border-right: 1px solid #cccccc;">{col}</td>
                    <td style="padding: 10px;">{val}</td>
                    </tr>
                    """
                body += "</table>"

            # Curve Data
            if self.include_curve_checkbox.isChecked():
                body += """
                <h3 style="color: #333333; font-weight: bold; font-size: 16pt;">Curve Data:</h3>
                <table style="border-collapse: collapse; width: 100%; margin-top: 10px;">
                <tr style="background-color: #f2f2f2; border-bottom: 1px solid #cccccc;">
                <th style="padding: 10px; border-right: 1px solid #cccccc;">Field</th>
                <th style="padding: 10px;">Value</th>
                </tr>
                """
                for i, (field, input_box) in enumerate(self.inputs.items()):
                    body += f"""
                    <tr style="background-color: {'#f2f2f2' if i % 2 == 0 else '#ffffff'}; border-bottom: 1px solid #cccccc;">
                    <td style="padding: 10px; border-right: 1px solid #cccccc;">{field}</td>
                    <td style="padding: 10px;">{input_box.text()}</td>
                    </tr>
                    """
                body += "</table>"

            # Bit Depth Section
            if self.include_bit_depth_checkbox.isChecked():
                body += f"""
                <h3 style="color: #333333; font-weight: bold; font-size: 16pt;">Bit Depth:</h3>
                <div style="background-color: #f2f2f2; padding: 10px; border: 1px solid #cccccc; border-radius: 10px;">
                <p>Bit Depth: {self.bit_depth_value.text()}</p>
                <p>Inclination: {self.inclination_value.text()}</p>
                <p>Azimuth: {self.azimuth_value.text()}</p>
                <p>A/B: {self.ab_value.text()}</p>
                <p>L/R: {self.lr_value.text()}</p>
                </div>
                """

            # Attachments
            if os.path.exists("gamma_plot.gif"):
                with open("gamma_plot.gif", "rb") as image_file:
                    encoded_image = base64.b64encode(image_file.read()).decode()
                body += f"""
                <h3 style="color: #333333; font-weight: bold; font-size: 16pt;">Gamma Plot:</h3>
                <img src="data:image/gif;base64,{encoded_image}" alt="Gamma Plot" style="width: 100%; height: auto;">
                """
                   # Function to convert DMS to Decimal Degrees
            def dms_to_decimal(degrees, minutes, seconds, direction):
                decimal = degrees + (minutes / 60) + (seconds / 3600)
                # Adjust for direction
                if direction in ['S', 'W']:  # Negative for South or West
                    decimal = -decimal
                return decimal

            # Google Maps Link
            if self.survey_table.rowCount() > 0:
                lat_item = self.survey_table.item(1, 15)  # Latitude column
                lon_item = self.survey_table.item(1, 16)  # Longitude column
                
                if lat_item and lon_item and lat_item.text().strip() and lon_item.text().strip():
                    latitude_dms = lat_item.text().strip()  # Example: "32° 12' 5.013" N"
                    longitude_dms = lon_item.text().strip()  # Example: "102° 4' 7.887" W"
                    
                    # Parse DMS values for latitude
                    lat_deg, lat_min, lat_sec, lat_dir = latitude_dms.replace('°','').replace("'","").replace('"', "").split()  # e.g. ["32", "12", "5.013", "N"]
                    lat_deg, lat_min, lat_sec = float(lat_deg), float(lat_min), float(lat_sec)
                    
                    # Parse DMS values for longitude
                    lon_deg, lon_min, lon_sec, lon_dir = longitude_dms.replace('°','').replace("'","").replace('"', "").split()  # e.g. ["102", "4", "7.887", "W"]
                    lon_deg, lon_min, lon_sec = float(lon_deg), float(lon_min), float(lon_sec)
                    
                    # Convert to decimal degrees
                    latitude = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
                    longitude = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)
                    
                    # Merge latitude and longitude with a comma in between
                    coordinates = f"{latitude},{longitude}"
                    
                    # Ensure both latitude and longitude are included in the link for Google Maps
                    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={coordinates}"
                    
                    body += f"""
                    <h3 style="color: #333333; font-weight: bold; font-size: 16pt;">🗺 Directions to the Rig:</h3>
                    <p>Coordinates: {latitude_dms},{longitude_dms}</p>
                    <a href="{google_maps_link}" target="_blank" 
                    style="color: #1a73e8; text-decoration: none; font-size: 14pt;">
                    View on Google Maps</a>
                    """

            body += "</div></body></html>"

            mail.BodyFormat = 2  # HTML format
            mail.HTMLBody = body

            # To and CC Emails
            to_emails = [self.distro_list_table.item(row, 1).text() for row in range(self.distro_list_table.rowCount())
                        if self.distro_list_table.item(row, 1)]
            mail.To = ";".join(to_emails)
            mail.CC = ";".join(to_emails)  # Adjust if CC is separate

            mail.Display()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open email draft: {e}")


    def save_template_as_excel(self):
        try:
            df = pd.DataFrame({
                "Name": [],
                "Email": []
            })
            df.to_excel("distro_list_template.xlsx", index=False)
            QMessageBox.information(self, "Success", "Template saved as distro_list_template.xlsx")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save template: {e}")

    def import_excel_template(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel Template", "", "Excel Files (*.xlsx)")
            if file_path:
                df = pd.read_excel(file_path)
                self.distro_list_table.setRowCount(0)
                self.distro_list_table.setColumnCount(len(df.columns))
                self.distro_list_table.setHorizontalHeaderLabels(df.columns)
                for row_idx, row_data in df.iterrows():
                    self.distro_list_table.insertRow(row_idx)
                    for col_idx, cell_data in enumerate(row_data):
                        self.distro_list_table.setItem(row_idx, col_idx, QTableWidgetItem(str(cell_data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import template: {e}")

    def create_distro_list(self):
        try:
            df = pd.DataFrame({
                "Name": [],
                "Email": []
            })
            for row in range(self.distro_list_table.rowCount()):
                name = self.distro_list_table.item(row, 0).text()
                email = self.distro_list_table.item(row, 1).text()
                df = pd.concat([df, pd.DataFrame({"Name": [name], "Email": [email]})], ignore_index=True)
            distro_list_name = self.distro_list_name_input.text()
            if distro_list_name:
                df.to_excel(f"{distro_list_name}.xlsx", index=False)
                QMessageBox.information(self, "Success", f"Distro list saved as {distro_list_name}.xlsx")
            else:
                QMessageBox.critical(self, "Error", "Please enter a name for the distro list")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create distro list: {e}")

    def add_email_to_distro_list(self):
        try:
            name, ok = QInputDialog.getText(self, "Add Email", "Enter Name:")
            if ok:
                email, ok = QInputDialog.getText(self, "Add Email", "Enter Email:")
                if ok:
                    self.distro_list_table.setRowCount(self.distro_list_table.rowCount() + 1)
                    self.distro_list_table.setItem(self.distro_list_table.rowCount() - 1, 0, QTableWidgetItem(name))
                    self.distro_list_table.setItem(self.distro_list_table.rowCount() - 1, 1, QTableWidgetItem(email))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to add email to distro list: {e}")

    def new_window(self):
        # Get the current script path
        script_path = os.path.abspath(__file__)

        # Run a new instance of the application
        subprocess.Popen([sys.executable, script_path])

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "Files (*.xlsx *.xls *.csv *.txt)")
        if file_path:
            self.current_file = file_path
            self.parse_survey_file()

    def save_file(self):
        # Ask the user for the application name and file path
        self.app_name, ok = QFileDialog.getSaveFileName(self, "Save Application", "", "Pickle Files (*.pkl)")
        if ok:
            self.app_file_path = self.app_name
            # Save the current state of the application
            with open(self.app_file_path, "wb") as f:
                pickle.dump({
                    "current_file": self.current_file,
                    "data": self.data,
                    "well_name": self.well_name_input.text(),
                    "rig_name": self.rig_name_input.text(),
                    "sensor_offset": self.sensor_offset_input.text(),
                    "logo": self.logo_combo.currentText(),
                    "distro_list": [[self.distro_list_table.item(row, 0).text(), self.distro_list_table.item(row, 1).text()] for row in range(self.distro_list_table.rowCount())]
                }, f)
            QMessageBox.information(self, "Application Saved", "Application has been saved successfully.")



    def load_state_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Saved Application", "", "All Files (*)")
        if file_path:
            try:
                # Validate file format (e.g., check extension or use a file type detection library)
                if not file_path.endswith(('.pkl', '.pickle')):
                    raise ValueError("Invalid file format. Only .pkl and .pickle files are supported.")

                with open(file_path, "rb") as f:
                    state = pickle.load(f)
                    self.current_file = state.get("current_file", None)
                    self.data = state.get("data", None)
                    self.well_name_input.setText(state.get("well_name", ""))
                    self.rig_name_input.setText(state.get("rig_name", ""))
                    self.sensor_offset_input.setText(state.get("sensor_offset", ""))
                    self.logo_combo.setCurrentText(state.get("logo", ""))
                    self.distro_list_table.setRowCount(0)
                    for row in state.get("distro_list", []):
                        self.distro_list_table.insertRow(self.distro_list_table.rowCount())
                        self.distro_list_table.setItem(self.distro_list_table.rowCount() - 1, 0, QTableWidgetItem(row[0]))
                        self.distro_list_table.setItem(self.distro_list_table.rowCount() - 1, 1, QTableWidgetItem(row[1]))
                    if self.current_file and os.path.exists(self.current_file):
                        try:
                            self.parse_survey_file()
                        except Exception as e:
                            print(f"Error parsing survey file: {e}")
                            QMessageBox.critical(self, "Error", f"Failed to parse survey file: {e}")
                QMessageBox.information(self, "Application Loaded", "Application has been loaded successfully.")
            except pickle.UnpicklingError:
                QMessageBox.critical(self, "Error", "Invalid file format")
            except ValueError as e:
                QMessageBox.critical(self, "Error", f"Failed to load state: {e}")
            except Exception as e:
                print(f"Error loading state: {e}")
                QMessageBox.critical(self, "Error", f"Failed to load state: {e}")



    def load_state(self):
        # Load the saved state of the application
        if os.path.exists(self.app_file_path) and os.path.getsize(self.app_file_path) > 0:
            try:
                with open(self.app_file_path, "rb") as f:
                    state = pickle.load(f)
                    self.current_file = state["current_file"]
                    self.data = state["data"]
                    self.well_name_input.setText(state.get("well_name", ""))
                    self.rig_name_input.setText(state.get("rig_name", ""))
                    self.sensor_offset_input.setText(state.get("sensor_offset", ""))
                    self.logo_combo.setCurrentText(state.get("logo", ""))
                    self.distro_list_table.setRowCount(0)
                    for row in state.get("distro_list", []):
                        self.distro_list_table.insertRow(self.distro_list_table.rowCount())
                        self.distro_list_table.setItem(self.distro_list_table.rowCount() - 1, 0, QTableWidgetItem(row[0]))
                        self.distro_list_table.setItem(self.distro_list_table.rowCount() - 1, 1, QTableWidgetItem(row[1]))
                    self.parse_survey_file()
            except Exception as e:
                print(f"Error loading state: {e}")
        else:
            pass



if __name__ == "__main__":
    app = QApplication([])
    window = NewWellTech()
    window.showMaximized()
    app.exec()

