from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFileDialog, QInputDialog
import sys
import back
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mi aplicación")

        layout = QVBoxLayout()

        self.label = QLabel()

        self.button_load = QPushButton("Cargar archivo CSV")
        self.button_load.clicked.connect(self.select_csv_file)

        self.button_guardar_combinaciones = QPushButton("Guardar combinaciones")
        self.button_guardar_combinaciones.clicked.connect(self.guardar_combinaciones)
        self.button_guardar_combinaciones.setEnabled(False)

        self.button_unir_pares = QPushButton("Unir pares")
        self.button_unir_pares.clicked.connect(self.unir_pares)
        self.button_unir_pares.setEnabled(False)

        self.button_unir_rango = QPushButton("Unir rango")
        self.button_unir_rango.clicked.connect(self.unir_rango)
        self.button_unir_rango.setEnabled(False)

        layout.addWidget(self.button_load)
        layout.addWidget(self.button_guardar_combinaciones)
        layout.addWidget(self.button_unir_pares)
        layout.addWidget(self.button_unir_rango)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def select_csv_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Buscar CSV", "", "CSV Files (*.csv)")
        if filepath:
            filename = os.path.basename(filepath).replace('.csv', '')
            self.csv_filename = back.obtener_archivo(filename)
            if self.csv_filename is not None:
                self.label.setText(f"Archivo CSV cargado: {self.csv_filename}")
                self.button_guardar_combinaciones.setEnabled(True)
                self.button_unir_pares.setEnabled(True)
                self.button_unir_rango.setEnabled(True)
            else:
                self.label.setText(f"Archivo CSV no encontrado: {filename}")

    def unir_pares(self):
        pair, ok = QInputDialog.getText(self, "Unir pares", "Introduce el par de archivos CSV a unir:")
        if ok and pair:
            result = back.unir_pares(pair)  # Aquí pasamos el valor recibido del front a la función del back
            self.label.setText(f"Resultado de unir pares: {result}")

    def unir_rango(self):
        range_start, ok1 = QInputDialog.getInt(self, "Unir rango", "Introduce el inicio del rango:")
        range_end, ok2 = QInputDialog.getInt(self, "Unir rango", "Introduce el final del rango:")
        if ok1 and ok2:
            result = back.unir_rango(range_start, range_end)  # Aquí pasamos los valores recibidos del front a la función del back
            self.label.setText(f"Resultado de unir rango: {result}")

    def guardar_combinaciones(self):
        filename, ok = QInputDialog.getText(self, "Guardar combinaciones", "Introduce el nombre del archivo para guardar las combinaciones:")
        if ok and filename:
            back.guardar_combinaciones(filename)  # Aquí pasamos el valor recibido del front a la función del back
            self.label.setText(f"Combinaciones guardadas en el archivo: {filename}")
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()