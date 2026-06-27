from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton,
    QTableView, QHeaderView, QMessageBox, QGroupBox,
    QLabel, QDateEdit, QFileDialog
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtPrintSupport import QPrinter, QPrintDialog
from services.compra_service import CompraService
from services.ticket_generator import TicketGenerator
from core.models import Compra, DetalleCompra
from ui.widgets.compra_table_model import CompraTableModel
from decimal import Decimal
from datetime import datetime



class ComprasView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.service = CompraService()
        self.lineas_actuales: list[DetalleCompra] = []
        self.compra_seleccionada: Compra | None = None
        self._init_ui()
        self.cargar_historial()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título
        titulo = QLabel("🛒 Módulo de Compras")
        titulo.setStyleSheet("""
            font-size: 18px; font-weight: bold; padding: 10px;
            background-color: #27ae60; color: white; border-radius: 5px;
        """)
        layout.addWidget(titulo)
        
        # === SECCIÓN 1: Formulario para agregar líneas ===
        form_group = QGroupBox("Agregar Producto a la Compra")
        form_layout = QFormLayout()
        
        self.date_compra = QDateEdit()
        self.date_compra.setDate(QDate.currentDate())  # Fecha de hoy por defecto
        self.date_compra.setCalendarPopup(True)  # Mostrar calendario al hacer clic
        self.date_compra.setDisplayFormat("dd/MM/yyyy")
        self.date_compra.setStyleSheet("""
            QDateEdit {
                background-color: white;
                color: #2c3e50;
                border: 1px solid #bdc3c7;
                padding: 5px;
                border-radius: 3px;
            }
            QDateEdit:disabled {
                background-color: #ecf0f1;
                color: #7f8c8d;
                border: 1px solid #bdc3c7;
            }
        """)

        form_layout.addRow("Fecha de Compra:", self.date_compra)

        self.txt_codigo = QLineEdit()
        self.txt_codigo.setPlaceholderText("Ej: 345-0019")
        
        self.txt_descripcion = QLineEdit()
        self.txt_descripcion.setPlaceholderText("Descripción del producto")
        
        self.txt_precio = QLineEdit()
        self.txt_precio.setPlaceholderText("Ej: 8.434,80")
        
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 9999)
        self.spin_cantidad.setValue(1)
        
        form_layout.addRow("Código:", self.txt_codigo)
        form_layout.addRow("Descripción:", self.txt_descripcion)
        form_layout.addRow("Precio Unitario:", self.txt_precio)
        form_layout.addRow("Cantidad:", self.spin_cantidad)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # Botones de línea
        btn_linea_layout = QHBoxLayout()
        self.btn_agregar_linea = QPushButton("➕ Agregar Línea")
        self.btn_agregar_linea.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px;")
        self.btn_quitar_linea = QPushButton("➖ Quitar Línea Seleccionada")
        self.btn_quitar_linea.setStyleSheet("background-color: #e67e22; color: white; padding: 8px;")
        self.btn_limpiar_lineas = QPushButton("️ Limpiar Todo")
        self.btn_limpiar_lineas.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px;")
        
        for btn in [self.btn_agregar_linea, self.btn_quitar_linea, self.btn_limpiar_lineas]:
            btn_linea_layout.addWidget(btn)
        btn_linea_layout.addStretch()
        layout.addLayout(btn_linea_layout)
        
        # === SECCIÓN 2: Tabla de líneas actuales ===
        lineas_group = QGroupBox("Líneas de la Compra Actual")
        lineas_layout = QVBoxLayout()
        
        self.tabla_lineas = QTableView()
        self.tabla_lineas.setSelectionBehavior(QTableView.SelectRows)
        self.tabla_lineas.setAlternatingRowColors(True)
        self.tabla_lineas.horizontalHeader().setStretchLastSection(True)
        lineas_layout.addWidget(self.tabla_lineas)
        
        # Total de la compra actual
        self.lbl_total_actual = QLabel("Total: $ 0,00")
        self.lbl_total_actual.setStyleSheet("font-size: 16px; font-weight: bold; padding: 5px;")
        self.lbl_total_actual.setAlignment(Qt.AlignRight)
        lineas_layout.addWidget(self.lbl_total_actual)
        
        lineas_group.setLayout(lineas_layout)
        layout.addWidget(lineas_group)
        
        # Botón guardar compra
        btn_guardar_layout = QHBoxLayout()
        self.btn_guardar_compra = QPushButton("💾 Guardar Compra Completa")
        self.btn_guardar_compra.setStyleSheet("""
            background-color: #2980b9; color: white; 
            padding: 12px; font-size: 14px; font-weight: bold;
        """)
        btn_guardar_layout.addWidget(self.btn_guardar_compra)
        btn_guardar_layout.addStretch()
        layout.addLayout(btn_guardar_layout)
        
        # === SECCIÓN 3: Historial de compras ===
        hist_group = QGroupBox("Historial de Compras")
        hist_layout = QVBoxLayout()
        
        self.tabla_historial = QTableView()
        self.modelo_historial = CompraTableModel()
        self.tabla_historial.setModel(self.modelo_historial)
        self.tabla_historial.setSelectionBehavior(QTableView.SelectRows)
        self.tabla_historial.setAlternatingRowColors(True)
        self.tabla_historial.horizontalHeader().setStretchLastSection(True)
        hist_layout.addWidget(self.tabla_historial)
        
        # Botones del historial
        btn_hist_layout = QHBoxLayout()
        self.btn_ver_ticket = QPushButton(" Ver/Imprimir Ticket")
        self.btn_ver_ticket.setStyleSheet("background-color: #8e44ad; color: white; padding: 8px;")
        self.btn_eliminar_compra = QPushButton("🗑️ Eliminar Compra")
        self.btn_eliminar_compra.setStyleSheet("background-color: #c0392b; color: white; padding: 8px;")
        
        for btn in [self.btn_ver_ticket, self.btn_eliminar_compra]:
            btn_hist_layout.addWidget(btn)
        btn_hist_layout.addStretch()
        hist_layout.addLayout(btn_hist_layout)
        
        hist_group.setLayout(hist_layout)
        layout.addWidget(hist_group, 1)
        
        # Conexiones
        self._conectar_señales()
    
    def _conectar_señales(self):
        self.btn_agregar_linea.clicked.connect(self.agregar_linea)
        self.btn_quitar_linea.clicked.connect(self.quitar_linea)
        self.btn_limpiar_lineas.clicked.connect(self.limpiar_lineas)
        self.btn_guardar_compra.clicked.connect(self.guardar_compra)
        self.btn_ver_ticket.clicked.connect(self.ver_ticket)
        self.btn_eliminar_compra.clicked.connect(self.eliminar_compra)
        self.tabla_historial.clicked.connect(self.on_historial_click)
    
    def _parsear_precio(self, texto: str) -> Decimal | None:
        """
        Convierte un string de precio a Decimal, detectando automáticamente
        si está en formato argentino (8.434,80) o estándar/inglés (8342.23).
        """
        try:
            # Limpiar símbolos y espacios
            texto = texto.replace("$", "").strip()
            
            if not texto:
                return None
            
            # Contar puntos y comas
            cantidad_puntos = texto.count('.')
            cantidad_comas = texto.count(',')
            
            # Caso 1: Tiene ambos (ej: "8.434,80" o "8,434.80")
            if cantidad_puntos > 0 and cantidad_comas > 0:
                # El último separador es el decimal
                ultimo_punto = texto.rfind('.')
                ultima_coma = texto.rfind(',')
                
                if ultima_coma > ultimo_punto:
                    # Formato argentino: "8.434,80"
                    texto = texto.replace('.', '').replace(',', '.')
                else:
                    # Formato inglés: "8,434.80"
                    texto = texto.replace(',', '')
            
            # Caso 2: Solo tiene comas (ej: "8342,80" o "8,434")
            elif cantidad_comas > 0 and cantidad_puntos == 0:
                # Si hay una sola coma y 1-3 dígitos después, es decimal
                # Si hay una sola coma y más de 3 dígitos después, es de miles
                posicion_coma = texto.index(',')
                digitos_despues = len(texto) - posicion_coma - 1
                
                if digitos_despues <= 2:
                    # Es decimal: "8342,80"
                    texto = texto.replace(',', '.')
                else:
                    # Es de miles: "8,434" (raro pero posible)
                    texto = texto.replace(',', '')
            
            # Caso 3: Solo tiene puntos (ej: "8342.23" o "8.434")
            elif cantidad_puntos > 0 and cantidad_comas == 0:
                # Si hay un solo punto y 1-2 dígitos después, es decimal
                # Si hay un solo punto y 3 dígitos después, es ambiguo (asumimos decimal)
                # Si hay múltiples puntos, son de miles
                if cantidad_puntos == 1:
                    posicion_punto = texto.index('.')
                    digitos_despues = len(texto) - posicion_punto - 1
                    
                    if digitos_despues <= 2:
                        # Es decimal: "8342.23"
                        pass  # Ya está en formato correcto
                    else:
                        # Es de miles: "8.434" (raro en formato inglés)
                        texto = texto.replace('.', '')
                else:
                    # Múltiples puntos: son de miles "8.434.000"
                    texto = texto.replace('.', '')
            
            # Caso 4: No tiene separadores (ej: "8342")
            # Ya está en formato correcto
            
            return Decimal(texto)
        
        except Exception:
            return None
    
    def agregar_linea(self):
        codigo = self.txt_codigo.text().strip()
        descripcion = self.txt_descripcion.text().strip()
        precio = self._parsear_precio(self.txt_precio.text())
        cantidad = self.spin_cantidad.value()
        
        if not codigo or not descripcion:
            QMessageBox.warning(self, "Validación", "Código y descripción son obligatorios")
            return
        
        if precio is None or precio <= 0:
            QMessageBox.warning(self, "Validación", "Precio inválido")
            return
        
        if cantidad <= 0:
            QMessageBox.warning(self, "Validación", "La cantidad debe ser mayor a 0")
            return
        
        detalle = DetalleCompra(
            codigo_producto=codigo,
            descripcion=descripcion,
            precio_unitario=precio,
            cantidad=cantidad
        )
        detalle.calcular_subtotal()
        
        self.lineas_actuales.append(detalle)
        self.actualizar_tabla_lineas()
        self.limpiar_formulario_linea()

        # 🔒 BLOQUEAR LA FECHA SI YA HAY AL MENOS UNA LÍNEA
        if len(self.lineas_actuales) > 0:
            self.date_compra.setEnabled(False)
            self.date_compra.setToolTip("La fecha no se puede cambiar con líneas cargadas")
    
    def quitar_linea(self):
        # Verificar que haya un modelo asignado
        if self.tabla_lineas.model() is None:
            QMessageBox.warning(self, "Atención", "No hay líneas para quitar")
            return
        
        # Verificar que haya una selección
        selection_model = self.tabla_lineas.selectionModel()
        if selection_model is None or not selection_model.hasSelection():
            QMessageBox.warning(self, "Atención", "Seleccioná una línea para quitar")
            return
        
        indices = selection_model.selectedRows()
        
        # Eliminar en orden inverso para no desfasar índices
        for index in sorted(indices, key=lambda i: i.row(), reverse=True):
            self.lineas_actuales.pop(index.row())
        
        self.actualizar_tabla_lineas()
    
    def limpiar_lineas(self):
        if self.lineas_actuales and QMessageBox.question(
            self, "Confirmar", "¿Limpiar todas las líneas?"
        ) == QMessageBox.Yes:
            self.lineas_actuales.clear()
            self.actualizar_tabla_lineas()
            # 🔓 DESBLOQUEAR LA FECHA Y PONER LA DE HOY
            self.date_compra.setEnabled(True)
            self.date_compra.setDate(QDate.currentDate())
            self.date_compra.setToolTip("Seleccioná la fecha de la compra")
    
    def actualizar_tabla_lineas(self):
        from PySide6.QtGui import QStandardItemModel, QStandardItem
        
        modelo = QStandardItemModel()
        modelo.setHorizontalHeaderLabels(["Código", "Descripción", "P. Unitario", "Cant.", "Subtotal"])
        
        total = Decimal("0.00")
        for detalle in self.lineas_actuales:
            fila = [
                QStandardItem(detalle.codigo_producto),
                QStandardItem(detalle.descripcion),
                QStandardItem(f"$ {detalle.precio_unitario:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")),
                QStandardItem(str(detalle.cantidad)),
                QStandardItem(f"$ {detalle.subtotal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            ]
            modelo.appendRow(fila)
            total += detalle.subtotal
        
        self.tabla_lineas.setModel(modelo)
        self.tabla_lineas.horizontalHeader().setStretchLastSection(False)
        self.tabla_lineas.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.lbl_total_actual.setText(f"Total: $ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    def limpiar_formulario_linea(self):
        self.txt_codigo.clear()
        self.txt_descripcion.clear()
        self.txt_precio.clear()
        self.spin_cantidad.setValue(1)
        self.txt_codigo.setFocus()
    
    def guardar_compra(self):
        if not self.lineas_actuales:
            QMessageBox.warning(self, "Atención", "Agregá al menos una línea")
            return
        
        fecha_qdate = self.date_compra.date()
        fecha_str = fecha_qdate.toString("yyyy-MM-dd")

        compra_id = self.service.crear_compra(self.lineas_actuales, fecha_str)
        
        if compra_id:
            QMessageBox.information(self, "Éxito", f"Compra #{compra_id} guardada correctamente")
            self.lineas_actuales.clear()
            self.actualizar_tabla_lineas()
            self.cargar_historial()

            #  DESBLOQUEAR LA FECHA PARA LA PRÓXIMA COMPRA
            self.date_compra.setEnabled(True)
            self.date_compra.setDate(QDate.currentDate())
            self.date_compra.setToolTip("Seleccioná la fecha de la compra")
        else:
            QMessageBox.critical(self, "Error", "No se pudo guardar la compra")
    
    def cargar_historial(self):
        compras = self.service.obtener_historial()
        self.modelo_historial.set_compras(compras)
    
    def on_historial_click(self, index):
        self.compra_seleccionada = self.modelo_historial.get_compra(index.row())
    
    def eliminar_compra(self):
        if not self.compra_seleccionada:
            QMessageBox.warning(self, "Atención", "Seleccioná una compra del historial")
            return
        
        if QMessageBox.question(
            self, "Confirmar", 
            f"¿Eliminar la compra #{self.compra_seleccionada.id}?"
        ) == QMessageBox.Yes:
            if self.service.eliminar_compra(self.compra_seleccionada.id):
                QMessageBox.information(self, "Éxito", "Compra eliminada")
                self.compra_seleccionada = None
                self.cargar_historial()
    
    def ver_ticket(self):
        if not self.compra_seleccionada:
            QMessageBox.warning(self, "Atención", "Seleccioná una compra del historial")
            return
        
        compra = self.service.obtener_compra_completa(self.compra_seleccionada.id)
        if not compra:
            return
        
        html_ticket = TicketGenerator.generar_html(compra)
        
        # 1. Importar las clases nuevas de PySide6 (agregalas arriba del todo en tu archivo si preferís)
        from PySide6.QtGui import QTextDocument, QPageSize, QPageLayout
        from PySide6.QtCore import QMarginsF
        
        documento = QTextDocument()
        documento.setHtml(html_ticket)
        
        # 2. Configurar la impresora con la sintaxis de PySide6
        printer = QPrinter(QPrinter.HighResolution)
        
        # Configurar tamaño A4
        page_layout = QPageLayout(
            QPageSize(QPageSize.A4), 
            QPageLayout.Portrait, # Vertical
            QMarginsF(15, 15, 15, 15) # Márgenes de 15mm (izq, arr, der, aba)
        )
        printer.setPageLayout(page_layout)
        
        # 3. Mostrar diálogo de impresión
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec() == QPrintDialog.Accepted:
            documento.print_(printer)
            QMessageBox.information(self, "Éxito", "Ticket enviado a la impresora")
    
    