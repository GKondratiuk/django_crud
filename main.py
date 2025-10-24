import sys
import json
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QComboBox, QListWidget, 
                               QLineEdit, QPushButton, QMessageBox, QListWidgetItem,
                               QSpinBox, QTabWidget, QTextEdit, QFrame)
from PySide6.QtCore import Qt
import pandas as pd
from datetime import datetime

class InventarioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.gestorias = self.cargar_gestorias()
        self.inventario = self.cargar_inventario()
        self.initUI()
        
    def initUI(self):
        """Inicializa la interfaz gráfica"""
        self.setWindowTitle('Sistema de Inventario - Gestorías')
        self.setGeometry(100, 100, 900, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Crear pestañas
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Pestaña 1: Gestión de Inventario
        tab_inventario = QWidget()
        tabs.addTab(tab_inventario, "Gestión de Inventario")
        
        # Pestaña 2: Exportación
        tab_exportar = QWidget()
        tabs.addTab(tab_exportar, "Exportar Datos")
        
        # Configurar pestaña de inventario
        self.setup_tab_inventario(tab_inventario)
        
        # Configurar pestaña de exportación
        self.setup_tab_exportar(tab_exportar)
        
    def setup_tab_inventario(self, tab):
        """Configura la pestaña de gestión de inventario"""
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Panel de gestión de gestorías
        gestoria_panel = QWidget()
        gestoria_panel_layout = QVBoxLayout()
        gestoria_panel.setLayout(gestoria_panel_layout)
        
        # Título para la sección de gestión de gestorías
        gestoria_panel_layout.addWidget(QLabel("Gestión de Gestorías"))
        
        # Layout para agregar nueva gestoría
        nueva_gestoria_layout = QHBoxLayout()
        self.input_gestoria_id = QLineEdit()
        self.input_gestoria_id.setPlaceholderText("ID (número)")
        self.input_gestoria_nombre = QLineEdit()
        self.input_gestoria_nombre.setPlaceholderText("Nombre de la Gestoría")
        
        nueva_gestoria_layout.addWidget(self.input_gestoria_id)
        nueva_gestoria_layout.addWidget(self.input_gestoria_nombre)
        
        btn_agregar_gestoria = QPushButton("Agregar Gestoría")
        btn_agregar_gestoria.clicked.connect(self.agregar_gestoria)
        nueva_gestoria_layout.addWidget(btn_agregar_gestoria)
        
        gestoria_panel_layout.addLayout(nueva_gestoria_layout)
        
        # Lista de gestorías existentes
        gestoria_panel_layout.addWidget(QLabel("Gestorías Existentes:"))
        self.lista_gestorias = QListWidget()
        gestoria_panel_layout.addWidget(self.lista_gestorias)
        
        # Botón para eliminar gestoría
        btn_eliminar_gestoria = QPushButton("Eliminar Gestoría Seleccionada")
        btn_eliminar_gestoria.clicked.connect(self.eliminar_gestoria)
        gestoria_panel_layout.addWidget(btn_eliminar_gestoria)
        
        # Agregar el panel de gestión al layout principal
        layout.addWidget(gestoria_panel)
        
        # Separador visual
        separador = QFrame()
        separador.setFrameShape(QFrame.HLine)
        separador.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separador)
        
        # Selección de gestoría
        gestoria_layout = QHBoxLayout()
        gestoria_layout.addWidget(QLabel("Seleccionar Gestoría:"))
        
        self.combo_gestorias = QComboBox()
        self.actualizar_combo_gestorias()
        
        self.combo_gestorias.currentIndexChanged.connect(self.cargar_inventario_gestoria)
        
        self.combo_gestorias.currentIndexChanged.connect(self.cargar_inventario_gestoria)
        gestoria_layout.addWidget(self.combo_gestorias)
        gestoria_layout.addStretch()
        layout.addLayout(gestoria_layout)
        
        # Información de la gestoría seleccionada
        self.label_info_gestoria = QLabel("")
        layout.addWidget(self.label_info_gestoria)
        
        # Lista de inventario
        layout.addWidget(QLabel("Inventario de la Gestoría:"))
        self.lista_inventario = QListWidget()
        layout.addWidget(self.lista_inventario)
        
        # Controles para agregar/modificar elementos
        form_layout = QHBoxLayout()
        
        # Descripción del elemento
        form_layout.addWidget(QLabel("Descripción:"))
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Ej: Silla, Mesa, Computadora...")
        form_layout.addWidget(self.input_descripcion)
        
        # Cantidad
        form_layout.addWidget(QLabel("Cantidad:"))
        self.input_cantidad = QSpinBox()
        self.input_cantidad.setMinimum(1)
        self.input_cantidad.setMaximum(1000)
        form_layout.addWidget(self.input_cantidad)
        
        layout.addLayout(form_layout)
        
        # Botones de acción
        botones_layout = QHBoxLayout()
        
        self.btn_agregar = QPushButton("Agregar Elemento")
        self.btn_agregar.clicked.connect(self.agregar_elemento)
        botones_layout.addWidget(self.btn_agregar)
        
        self.btn_modificar = QPushButton("Modificar Elemento")
        self.btn_modificar.clicked.connect(self.modificar_elemento)
        botones_layout.addWidget(self.btn_modificar)
        
        self.btn_eliminar = QPushButton("Eliminar Elemento")
        self.btn_eliminar.clicked.connect(self.eliminar_elemento)
        botones_layout.addWidget(self.btn_eliminar)
        
        botones_layout.addStretch()
        
        self.btn_limpiar = QPushButton("Limpiar Selección")
        self.btn_limpiar.clicked.connect(self.limpiar_seleccion)
        botones_layout.addWidget(self.btn_limpiar)
        
        layout.addLayout(botones_layout)
        
        # Cargar la primera gestoría por defecto
        if self.combo_gestorias.count() > 0:
            self.combo_gestorias.setCurrentIndex(0)
            self.cargar_inventario_gestoria()
    
    def setup_tab_exportar(self, tab):
        """Configura la pestaña de exportación"""
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Información sobre exportación
        info_label = QLabel(
            "Esta función permite exportar el inventario completo de todas las gestorías "
            "a un archivo Excel. El archivo se guardará en la carpeta 'exportaciones'."
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Botón de exportación
        self.btn_exportar = QPushButton("Exportar a Excel")
        self.btn_exportar.clicked.connect(self.exportar_a_excel)
        layout.addWidget(self.btn_exportar)
        
        # Área de texto para mostrar información de exportación
        self.texto_exportacion = QTextEdit()
        self.texto_exportacion.setReadOnly(True)
        self.texto_exportacion.setPlaceholderText("Aquí se mostrará información sobre la exportación...")
        layout.addWidget(self.texto_exportacion)
        
    def cargar_gestorias(self):
        """
        Carga el listado de gestorías desde un archivo JSON.
        Si el archivo no existe, crea uno vacío.
        """
        try:
            if os.path.exists('gestorias.json'):
                with open('gestorias.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Crear archivo vacío
                gestorias = {}
                with open('gestorias.json', 'w', encoding='utf-8') as f:
                    json.dump(gestorias, f, ensure_ascii=False, indent=2)
                return gestorias
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar gestorías: {str(e)}")
            return {"1": "Casa Central"}
    
    def cargar_inventario(self):
        """
        Carga el inventario desde un archivo JSON.
        Si el archivo no existe, crea uno vacío.
        """
        try:
            if os.path.exists('inventario.json'):
                with open('inventario.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Crear inventario vacío
                inventario_vacio = {}
                with open('inventario.json', 'w', encoding='utf-8') as f:
                    json.dump(inventario_vacio, f, indent=2)
                return inventario_vacio
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar inventario: {str(e)}")
            return {}
    
    def guardar_inventario(self):
        """Guarda el inventario en el archivo JSON"""
        try:
            with open('inventario.json', 'w', encoding='utf-8') as f:
                json.dump(self.inventario, f, ensure_ascii=False, indent=2)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar inventario: {str(e)}")
    
    def cargar_inventario_gestoria(self):
        """Carga y muestra el inventario de la gestoría seleccionada"""
        gestoria_id = self.combo_gestorias.currentData()
        gestoria_nombre = self.gestorias.get(gestoria_id, "Desconocida")
        
        # Actualizar información de la gestoría
        self.label_info_gestoria.setText(f"Gestoría {gestoria_id}: {gestoria_nombre}")
        
        # Limpiar la lista
        self.lista_inventario.clear()
        
        # Cargar elementos del inventario
        if gestoria_id in self.inventario:
            for descripcion, cantidad in self.inventario[gestoria_id].items():
                item_text = f"{cantidad} x {descripcion}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, descripcion)  # Guardar la descripción como dato adicional
                self.lista_inventario.addItem(item)
        
        # Limpiar campos de entrada
        self.limpiar_campos()
    
    def agregar_elemento(self):
        """Agrega un nuevo elemento al inventario de la gestoría actual"""
        gestoria_id = self.combo_gestorias.currentData()
        descripcion = self.input_descripcion.text().strip()
        cantidad = self.input_cantidad.value()
        
        if not descripcion:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese una descripción para el elemento.")
            return
        
        # Inicializar el inventario de la gestoría si no existe
        if gestoria_id not in self.inventario:
            self.inventario[gestoria_id] = {}
        
        # Agregar o actualizar el elemento
        self.inventario[gestoria_id][descripcion] = cantidad
        
        # Guardar y actualizar la vista
        self.guardar_inventario()
        self.cargar_inventario_gestoria()
        
        QMessageBox.information(self, "Éxito", f"Elemento agregado: {cantidad} x {descripcion}")
    
    def modificar_elemento(self):
        """Modifica el elemento seleccionado en el inventario"""
        item_seleccionado = self.lista_inventario.currentItem()
        
        if not item_seleccionado:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un elemento para modificar.")
            return
        
        descripcion_actual = item_seleccionado.data(Qt.UserRole)
        gestoria_id = self.combo_gestorias.currentData()
        nueva_descripcion = self.input_descripcion.text().strip()
        nueva_cantidad = self.input_cantidad.value()
        
        if not nueva_descripcion:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese una descripción para el elemento.")
            return
        
        # Si la descripción cambió, eliminar el elemento anterior y crear uno nuevo
        if descripcion_actual != nueva_descripcion:
            # Eliminar el elemento anterior
            if descripcion_actual in self.inventario[gestoria_id]:
                del self.inventario[gestoria_id][descripcion_actual]
        
        # Actualizar con los nuevos valores
        self.inventario[gestoria_id][nueva_descripcion] = nueva_cantidad
        
        # Guardar y actualizar la vista
        self.guardar_inventario()
        self.cargar_inventario_gestoria()
        
        QMessageBox.information(self, "Éxito", f"Elemento modificado: {nueva_cantidad} x {nueva_descripcion}")
    
    def eliminar_elemento(self):
        """Elimina el elemento seleccionado del inventario"""
        item_seleccionado = self.lista_inventario.currentItem()
        
        if not item_seleccionado:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un elemento para eliminar.")
            return
        
        descripcion = item_seleccionado.data(Qt.UserRole)
        gestoria_id = self.combo_gestorias.currentData()
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar '{descripcion}' del inventario?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            # Eliminar el elemento
            if gestoria_id in self.inventario and descripcion in self.inventario[gestoria_id]:
                del self.inventario[gestoria_id][descripcion]
                
                # Si la gestoría queda vacía, eliminarla del inventario
                if not self.inventario[gestoria_id]:
                    del self.inventario[gestoria_id]
                
                # Guardar y actualizar la vista
                self.guardar_inventario()
                self.cargar_inventario_gestoria()
                
                QMessageBox.information(self, "Éxito", f"Elemento '{descripcion}' eliminado correctamente.")
    
    def limpiar_seleccion(self):
        """Limpia la selección actual y los campos de entrada"""
        self.lista_inventario.clearSelection()
        self.limpiar_campos()
    
    def limpiar_campos(self):
        """Limpia los campos de entrada"""
        self.input_descripcion.clear()
        self.input_cantidad.setValue(1)
    
    def actualizar_combo_gestorias(self):
        """Actualiza el combo y la lista de gestorías con la lista actual"""
        self.combo_gestorias.clear()
        self.lista_gestorias.clear()
        
        # Ordenar las gestorías numéricamente
        sorted_gestorias = sorted(self.gestorias.keys(), key=int)
        for gestoria_id in sorted_gestorias:
            # Actualizar combo
            self.combo_gestorias.addItem(f"Gestoría {gestoria_id}: {self.gestorias[gestoria_id]}", gestoria_id)
            # Actualizar lista
            item = QListWidgetItem(f"Gestoría {gestoria_id}: {self.gestorias[gestoria_id]}")
            item.setData(Qt.UserRole, gestoria_id)
            self.lista_gestorias.addItem(item)
    
    def agregar_gestoria(self):
        """Agrega una nueva gestoría al sistema"""
        gestoria_id = self.input_gestoria_id.text().strip()
        nombre_gestoria = self.input_gestoria_nombre.text().strip()
        
        # Validaciones
        if not gestoria_id or not nombre_gestoria:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
            return
        
        # Validar que el ID sea numérico
        if not gestoria_id.isdigit():
            QMessageBox.warning(self, "Advertencia", "El ID de la gestoría debe ser un número.")
            return
        
        # Verificar si la gestoría ya existe
        if gestoria_id in self.gestorias:
            QMessageBox.warning(self, "Advertencia", "Ya existe una gestoría con ese ID.")
            return
        
        # Agregar la nueva gestoría
        self.gestorias[gestoria_id] = nombre_gestoria
        
        # Guardar en el archivo
        try:
            with open('gestorias.json', 'w', encoding='utf-8') as f:
                json.dump(self.gestorias, f, ensure_ascii=False, indent=2)
            
            # Actualizar el combo de gestorías
            self.actualizar_combo_gestorias()
            
            # Limpiar campos
            self.input_gestoria_id.clear()
            self.input_gestoria_nombre.clear()
            
            QMessageBox.information(self, "Éxito", f"Gestoría {gestoria_id}: {nombre_gestoria} agregada correctamente.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la gestoría: {str(e)}")
    
    def eliminar_gestoria(self):
        """Elimina la gestoría seleccionada del sistema"""
        # Obtener la gestoría seleccionada
        item_seleccionado = self.lista_gestorias.currentItem()
        if not item_seleccionado:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione una gestoría para eliminar.")
            return
        
        gestoria_id = item_seleccionado.data(Qt.UserRole)
        nombre_gestoria = self.gestorias.get(gestoria_id, "Desconocida")
        
        # Confirmar eliminación
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la Gestoría {gestoria_id}: {nombre_gestoria}?\n\n"
            "Esta acción también eliminará todo el inventario asociado a esta gestoría.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            try:
                # Eliminar la gestoría
                del self.gestorias[gestoria_id]
                
                # Eliminar su inventario si existe
                if gestoria_id in self.inventario:
                    del self.inventario[gestoria_id]
                
                # Guardar los cambios
                with open('gestorias.json', 'w', encoding='utf-8') as f:
                    json.dump(self.gestorias, f, ensure_ascii=False, indent=2)
                self.guardar_inventario()
                
                # Actualizar la interfaz
                self.actualizar_combo_gestorias()
                self.lista_inventario.clear()
                self.label_info_gestoria.clear()
                
                QMessageBox.information(self, "Éxito", f"Gestoría {gestoria_id} eliminada correctamente.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar la gestoría: {str(e)}")
    
    def exportar_a_excel(self):
        """Exporta todo el inventario a un archivo Excel"""
        try:
            # Crear directorio de exportaciones si no existe
            if not os.path.exists('exportaciones'):
                os.makedirs('exportaciones')
            
            # Generar nombre de archivo con fecha y hora
            fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            nombre_archivo = f"exportaciones/inventario_gestorias_{fecha_actual}.xlsx"
            
            # Preparar datos para exportación
            datos_exportacion = []
            
            for gestoria_id, elementos in self.inventario.items():
                gestoria_nombre = self.gestorias.get(gestoria_id, "Desconocida")
                
                for descripcion, cantidad in elementos.items():
                    datos_exportacion.append({
                        'Gestoría ID': gestoria_id,
                        'Gestoría Nombre': gestoria_nombre,
                        'Elemento': descripcion,
                        'Cantidad': cantidad
                    })
            
            # Crear DataFrame y exportar a Excel
            if datos_exportacion:
                df = pd.DataFrame(datos_exportacion)
                df.to_excel(nombre_archivo, index=False, engine='openpyxl')
                
                mensaje = f"✅ Exportación completada exitosamente!\n\n"
                mensaje += f"Archivo: {nombre_archivo}\n"
                mensaje += f"Total de registros exportados: {len(datos_exportacion)}\n"
                mensaje += f"Total de gestorías: {len(self.inventario)}"
                
                self.texto_exportacion.setText(mensaje)
                
                QMessageBox.information(self, "Exportación Exitosa", 
                                      f"Inventario exportado correctamente a:\n{nombre_archivo}")
            else:
                self.texto_exportacion.setText("❌ No hay datos para exportar.")
                QMessageBox.warning(self, "Sin Datos", "No hay datos de inventario para exportar.")
                
        except Exception as e:
            error_msg = f"❌ Error al exportar a Excel:\n{str(e)}"
            self.texto_exportacion.setText(error_msg)
            QMessageBox.critical(self, "Error de Exportación", f"Error al exportar: {str(e)}")

def main():
    """Función principal que inicia la aplicación"""
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana principal
    ventana = InventarioApp()
    ventana.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
