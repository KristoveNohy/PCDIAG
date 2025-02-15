import sys
import psutil
import platform, time
from PyQt5 import QtCore, QtWidgets
from ui import Ui_MainWindow
from myfunctions import is_module_installed, getCPUname

# Pôvodná trieda UI zostáva nezmenená

# Hlavná trieda aplikácie, kde je pridaná diagnostika hardvéru
import time
import psutil

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Inicializácia pre diskové I/O
        self.last_disk_io = psutil.disk_io_counters()
        self.last_disk_time = time.time()

        self.initHardwareDiagnostics()

    def initHardwareDiagnostics(self):
        # Prvé načítanie údajov
        self.updateHardwareInfo()
        # Timer na periodickú aktualizáciu každých 5 sekúnd
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.updateHardwareInfo)
        self.timer.start(5000)

    def updateHardwareInfo(self):
        # CPU diagnostika
        cpu_logical = psutil.cpu_count(logical=True)
        cpu_physical = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        freq_str = f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A"
        cpu_name = platform.processor() or "N/A"
        self.ui.cpu_name_label.setText(f"CPU: {cpu_name}")
        self.ui.cpu_logical_label.setText(f"Pocet logickych jadier: {cpu_logical}")
        self.ui.cpu_physical_label.setText(f"Pocet fyzických jadier: {cpu_physical}")
        self.ui.cpu_freq_label.setText(f"Frekvencia: {freq_str}")

        # Úložisko - výpočet rýchlosti čítania a zápisu
        disk = psutil.disk_usage('/')
        total_gb = disk.total / (1024 ** 3)
        self.ui.storage_capacity_label.setText(f"Kapacita: {total_gb:.2f} GB")
        self.ui.storage_type_label.setText("Typ uložiska: SSD/HD")  # placeholder

        # Meranie rýchlosti I/O
        current_disk_io = psutil.disk_io_counters()
        current_time = time.time()
        interval = current_time - self.last_disk_time
        if interval > 0:
            # Výpočet rozdielu prečítaných a zapísaných bajtov
            read_bytes = current_disk_io.read_bytes - self.last_disk_io.read_bytes
            write_bytes = current_disk_io.write_bytes - self.last_disk_io.write_bytes
            # Prepočet na MB/s
            read_speed = read_bytes / (1024 * 1024 * interval)
            write_speed = write_bytes / (1024 * 1024 * interval)
            self.ui.storage_read_label.setText(f"Rýchlosť čítania: {read_speed:.2f} MB/s")
            self.ui.storage_write_label.setText(f"Rýchlosť zápisu: {write_speed:.2f} MB/s")
        # Aktualizácia pre nasledujúce meranie
        self.last_disk_io = current_disk_io
        self.last_disk_time = current_time

        # Operačná pamäť
        mem = psutil.virtual_memory()
        total_ram_gb = mem.total / (1024 ** 3)
        self.ui.ram_total_label.setText(f"Kapacita: {total_ram_gb:.2f} GB")
        self.ui.ram_channels_label.setText("Pocet kanalov: N/A")
        self.ui.ram_type_label.setText("Typ: DDR4")  # placeholder
        self.ui.ram_freq_label.setText("Frekvencia: N/A")

        # GPU diagnostika
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                gpu = gpus[0]
                self.ui.gpu_name_label.setText(f"Názov: {gpu.name}")
                self.ui.gpu_vram_label.setText(f"VRAM kapacita: {gpu.memoryTotal} MB")
                self.ui.gpu_cuda_cores_label.setText("Pocet CUDA jadier: N/A")
                self.ui.gpu_cuda_capability_label.setText("CUDA compute capability: N/A")
                self.ui.gpu_compute_units_label.setText("Počet výpočtových jednotiek: N/A")
            else:
                self.ui.gpu_name_label.setText("N/A")
                self.ui.gpu_vram_label.setText("VRAM kapacita: N/A")
                self.ui.gpu_cuda_cores_label.setText("Pocet CUDA jadier: N/A")
                self.ui.gpu_cuda_capability_label.setText("CUDA compute capability: N/A")
                self.ui.gpu_compute_units_label.setText("Počet výpočtových jednotiek: N/A")
        except ImportError:
            self.ui.gpu_name_label.setText("N/A")
            self.ui.gpu_vram_label.setText("VRAM kapacita: N/A")
            self.ui.gpu_cuda_cores_label.setText("Pocet CUDA jadier: N/A")
            self.ui.gpu_cuda_capability_label.setText("CUDA compute capability: N/A")
            self.ui.gpu_compute_units_label.setText("Počet výpočtových jednotiek: N/A")

        # Software diagnostika
        self.ui.python_label.setText(f"Python: {platform.python_version()}")
        self.ui.cuda_support_label.setText("CUDA: N/A")
        self.ui.cudnn_support_label.setText("CUDNN: N/A")
        self.ui.opencl_label.setText("OpenCL: N/A")
        self.ui.numpy_label.setText(f"NumPy: {is_module_installed("numpy")}")
        self.ui.scipy_label.setText(f"SciPy: {is_module_installed("scipy")}")
        self.ui.pandas_label.setText(f"Pandas: {is_module_installed("pandas")}")
        self.ui.pytorch_label.setText(f"PyTorch: {is_module_installed("torch") if is_module_installed("torchvison") != "nenajdený" and is_module_installed("torchaudio") != "nenajdený" else "nenajdený"}")
        self.ui.tensorflow_label.setText(f"TensorFlow: {is_module_installed("tensorflow")}")
        self.ui.torch_cuda_support_label.setText("Podpora Torch s CUDA: N/A")
        self.ui.tensorflow_cuda_support_label.setText("Podpora TensorFlow s CUDA: N/A")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
