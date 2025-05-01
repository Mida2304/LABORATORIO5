import sys
import numpy as np
import nidaqmx
import csv
import time
from scipy.signal import butter, lfilter
from nidaqmx.stream_readers import AnalogSingleChannelReader
from PyQt6.QtWidgets import QMainWindow, QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

def diseno_filtro(fs):
    lowcut = 0.5
    highcut = 100
    order = 4
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

class Principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Adquisición de Señal ECG en Tiempo Real")
        self.setGeometry(200, 200, 800, 600)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.setStyleSheet("""
            QMainWindow { background-color: #eeaeff; }
            QPushButton {
                background-color: #A3B8E3;
                color: black;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #A020F0; }
            QLabel { font-size: 16px; font-weight: bold; color: #4A6FA5; }
        """)

        self.layout = QVBoxLayout(self.main_widget)

        self.button = QPushButton("Iniciar Grabación ECG")
        self.button.clicked.connect(self.iniciar_grabacion)
        self.layout.addWidget(self.button)

        self.stop_button = QPushButton("Detener Grabación")
        self.stop_button.clicked.connect(self.detener_grabacion)
        self.stop_button.setEnabled(False)
        self.layout.addWidget(self.stop_button)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Señal ECG en Tiempo Real")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Voltaje (V)")
        self.line, = self.ax.plot([], [], 'b-')

        self.data_buffer = []
        self.time_buffer = []

        self.sampling_rate = 1000  # Hz
        self.total_time = 5 * 60   # 5 minutos
        self.thread = None
        self.guardado = False

    def iniciar_grabacion(self):
        self.data_buffer = []
        self.time_buffer = []
        self.ax.cla()
        self.ax.set_title("Señal ECG en Tiempo Real")
        self.ax.set_xlabel("Tiempo (s)")
        self.ax.set_ylabel("Voltaje (V)")
        self.line, = self.ax.plot([], [], 'b-')
        self.guardado = False

        self.thread = AdquisicionDAQ(self.sampling_rate, self.total_time)
        self.thread.signal_data.connect(self.actualizar_grafica)
        self.thread.finished.connect(self.finalizar_grabacion)
        self.thread.start()

        self.button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.button.setText("Grabando...")

    def detener_grabacion(self):
        if self.thread and self.thread.isRunning():
            self.thread.stop()
            self.thread.wait()

    def actualizar_grafica(self, datos):
        for valor in datos:
            t = self.time_buffer[-1] + (1 / self.sampling_rate) if self.time_buffer else 0
            self.data_buffer.append(valor)
            self.time_buffer.append(t)

        limite = self.sampling_rate * 5
        self.line.set_data(self.time_buffer[-limite:], self.data_buffer[-limite:])
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

    def finalizar_grabacion(self):
        if self.guardado:
            return
        self.guardado = True

        self.button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.button.setText("Iniciar Grabación ECG")
        print("Grabación finalizada.")

        try:
            with open("datos_ecg.csv", mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Tiempo (s)", "Voltaje (V)"])
                for t, v in zip(self.time_buffer, self.data_buffer):
                    writer.writerow([t, v])
            print("Datos guardados en datos_ecg.csv")

            with open("datos_ecg.txt", mode='w') as file:
                file.write("Tiempo (s)\tVoltaje (V)\n")
                for t, v in zip(self.time_buffer, self.data_buffer):
                    file.write(f"{t:.4f}\t{v:.6f}\n")
            print("Datos guardados en datos_ecg.txt")

            self.figure.savefig("grafica_ecg.png")
            print("Gráfica guardada como grafica_ecg.png")
        except Exception as e:
            print(f"Error al guardar los datos: {e}")

class AdquisicionDAQ(QThread):
    signal_data = pyqtSignal(list)

    def __init__(self, fs, duracion):
        super().__init__()
        self.fs = fs
        self.duracion = duracion
        self.running = True
        self.b, self.a = diseno_filtro(fs)  # Coeficientes del filtro
        self.zi = np.zeros(max(len(self.a), len(self.b)) - 1)  # Condiciones iniciales en cero

    def run(self):
        try:
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan("Dev6/ai1")
                task.timing.cfg_samp_clk_timing(rate=self.fs, sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS)
                reader = AnalogSingleChannelReader(task.in_stream)

                buffer = np.zeros(100, dtype=np.float64)
                start_time = time.time()

                while self.running and (time.time() - start_time < self.duracion):
                    reader.read_many_sample(buffer, number_of_samples_per_channel=len(buffer), timeout=1.0)

                    # Filtrar datos
                    datos_filtrados, self.zi = lfilter(self.b, self.a, buffer, zi=self.zi)

                    self.signal_data.emit(datos_filtrados.tolist())

        except Exception as e:
            print(f"Error de adquisición: {e}")
        finally:
            self.running = False
            self.finished.emit()

    def stop(self):
        self.running = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Principal()
    ventana.show()
    sys.exit(app.exec())
