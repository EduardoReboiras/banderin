# ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt
from ui.views.products_view import ProductsView
from ui.views.compras_view import ComprasView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Banderín - Sistema de Gestión")
        self.resize(1200, 800)
        self._init_ui()
    
    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # === SIDEBAR IZQUIERDO ===
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
                border-radius: 0;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
            QPushButton:checked {
                background-color: #16a085;
                font-weight: bold;
            }
        """)
        side_layout = QVBoxLayout(sidebar)
        side_layout.setSpacing(0)
        
        # Título del sidebar
        titulo = QLabel(" BANDERÍN")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            color: white; 
            font-size: 18px; 
            font-weight: bold; 
            padding: 20px 10px;
            background-color: #1a252f;
        """)
        side_layout.addWidget(titulo)
        
        # Botones de navegación
        self.btn_productos = QPushButton("📦 Productos")
        self.btn_compras = QPushButton("🛒 Compras")
        
        for btn in [self.btn_productos, self.btn_compras]:
            btn.setCheckable(True)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(50)
            side_layout.addWidget(btn)
        
        side_layout.addStretch()
        layout.addWidget(sidebar)
        
        # === ÁREA PRINCIPAL ===
        self.stacked = QStackedWidget()
        self.stacked.setStyleSheet("""
            QStackedWidget {
                background-color: #ecf0f1;
                color: #2c3e50;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                padding: 5px;
                border-radius: 3px;
            }
            QGroupBox {
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QTableView {
                background-color: white;
                color: #2c3e50;
                gridline-color: #bdc3c7;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 5px;
                border: none;
            }
        """)
        layout.addWidget(self.stacked, 1)
        
        # Crear vistas
        self.products_view = ProductsView()
        self.compras_view = ComprasView()
        
        self.stacked.addWidget(self.products_view)  # índice 0
        self.stacked.addWidget(self.compras_view)   # índice 1
        
        # Conexiones
        self.btn_productos.clicked.connect(lambda: self._cambiar_vista(0, self.btn_productos))
        self.btn_compras.clicked.connect(lambda: self._cambiar_vista(1, self.btn_compras))
        
        # Vista inicial
        self.btn_productos.setChecked(True)
    
    def _cambiar_vista(self, index, boton_activo):
        """Cambia la vista visible y actualiza el botón activo"""
        # Desmarcar todos los botones
        for btn in [self.btn_productos, self.btn_compras]:
            btn.setChecked(False)
        
        # Marcar el botón activo
        boton_activo.setChecked(True)
        
        # Cambiar la vista
        self.stacked.setCurrentIndex(index)