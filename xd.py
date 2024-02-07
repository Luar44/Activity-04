from PyQt6.QtWidgets import QApplication, QWidget, QLabel

# Crea una instancia de la aplicación
app = QApplication([])

# Crea una ventana
window = QWidget()
window.setWindowTitle("Ventana demasiado Cute")
window.setGeometry(100, 100, 300, 200)  # Establece las dimensiones de la ventana

# Crea una etiqueta con el mensaje
label = QLabel("Holi, soy muy cute 7w7 uwu", parent=window)
label.setGeometry(50, 50, 200, 30)  # Posición y tamaño de la etiqueta

# Muestra la ventana
window.show()

# Inicia el bucle de eventos
app.exec()
