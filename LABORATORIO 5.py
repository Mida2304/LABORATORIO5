import sys
import time
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QInputDialog, QDialog, QLabel, QMessageBox
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtGui import QPixmap
import serial.tools.list_ports
from PyQt6 import QtWidgets

import serial
import numpy as np
import struct
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime
import os
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QWidget


class BluetoothThread(QThread):
    data_ready = pyqtSignal(list)

    def __init__(self, port, baud_rate=115200):
        super().__init__()
        self.port = port
        self.baud_rate = baud_rate

    def run(self):
        """Ejecución del hilo: lee datos del puerto serial."""
        try:
            self.ser = serial.Serial(self.port, self.baud_rate)
            self.running = True
            buffer = np.zeros(1000)
            while self.running:
                data = self.ser.read(50)
                if len(data) == 50:
                    try:
                        data = struct.unpack('50B', data)
                        for i in range(0, len(data), 2):
                            if i + 1 < len(data):  # Validar índices
                                value = data[i] * 100 + data[i + 1]
                                buffer = np.roll(buffer, -1)
                                buffer[-1] = value
                        self.data_ready.emit(buffer)  # Emitir datos procesados
                    except struct.error as e:
                        print("Error al desempaquetar datos:", e)
        except serial.SerialException as e:
            print("Error en el puerto serial:", e)
        finally:
            if hasattr(self, 'ser') and self.ser and self.ser.is_open:
                self.ser.close()

    def stop(self):
        """Detiene la lectura y cierra el puerto serial."""
        self.running = False
        self.wait()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interfaz de Señal EMG")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow { background-color: #eeaeff; }
            QPushButton { background-color: #A3B8E3; color: black; border-radius: 5px; padding: 8px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #A020F0; }
            QLabel { font-size: 16px; font-weight: bold; color: #4A6FA5; }
            QComboBox { background-color: #A3B8E3; color: black; font-size: 14px; font-weight: bold; }
        """)

        # Controles principales
        self.combo_puertos = QComboBox()
        self.connect_button = QPushButton("Conectar")
        self.connect_button.clicked.connect(self.conectar_bluetooth)

        self.start_button = QPushButton("Iniciar Gráfica")
        self.start_button.clicked.connect(self.iniciar_grafica)
        self.start_button.setEnabled(False)

        self.save_button = QPushButton("Guardar CSV")
        self.save_button.clicked.connect(self.guardar_csv)
        self.save_button.setEnabled(False)

        self.status_label = QLabel("Estado: No conectado")

        # Layout de la interfaz
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.combo_puertos)
        self.layout.addWidget(self.connect_button)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.save_button)
        self.layout.addWidget(self.status_label)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Variables internas
        self.hilo = None
        self.connected = False
        self.data = []
        self.time_data = []
        self.tiempo_inicial = 0

        self.actualizar_puertos()

    def actualizar_puertos(self):
        """Actualiza la lista de puertos disponibles."""
        self.combo_puertos.clear()
        puertos = serial.tools.list_ports.comports()
        for port in puertos:
            self.combo_puertos.addItem(port.device)

    def conectar_bluetooth(self):
        """Conecta o desconecta el hilo Bluetooth."""
        if not self.connected:
            try:
                self.port_selected = self.combo_puertos.currentText()
                if not self.port_selected:
                    raise ValueError("No se seleccionó un puerto.")
                
                # Crear el hilo de conexión Bluetooth
                self.hilo = BluetoothThread(self.port_selected)
                self.hilo.data_ready.connect(self.update_plot)
                self.hilo.start()
                
                self.connected = True
                self.connect_button.setText("Desconectar")
                self.start_button.setEnabled(True)
                self.status_label.setText(f"Estado: Conectado a {self.port_selected}")
            except Exception as e:
                QMessageBox.critical(self, "Error de conexión", str(e))
        else:
            self.hilo.stop()
            self.hilo = None
            self.connected = False
            self.connect_button.setText("Conectar")
            self.start_button.setEnabled(False)
            self.save_button.setEnabled(False)
            self.status_label.setText("Estado: No conectado")

    def iniciar_grafica(self):
        """Inicializa los datos y la gráfica."""
        if self.hilo and self.connected:
            self.data.clear()
            self.time_data.clear()
            self.ax.clear()
            self.ax.set_title("ECG en tiempo real")
            self.ax.set_xlabel("Tiempo (s)")
            self.ax.set_ylabel("Voltaje (V)")
            self.canvas.draw()
            self.tiempo_inicial = time.time()
            self.save_button.setEnabled(True)

    def update_plot(self, data):
        """Actualiza la gráfica con nuevos datos."""
        if not data:
            return

        tiempo_actual = time.time() - self.tiempo_inicial
        self.time_data.append(tiempo_actual)
        self.data.append(data[-1])

        self.ax.clear()
        self.ax.plot(self.time_data, self.data, color='purple')
        self.ax.set_title("Datos en tiempo real")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Voltaje (V)")
        self.canvas.draw()

    def guardar_csv(self):
        """Guarda los datos en un archivo CSV."""
        if not self.data or not self.time_data:
            QMessageBox.warning(self, "Sin datos", "No hay datos para guardar.")
            return

        nombre_archivo = f"datos_emg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(nombre_archivo, 'w') as f:
                f.write("Tiempo (s),Amplitud\n")
                for t, d in zip(self.time_data, self.data):
                    f.write(f"{t:.2f},{d:.2f}\n")
            QMessageBox.information(self, "Archivo guardado", f"Datos guardados en {nombre_archivo}")
        except Exception as e:
            QMessageBox.critical(self, "Error al guardar", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec())
