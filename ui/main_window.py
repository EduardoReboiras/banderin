# ui/main_window.py (simplificado)
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from ui.views.products_view import ProductsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banderín - Sistema de Gestión")
        self.resize(1000, 700)
        self._init_ui()
    
    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header
        header = QLabel("🏪 LIBRERÍA - Sistema de Gestión")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("""
            background-color: #2c3e50;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px;
        """)
        layout.addWidget(header)
        
        # Vista principal de productos
        self.products_view = ProductsView()
        layout.addWidget(self.products_view)