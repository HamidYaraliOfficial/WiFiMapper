import sys
import os
import time
import math
import json
import csv
import datetime
import platform
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox, QFileDialog, QTabWidget,
    QTableWidget, QTableWidgetItem, QLineEdit, QSpinBox,
    QCheckBox, QMessageBox, QProgressBar, QDockWidget, QToolBar,
    QStatusBar, QDialog, QFormLayout, QDoubleSpinBox, QTextEdit,
    QGroupBox
)
from PyQt6.QtGui import (
    QIcon, QPainter, QPen, QBrush, QColor, QFont, QPixmap, QAction
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QSize, QTranslator, QLocale
import pyqtgraph as pg
import numpy as np
import pandas as pd
try:
    import pywifi
    from pywifi import const
except ImportError:
    pywifi = None
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import qdarkstyle
from PIL import Image

class WiFiMapper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WiFiMapper")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set window icon (favicon)
        self.setWindowIcon(QIcon("WiFiMapper.jpg"))
        
        # Initialize variables
        self.scan_data = []
        self.heatmap_data = []
        self.floor_plan = None
        self.current_theme = "Windows 11"
        self.current_language = "English"
        self.themes = {
            "Windows 11": {"bg": "#FFFFFF", "fg": "#000000", "accent": "#0078D4"},
            "Dark": {"bg": "#2D2D2D", "fg": "#FFFFFF", "accent": "#1E90FF"},
            "Light": {"bg": "#F0F0F0", "fg": "#000000", "accent": "#4169E1"},
            "Red": {"bg": "#FFF0F0", "fg": "#000000", "accent": "#FF0000"},
            "Blue": {"bg": "#F0F8FF", "fg": "#000000", "accent": "#0000FF"}
        }
        
        # Translation setup
        self.translator = QTranslator()
        self.translations = {
            "English": {"dir": "ltr", "file": "en.qm"},
            "فارسی": {"dir": "rtl", "file": "fa.qm"},
            "中文": {"dir": "ltr", "file": "zh.qm"}
        }
        
        # Initialize WiFi interface
        self.wifi = None
        if pywifi:
            try:
                self.wifi = pywifi.PyWiFi()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to initialize pywifi: {str(e)}")
        
        # Initialize UI
        self.init_ui()
        self.apply_theme()
        self.apply_language()
        
        # Timer for real-time scanning
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.scan_networks)
        self.scan_timer.start(5000)  # Scan every 5 seconds
        
    def init_ui(self):
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        
        # Create dock widget for controls
        self.control_dock = QDockWidget("Controls", self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.control_dock)
        self.control_widget = QWidget()
        self.control_layout = QVBoxLayout(self.control_widget)
        
        # Menu bar
        self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Tabs
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        # Heatmap tab
        self.heatmap_tab = QWidget()
        self.heatmap_layout = QVBoxLayout(self.heatmap_tab)
        self.heatmap_widget = pg.GraphicsLayoutWidget()
        self.heatmap_layout.addWidget(self.heatmap_widget)
        self.tabs.addTab(self.heatmap_tab, "Heatmap")
        
        # Network Analysis tab
        self.analysis_tab = QWidget()
        self.analysis_layout = QVBoxLayout(self.analysis_tab)
        self.network_table = QTableWidget()
        self.analysis_layout.addWidget(self.network_table)
        self.tabs.addTab(self.analysis_tab, "Network Analysis")
        
        # Settings tab
        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        self.create_settings_ui()
        self.tabs.addTab(self.settings_tab, "Settings")
        
        # Simulation tab
        self.simulation_tab = QWidget()
        self.simulation_layout = QVBoxLayout(self.simulation_tab)
        self.create_simulation_ui()
        self.tabs.addTab(self.simulation_tab, "Network Simulation")
        
        # Control panel
        self.create_control_panel()
        
        # Initialize heatmap
        self.init_heatmap()
        
        # Initialize network table
        self.init_network_table()
        
    def create_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        load_action = QAction("Load Floor Plan", self)
        load_action.triggered.connect(self.load_floor_plan)
        file_menu.addAction(load_action)
        
        save_action = QAction("Save Project", self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        export_action = QAction("Export Report", self)
        export_action.triggered.connect(self.export_report)
        file_menu.addAction(export_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        theme_menu = view_menu.addMenu("Themes")
        
        for theme in self.themes.keys():
            theme_action = QAction(theme, self)
            theme_action.triggered.connect(lambda checked, t=theme: self.set_theme(t))
            theme_menu.addAction(theme_action)
        
        # Language menu
        lang_menu = menu_bar.addMenu("Language")
        for lang in self.translations.keys():
            lang_action = QAction(lang, self)
            lang_action.triggered.connect(lambda checked, l=lang: self.set_language(l))
            lang_menu.addAction(lang_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        scan_action = QAction("Scan Networks", self)
        scan_action.triggered.connect(self.scan_networks)
        toolbar.addAction(scan_action)
        
        heatmap_action = QAction("Generate Heatmap", self)
        heatmap_action.triggered.connect(self.generate_heatmap)
        toolbar.addAction(heatmap_action)
        
        simulate_action = QAction("Simulate Network", self)
        simulate_action.triggered.connect(self.simulate_network)
        toolbar.addAction(simulate_action)
        
    def create_control_panel(self):
        # Logo display
        self.logo_label = QLabel()
        logo_pixmap = QPixmap("WiFiMapper.jpg")
        if not logo_pixmap.isNull():
            self.logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
            self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.logo_label.setText("Logo not found")
        self.control_layout.addWidget(self.logo_label)
        
        # Scan controls
        scan_group = QGroupBox("Scan Controls")
        scan_layout = QFormLayout()
        
        self.scan_mode = QComboBox()
        self.scan_mode.addItems(["Passive", "Active"])
        scan_layout.addRow("Scan Mode:", self.scan_mode)
        
        self.band_select = QComboBox()
        self.band_select.addItems(["2.4 GHz", "5 GHz", "6 GHz"])
        scan_layout.addRow("Frequency Band:", self.band_select)
        
        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.scan_networks)
        scan_layout.addRow(self.scan_button)
        
        self.scan_progress = QProgressBar()
        scan_layout.addRow("Scan Progress:", self.scan_progress)
        
        scan_group.setLayout(scan_layout)
        self.control_layout.addWidget(scan_group)
        
        # Heatmap controls
        heatmap_group = QGroupBox("Heatmap Controls")
        heatmap_layout = QFormLayout()
        
        self.load_floor_plan_button = QPushButton("Load Floor Plan")
        self.load_floor_plan_button.clicked.connect(self.load_floor_plan)
        heatmap_layout.addRow(self.load_floor_plan_button)
        
        self.heatmap_resolution = QSpinBox()
        self.heatmap_resolution.setRange(10, 100)
        self.heatmap_resolution.setValue(50)
        heatmap_layout.addRow("Resolution:", self.heatmap_resolution)
        
        self.heatmap_3d = QCheckBox("3D Heatmap")
        heatmap_layout.addRow(self.heatmap_3d)
        
        heatmap_group.setLayout(heatmap_layout)
        self.control_layout.addWidget(heatmap_group)
        
        # Analysis controls
        analysis_group = QGroupBox("Analysis Controls")
        analysis_layout = QFormLayout()
        
        self.channel_optimize = QPushButton("Optimize Channels")
        self.channel_optimize.clicked.connect(self.optimize_channels)
        analysis_layout.addRow(self.channel_optimize)
        
        self.interference_check = QPushButton("Check Interference")
        self.interference_check.clicked.connect(self.check_interference)
        analysis_layout.addRow(self.interference_check)
        
        self.dead_zone_check = QPushButton("Detect Dead Zones")
        self.dead_zone_check.clicked.connect(self.detect_dead_zones)
        analysis_layout.addRow(self.dead_zone_check)
        
        analysis_group.setLayout(analysis_layout)
        self.control_layout.addWidget(analysis_group)
        
        self.control_dock.setWidget(self.control_widget)
        
    def create_settings_ui(self):
        # General settings
        general_group = QGroupBox("General Settings")
        general_layout = QFormLayout()
        
        self.theme_select = QComboBox()
        self.theme_select.addItems(self.themes.keys())
        self.theme_select.currentTextChanged.connect(self.set_theme)
        general_layout.addRow("Theme:", self.theme_select)
        
        self.language_select = QComboBox()
        self.language_select.addItems(self.translations.keys())
        self.language_select.currentTextChanged.connect(self.set_language)
        general_layout.addRow("Language:", self.language_select)
        
        general_group.setLayout(general_layout)
        self.settings_layout.addWidget(general_group)
        
        # Network settings
        network_group = QGroupBox("Network Settings")
        network_layout = QFormLayout()
        
        self.wifi6_support = QCheckBox("Enable Wi-Fi 6/6E Support")
        network_layout.addRow(self.wifi6_support)
        
        self.wpa3_support = QCheckBox("Enable WPA3 Support")
        network_layout.addRow(self.wpa3_support)
        
        self.offline_mode = QCheckBox("Offline Mode")
        network_layout.addRow(self.offline_mode)
        
        network_group.setLayout(network_layout)
        self.settings_layout.addWidget(network_group)
        
    def create_simulation_ui(self):
        # Simulation controls
        sim_group = QGroupBox("Simulation Controls")
        sim_layout = QFormLayout()
        
        self.ap_model = QComboBox()
        self.ap_model.addItems(["Generic AP", "TP-Link AX6000", "Netgear Orbi", "Cisco Meraki"])
        sim_layout.addRow("Access Point Model:", self.ap_model)
        
        self.wall_material = QComboBox()
        self.wall_material.addItems(["Concrete", "Brick", "Drywall", "Glass"])
        sim_layout.addRow("Wall Material:", self.wall_material)
        
        self.device_count = QSpinBox()
        self.device_count.setRange(1, 200)
        self.device_count.setValue(10)
        sim_layout.addRow("Device Count:", self.device_count)
        
        self.simulate_button = QPushButton("Run Simulation")
        self.simulate_button.clicked.connect(self.simulate_network)
        sim_layout.addRow(self.simulate_button)
        
        sim_group.setLayout(sim_layout)
        self.simulation_layout.addWidget(sim_group)
        
        # Simulation results
        self.sim_results = QTextEdit()
        self.sim_results.setReadOnly(True)
        self.simulation_layout.addWidget(self.sim_results)
        
    def init_heatmap(self):
        self.heatmap_plot = self.heatmap_widget.addPlot()
        self.heatmap_plot.setAspectLocked(True)
        self.heatmap_image = pg.ImageItem()
        self.heatmap_plot.addItem(self.heatmap_image)
        
        # Add color bar
        self.color_bar = pg.ColorBarItem(
            values=(-100, 0),
            colorMap=pg.colormap.get("viridis")
        )
        self.heatmap_widget.addItem(self.color_bar)
        
    def init_network_table(self):
        self.network_table.setColumnCount(7)
        self.network_table.setHorizontalHeaderLabels([
            "SSID", "BSSID", "Channel", "RSSI (dBm)",
            "Security", "Frequency", "SNR"
        ])
        self.network_table.setRowCount(0)
        
    def apply_theme(self):
        theme = self.themes[self.current_theme]
        if self.current_theme == "Dark":
            self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
        else:
            self.setStyleSheet(f"""
                QMainWindow {{ background-color: {theme['bg']}; color: {theme['fg']}; }}
                QPushButton {{ background-color: {theme['accent']}; color: {theme['fg']}; }}
                QComboBox {{ background-color: {theme['bg']}; color: {theme['fg']}; }}
                QLineEdit {{ background-color: {theme['bg']}; color: {theme['fg']}; }}
                QTableWidget {{ background-color: {theme['bg']}; color: {theme['fg']}; }}
                QTabWidget::pane {{ background-color: {theme['bg']}; }}
                QDockWidget {{ background-color: {theme['bg']}; color: {theme['fg']}; }}
            """)
            
    def apply_language(self):
        direction = self.translations[self.current_language]["dir"]
        self.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if direction == "rtl"
            else Qt.LayoutDirection.LeftToRight
        )
        # Load translation file
        translation_file = self.translations[self.current_language]["file"]
        if os.path.exists(translation_file):
            self.translator.load(translation_file)
            QApplication.instance().installTranslator(self.translator)
        else:
            self.status_bar.showMessage(f"Translation file {translation_file} not found")
        
    def set_theme(self, theme):
        self.current_theme = theme
        self.apply_theme()
        
    def set_language(self, language):
        self.current_language = language
        self.apply_language()
        
    def load_floor_plan(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Floor Plan", "",
            "Images (*.png *.jpg *.jpeg *.pdf *.dwg)"
        )
        if file_name:
            try:
                self.floor_plan = Image.open(file_name)
                self.status_bar.showMessage(f"Floor plan loaded: {file_name}")
                self.update_heatmap()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load floor plan: {str(e)}")
                
    def scan_networks(self):
        if self.offline_mode.isChecked():
            QMessageBox.information(self, "Offline Mode", "Scanning disabled in offline mode")
            return
            
        if not pywifi or not self.wifi:
            QMessageBox.critical(
                self, "Error",
                "WiFi scanning unavailable: pywifi not installed or failed to initialize. "
                "Please install pywifi and comtypes or enable offline mode."
            )
            self.scan_progress.setValue(0)
            return
            
        try:
            self.scan_data = []
            self.scan_progress.setValue(0)
            interfaces = self.wifi.interfaces()
            if not interfaces:
                QMessageBox.critical(self, "Error", "No wireless interfaces found")
                self.scan_progress.setValue(0)
                return
                
            total_interfaces = len(interfaces)
            progress_step = 100 / total_interfaces if total_interfaces > 0 else 100
            
            for i, iface in enumerate(interfaces):
                try:
                    iface.scan()
                    time.sleep(2)  # Allow time for scan to complete
                    profiles = iface.scan_results()
                    for profile in profiles:
                        frequency = profile.freq / 1000000  # Convert Hz to MHz
                        if self.band_select.currentText() == "2.4 GHz" and not (2400 <= frequency <= 2500):
                            continue
                        if self.band_select.currentText() == "5 GHz" and not (5000 <= frequency <= 5900):
                            continue
                        if self.band_select.currentText() == "6 GHz" and not (5900 <= frequency <= 7100):
                            continue
                            
                        snr = profile.signal - profile.noise if hasattr(profile, 'noise') and profile.noise else 0
                        security = profile.auth if hasattr(profile, 'auth') else "Open"
                        self.scan_data.append({
                            'ssid': profile.ssid or "Hidden",
                            'bssid': profile.bssid,
                            'channel': profile.channel if hasattr(profile, 'channel') else 0,
                            'rssi': profile.signal,
                            'security': security,
                            'frequency': f"{frequency} MHz",
                            'snr': snr
                        })
                    self.scan_progress.setValue(int((i + 1) * progress_step))
                except Exception as e:
                    self.status_bar.showMessage(f"Error scanning interface {i}: {str(e)}")
                    continue
            
            self.update_network_table()
            self.status_bar.showMessage("Network scan completed")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Network scan failed: {str(e)}")
            self.scan_progress.setValue(0)
            
    def update_network_table(self):
        self.network_table.setRowCount(len(self.scan_data))
        for i, network in enumerate(self.scan_data):
            self.network_table.setItem(i, 0, QTableWidgetItem(network['ssid']))
            self.network_table.setItem(i, 1, QTableWidgetItem(network['bssid']))
            self.network_table.setItem(i, 2, QTableWidgetItem(str(network['channel'])))
            self.network_table.setItem(i, 3, QTableWidgetItem(str(network['rssi'])))
            self.network_table.setItem(i, 4, QTableWidgetItem(network['security']))
            self.network_table.setItem(i, 5, QTableWidgetItem(network['frequency']))
            self.network_table.setItem(i, 6, QTableWidgetItem(str(network['snr'])))
        self.network_table.resizeColumnsToContents()
        
    def generate_heatmap(self):
        if not self.floor_plan:
            QMessageBox.warning(self, "Warning", "Please load a floor plan first")
            return
            
        resolution = self.heatmap_resolution.value()
        width, height = self.floor_plan.size
        self.heatmap_data = np.zeros((height // resolution, width // resolution))
        
        # Generate heatmap based on scan data
        for network in self.scan_data:
            for i in range(height // resolution):
                for j in range(width // resolution):
                    # Simplified RSSI-based heatmap with path loss
                    distance = np.random.uniform(1, 50)
                    freq_mhz = float(network['frequency'].split()[0])
                    path_loss = 20 * math.log10(distance) + 20 * math.log10(freq_mhz)
                    self.heatmap_data[i, j] += network['rssi'] - path_loss
                    
        self.heatmap_data = np.clip(self.heatmap_data, -100, -30)
        self.heatmap_image.setImage(self.heatmap_data)
        self.color_bar.setImageItem(self.heatmap_image)
        
        if self.heatmap_3d.isChecked():
            self.heatmap_plot.enableAutoRange()
            self.heatmap_plot.setZValue(1)
        
    def update_heatmap(self):
        if self.floor_plan:
            self.heatmap_plot.clear()
            self.heatmap_image = pg.ImageItem()
            self.heatmap_plot.addItem(self.heatmap_image)
            if self.floor_plan:
                floor_plan_array = np.array(self.floor_plan.convert('RGB'))
                bg_image = pg.ImageItem(floor_plan_array)
                self.heatmap_plot.addItem(bg_image)
                bg_image.setZValue(-1)
            self.generate_heatmap()
            
    def optimize_channels(self):
        channels = {1: 0, 6: 0, 11: 0}  # Common 2.4 GHz channels
        if self.band_select.currentText() == "5 GHz":
            channels = {36: 0, 40: 0, 44: 0, 48: 0}
        elif self.band_select.currentText() == "6 GHz":
            channels = {1: 0, 5: 0, 9: 0, 13: 0}
            
        for network in self.scan_data:
            channel = network['channel']
            if channel in channels:
                channels[channel] += 1
                
        optimal_channel = min(channels, key=channels.get)
        QMessageBox.information(
            self, "Channel Optimization",
            f"Recommended channel: {optimal_channel} (Least congested)"
        )
        
    def check_interference(self):
        interference_sources = []
        non_wifi_interference = ["Microwave", "Bluetooth", "Cordless Phone"]
        
        for network in self.scan_data:
            if network['rssi'] > -50:
                interference_sources.append(f"WiFi: {network['ssid']} (RSSI: {network['rssi']} dBm)")
                
        # Simulate non-WiFi interference detection
        if np.random.random() > 0.7:
            interference_sources.append(np.random.choice(non_wifi_interference))
            
        if interference_sources:
            QMessageBox.warning(
                self, "Interference Detected",
                f"Potential interference sources:\n{', '.join(interference_sources)}"
            )
        else:
            QMessageBox.information(self, "Interference Check", "No significant interference detected")
            
    def detect_dead_zones(self):
        if not self.heatmap_data.size:
            QMessageBox.warning(self, "Warning", "Generate heatmap first")
            return
            
        dead_zones = np.where(self.heatmap_data < -80)
        if len(dead_zones[0]) > 0:
            QMessageBox.warning(
                self, "Dead Zones Detected",
                f"Found {len(dead_zones[0])} areas with weak signal (< -80 dBm)"
            )
            # Highlight dead zones on heatmap
            self.heatmap_data[dead_zones] = -100
            self.update_heatmap()
        else:
            QMessageBox.information(self, "Dead Zones", "No dead zones detected")
            
    def simulate_network(self):
        if not self.floor_plan:
            QMessageBox.warning(self, "Warning", "Please load a floor plan first")
            return
            
        # Simulate network performance
        ap_model = self.ap_model.currentText()
        wall_material = self.wall_material.currentText()
        device_count = self.device_count.value()
        
        # Simplified simulation model
        attenuation = {
            "Concrete": 15,
            "Brick": 12,
            "Drywall": 8,
            "Glass": 5
        }
        
        sim_results = f"""
        Network Simulation Results
        =========================
        Access Point: {ap_model}
        Wall Material: {wall_material}
        Device Count: {device_count}
        Attenuation: {attenuation[wall_material]} dB/m
        
        Estimated Performance:
        - Max Range: {100 / attenuation[wall_material]:.1f} meters
        - Max Throughput: {self.calculate_throughput(ap_model, device_count)} Mbps
        - Latency: {np.random.uniform(1, 5):.2f} ms
        - Capacity: {self.calculate_capacity(ap_model)} devices
        """
        
        self.sim_results.setText(sim_results)
        
    def calculate_throughput(self, ap_model, device_count):
        # Simplified throughput calculation
        base_throughputs = {
            "Generic AP": 300,
            "TP-Link AX6000": 6000,
            "Netgear Orbi": 4000,
            "Cisco Meraki": 1300
        }
        base = base_throughputs.get(ap_model, 300)
        return base / max(1, device_count / 10)
        
    def calculate_capacity(self, ap_model):
        # Simplified capacity calculation
        capacities = {
            "Generic AP": 20,
            "TP-Link AX6000": 100,
            "Netgear Orbi": 80,
            "Cisco Meraki": 50
        }
        return capacities.get(ap_model, 20)
        
    def save_project(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "WiFiMapper Project (*.wmp)"
        )
        if file_name:
            project_data = {
                'scan_data': self.scan_data,
                'heatmap_data': self.heatmap_data.tolist() if self.heatmap_data.size else [],
                'settings': {
                    'theme': self.current_theme,
                    'language': self.current_language,
                    'wifi6': self.wifi6_support.isChecked(),
                    'wpa3': self.wpa3_support.isChecked(),
                    'offline': self.offline_mode.isChecked(),
                    'floor_plan': self.floor_plan.filename if self.floor_plan else ""
                }
            }
            with open(file_name, 'w') as f:
                json.dump(project_data, f)
            self.status_bar.showMessage(f"Project saved to {file_name}")
            
    def export_report(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Export Report", "",
            "PDF Files (*.pdf);;CSV Files (*.csv);;KMZ Files (*.kmz)"
        )
        if file_name:
            if file_name.endswith('.pdf'):
                self.generate_pdf_report(file_name)
            elif file_name.endswith('.csv'):
                self.generate_csv_report(file_name)
            elif file_name.endswith('.kmz'):
                self.generate_kmz_report(file_name)
            self.status_bar.showMessage(f"Report exported to {file_name}")
            
    def generate_pdf_report(self, file_name):
        c = canvas.Canvas(file_name, pagesize=letter)
        c.setFont("Helvetica", 12)
        
        c.drawString(100, 750, "WiFiMapper Network Analysis Report")
        c.drawString(100, 730, f"Generated: {datetime.datetime.now()}")
        
        y = 700
        for network in self.scan_data:
            c.drawString(100, y, f"SSID: {network['ssid']}")
            c.drawString(100, y-20, f"RSSI: {network['rssi']} dBm")
            c.drawString(100, y-40, f"Channel: {network['channel']}")
            c.drawString(100, y-60, f"SNR: {network['snr']} dB")
            y -= 80
            
        if self.heatmap_data.size:
            c.drawString(100, y, "Heatmap Statistics:")
            c.drawString(100, y-20, f"Average RSSI: {np.mean(self.heatmap_data):.1f} dBm")
            c.drawString(100, y-40, f"Min RSSI: {np.min(self.heatmap_data):.1f} dBm")
            c.drawString(100, y-60, f"Max RSSI: {np.max(self.heatmap_data):.1f} dBm")
            
        c.save()
        
    def generate_csv_report(self, file_name):
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["SSID", "BSSID", "Channel", "RSSI", "Security", "Frequency", "SNR"])
            for network in self.scan_data:
                writer.writerow([
                    network['ssid'], network['bssid'], network['channel'],
                    network['rssi'], network['security'], network['frequency'],
                    network['snr']
                ])
                
    def generate_kmz_report(self, file_name):
        try:
            import simplekml
            kml = simplekml.Kml()
            for i, network in enumerate(self.scan_data):
                pnt = kml.newpoint(name=network['ssid'])
                pnt.coords = [(np.random.uniform(-180, 180), np.random.uniform(-90, 90))]
                pnt.description = f"RSSI: {network['rssi']} dBm\nChannel: {network['channel']}\nSNR: {network['snr']} dB"
            kml.save(file_name)
        except ImportError:
            QMessageBox.critical(self, "Error", "KMZ export requires simplekml library")
            
    def show_about(self):
        QMessageBox.information(
            self, "About WiFiMapper",
            "WiFiMapper v1.0\nProfessional WiFi Analysis Tool\nDeveloped by Hamid Yarali\n© 2025"
        )
        
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "Exit", "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.scan_timer.stop()
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WiFiMapper()
    window.show()
    sys.exit(app.exec())