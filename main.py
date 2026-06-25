# main.py
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from core.database import Database


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Estilo global
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 13px;
        }
        QLineEdit, QDoubleSpinBox {
            padding: 6px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
        }
        QLineEdit:focus {
            border: 2px solid #3498db;
        }
        QPushButton {
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
            font-weight: bold;
        }
        QPushButton:hover {
            opacity: 0.9;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
            color: #2c3e50;
        }
        QTableView {
            gridline-color: #ecf0f1;
            alternate-background-color: #f8f9fa;
            selection-background-color: #3498db;
            selection-color: white;
        }
        QHeaderView::section {
            background-color: #34495e;
            color: white;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
    """)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()