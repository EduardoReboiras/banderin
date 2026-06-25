# ui/views/products_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QDoubleSpinBox, QPushButton,
    QTableView, QHeaderView, QMessageBox, QGroupBox,
    QLabel, QFileDialog
)
from PySide6.QtCore import Qt
from services.product_service import ProductService
from core.models import Producto
from ui.widgets.product_table_model import ProductTableModel
from decimal import Decimal
import csv


class ProductsView(QWidget):
    """Vista principal de gestión de productos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = ProductService()
        self.producto_actual: Producto | None = None
        self._init_ui()
        self.cargar_datos()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Título
        titulo = QLabel("Gestión de Productos - Banderín")
        titulo.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            padding: 10px;
            background-color: #3498db;
            color: white;
            border-radius: 5px;
        """)
        layout.addWidget(titulo)
        
        # Formulario
        form_group = QGroupBox("Datos del Producto")
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Ej: 345-0019")
        self.txt_codigo.setMaximumWidth(200)
        
        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Ej: ABACO MARTIZ Nº7/10")
        
        self.txt_precio = QLineEdit()
        self.txt_precio.setPlaceholderText("Ej: 8.434,80")
        self.txt_precio.setMaximumWidth(200)
        self.txt_precio.setToolTip("Formato: 8.434,80 (punto para miles, coma para decimales)")
        
        form_layout.addRow("Código:", self.txt_codigo)
        form_layout.addRow("Descripción:", self.txt_descripcion)
        form_layout.addRow("Precio Unitario:", self.txt_precio)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botones de acción
        btn_layout = QHBoxLayout()
        
        self.btn_nuevo = QPushButton("➕ Nuevo")
        self.btn_nuevo.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px;")
        
        self.btn_guardar = QPushButton("💾 Guardar")
        self.btn_guardar.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        
        self.btn_cancelar = QPushButton("❌ Cancelar")
        self.btn_cancelar.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        
        self.btn_exportar = QPushButton("📄 Exportar CSV")
        self.btn_exportar.setStyleSheet("background-color: #f39c12; color: white; padding: 8px;")
        
        for btn in [self.btn_nuevo, self.btn_guardar, self.btn_eliminar, 
                    self.btn_cancelar, self.btn_exportar]:
            btn_layout.addWidget(btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Búsqueda
        search_group = QGroupBox("Búsqueda")
        search_layout = QHBoxLayout()
        
        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText("Buscar por código o descripción...")
        
        self.btn_buscar = QPushButton("🔍 Buscar")
        self.btn_limpiar = QPushButton("📋 Mostrar Todos")
        
        search_layout.addWidget(QLabel("🔎"))
        search_layout.addWidget(self.txt_buscar, 1)
        search_layout.addWidget(self.btn_buscar)
        search_layout.addWidget(self.btn_limpiar)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Tabla de productos
        table_group = QGroupBox("Listado de Productos")
        table_layout = QVBoxLayout()
        
        self.tabla = QTableView()
        self.modelo = ProductTableModel()
        self.tabla.setModel(self.modelo)
        
        # Configuración de la tabla
        self.tabla.setSelectionBehavior(QTableView.SelectRows)
        self.tabla.setSelectionMode(QTableView.SingleSelection)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSortingEnabled(True)
        self.tabla.horizontalHeader().setStretchLastSection(True)
        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        
        # Ajustar columnas específicas
        self.tabla.setColumnWidth(0, 120)  # Código
        self.tabla.setColumnWidth(2, 150)  # Precio
        
        table_layout.addWidget(self.tabla)
        table_group.setLayout(table_layout)
        layout.addWidget(table_group, 1)  # Stretch factor
        
        # Conexiones de señales
        self._conectar_señales()
    
    def _conectar_señales(self):
        """Conecta las señales de los botones"""
        self.btn_nuevo.clicked.connect(self.limpiar_formulario)
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_eliminar.clicked.connect(self.eliminar)
        self.btn_cancelar.clicked.connect(self.limpiar_formulario)
        self.btn_buscar.clicked.connect(self.buscar)
        self.btn_limpiar.clicked.connect(self.cargar_datos)
        self.btn_exportar.clicked.connect(self.exportar_csv)
        self.tabla.clicked.connect(self.on_tabla_click)
        self.txt_buscar.returnPressed.connect(self.buscar)
    
    def cargar_datos(self):
        """Carga todos los productos en la tabla"""
        productos = self.service.obtener_todos()
        self.modelo.set_productos(productos)
        self.lbl_total = QLabel(f"Total: {len(productos)} productos")
    
    def buscar(self):
        """Busca productos según el texto ingresado"""
        texto = self.txt_buscar.text().strip()
        if texto:
            productos = self.service.buscar(texto)
            self.modelo.set_productos(productos)
        else:
            self.cargar_datos()
    
    def on_tabla_click(self, index):
        """Maneja el clic en la tabla - carga el producto en el formulario"""
        producto = self.modelo.get_producto(index.row())
        self.producto_actual = producto
        self.cargar_en_formulario(producto)
    
    def cargar_en_formulario(self, producto: Producto):
        """Carga los datos de un producto en los campos del formulario"""
        self.txt_codigo.setText(producto.codigo)
        self.txt_descripcion.setText(producto.descripcion)
        self.txt_precio.setText(producto.get_precio_formateado().replace("$ ", "").replace(".", "X").replace(",", ".").replace("X", ","))
    
    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.producto_actual = None
        self.txt_codigo.clear()
        self.txt_descripcion.clear()
        self.txt_precio.clear()
        self.txt_codigo.setFocus()
    
    def _parsear_precio(self, texto: str) -> Decimal | None:
        """
        Convierte un string de precio en formato argentino a Decimal
        Ej: "8.434,80" -> Decimal("8434.80")
        """
        try:
            # Remover símbolo de peso y espacios
            texto = texto.replace("$", "").strip()
            # Reemplazar punto de miles y coma decimal
            texto = texto.replace(".", "").replace(",", ".")
            return Decimal(texto)
        except Exception:
            return None
    
    def _leer_formulario(self) -> Producto | None:
        """Lee los datos del formulario y retorna un objeto Producto"""
        codigo = self.txt_codigo.text().strip()
        descripcion = self.txt_descripcion.text().strip()
        precio = self._parsear_precio(self.txt_precio.text())
        
        if not codigo or not descripcion:
            QMessageBox.warning(
                self, "Validación",
                "Código y descripción son obligatorios"
            )
            return None
        
        if precio is None:
            QMessageBox.warning(
                self, "Validación",
                "Precio inválido. Use el formato: 8.434,80"
            )
            return None
        
        return Producto(
            id=self.producto_actual.id if self.producto_actual else None,
            codigo=codigo,
            descripcion=descripcion,
            precio_unitario=precio
        )
    
    def guardar(self):
        """Guarda o actualiza un producto"""
        producto = self._leer_formulario()
        if not producto:
            return
        
        if self.producto_actual and self.producto_actual.id:
            # Actualizar existente
            ok = self.service.actualizar(producto)
            msg = "Producto actualizado correctamente" if ok else "Error al actualizar"
        else:
            # Crear nuevo
            id = self.service.crear(producto)
            if id:
                msg = f"Producto creado con ID: {id}"
                ok = True
            else:
                msg = "Error: El código ya existe"
                ok = False
        
        if ok:
            QMessageBox.information(self, "Éxito", msg)
            self.cargar_datos()
            self.limpiar_formulario()
        else:
            QMessageBox.critical(self, "Error", msg)
    
    def eliminar(self):
        """Elimina un producto seleccionado"""
        if not self.producto_actual or not self.producto_actual.id:
            QMessageBox.warning(
                self, "Atención",
                "Seleccione un producto de la tabla para eliminar"
            )
            return
        
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Está seguro de eliminar el producto?\n\n"
            f"Código: {self.producto_actual.codigo}\n"
            f"Descripción: {self.producto_actual.descripcion}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.service.eliminar(self.producto_actual.id):
                QMessageBox.information(self, "Éxito", "Producto eliminado")
                self.cargar_datos()
                self.limpiar_formulario()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el producto")
    
    def exportar_csv(self):
        """Exporta los productos a un archivo CSV"""
        archivo, _ = QFileDialog.getSaveFileName(
            self, "Exportar productos", "",
            "Archivos CSV (*.csv);;Todos los archivos (*.*)"
        )
        
        if archivo:
            try:
                productos = self.service.obtener_todos()
                with open(archivo, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(['Código', 'Descripción', 'Precio Unitario'])
                    for prod in productos:
                        writer.writerow([
                            prod.codigo,
                            prod.descripcion,
                            prod.get_precio_formateado().replace("$ ", "")
                        ])
                QMessageBox.information(
                    self, "Éxito",
                    f"Se exportaron {len(productos)} productos a:\n{archivo}"
                )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error",
                    f"Error al exportar:\n{str(e)}"
                )