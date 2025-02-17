import sys
import psutil, wmi
import platform, time
from PyQt5 import QtCore, QtWidgets
from ui import Ui_MainWindow
from myfunctions import *
from workers import *

# Pôvodná trieda UI zostáva nezmenená

# Hlavná trieda aplikácie, kde je pridaná diagnostika hardvéru
import time
import psutil

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        

        self.startWorkers()
        self.initHardwareDiagnostics()

    def startWorkers(self):
        self.torch_thread = QtCore.QThread()
        self.tensor_thread = QtCore.QThread()

        self.torch_worker = TorchWorker()
        self.tensor_worker = TensorWorker()

        self.torch_worker.moveToThread(self.torch_thread)
        self.tensor_worker.moveToThread(self.tensor_thread)

        self.torch_thread.started.connect(self.torch_worker.run)
        self.tensor_thread.started.connect(self.tensor_worker.run)

        self.torch_worker.torch_info_ready.connect(self.onTorchInfoReady)
        self.tensor_worker.tensor_info_ready.connect(self.onTensorInfoReady)
        self.torch_thread.start()
        self.tensor_thread.start()

    def onTorchInfoReady(self, info):
        cuda_support = info.get("cuda_support", False)
        support_str = "s podporou CUDA" if cuda_support else "nie je"
        self.ui.torch_cuda_support_label.setText(f"Podpora Torch s CUDA: {support_str}")
        self.torch_thread.quit()
        self.torch_thread.wait()

    def onTensorInfoReady(self, info):
        cuda_support = info.get("cuda_support", False)
        support_str = "s podporou CUDA" if cuda_support else "nie je"
        self.ui.tensorflow_cuda_support_label.setText(f"Podpora TensorFlow s CUDA: {support_str}")
        self.tensor_thread.quit()
        self.tensor_thread.wait()

    def populate_gpu_combobox(self):
        self.ui.gpu_combo_box.clear()
        for gpu in self.system["gpu"]:
            self.ui.gpu_combo_box.addItem(gpu["name"])
    
    def on_gpu_selection_changed(self):
        index = self.ui.gpu_combo_box.currentIndex()
        if 0 <= index < len(self.system["gpu"]):
            print(index)
            gpu = self.system["gpu"][index]
            self.ui.gpu_name_label.setText(f"Názov: {gpu['name']}")
            vram_gb = gpu['vram'] / (1024 ** 3)
            self.ui.gpu_compute_units_label.setText(f"počet výpočtových jednotiek {gpu["CU"]}")
            self.ui.gpu_vram_label.setText(f"VRAM kapacita: {vram_gb:.2f} GB")

    def initHardwareDiagnostics(self):
        # Prvé načítanie údajov
        self.system = get_system_info()
        self.populate_gpu_combobox()
        self.ui.gpu_combo_box.currentIndexChanged.connect(self.on_gpu_selection_changed)

        self.on_gpu_selection_changed()
        self.updateHardwareInfo()
        # Timer na periodickú aktualizáciu každých 5 sekúnd
        

    def updateHardwareInfo(self):
        # CPU diagnostika
        cpu_freq = psutil.cpu_freq()
        freq_str = f"{cpu_freq.current:.2f} MHz" if cpu_freq else "N/A"
        cpu_name = self.system["cpu"]["name"] or "N/A"
        self.ui.cpu_name_label.setText(f"CPU: {cpu_name}")
        self.ui.cpu_logical_label.setText(f"Pocet logickych jadier: {self.system["cpu"]["logical_processors"]}")
        self.ui.cpu_physical_label.setText(f"Pocet fyzických jadier: {self.system["cpu"]["cores"]}")
        self.ui.cpu_freq_label.setText(f"Frekvencia: {freq_str}")

        # Úložisko - výpočet rýchlosti čítania a zápisu
        disk = psutil.disk_usage('/')
        total_gb = disk.total / (1024 ** 3)
        self.ui.storage_capacity_label.setText(f"Kapacita: {total_gb:.2f} GB")
        self.ui.storage_type_label.setText("Typ uložiska: SSD/HD")  # placeholder

        # Operačná pamäť
        mem = psutil.virtual_memory()
        total_ram_gb = mem.total / (1024 ** 3)
        self.ui.ram_total_label.setText(f"Kapacita: {total_ram_gb:.2f} GB")
        self.ui.ram_channels_label.setText(f"Pocet RAM : {len(self.system["ram"])}" )
        memtype = memtotext(self.system["ram"][0]["type"])
        self.ui.ram_type_label.setText(f"Typ: {memtype}")
        self.ui.ram_freq_label.setText(f"Frekvencia: {self.system["ram"][0]["speed_mhz"]}")

        # GPU diagnostika
        
        # self.ui.gpu_name_label.setText("N/A")
        # self.ui.gpu_vram_label.setText("VRAM kapacita: N/A")
        # self.ui.gpu_cuda_cores_label.setText("Pocet CUDA jadier: N/A")
        # self.ui.gpu_cuda_capability_label.setText("CUDA compute capability: N/A")
        # self.ui.gpu_compute_units_label.setText("Počet výpočtových jednotiek: N/A")

        # Software diagnostika
        self.ui.python_label.setText(f"Python: {platform.python_version()}")
        self.ui.cuda_support_label.setText(f"CUDA: {is_cuda()}")
        self.ui.cudnn_support_label.setText(f"CUDNN: {is_cudnn()}")
        self.ui.numpy_label.setText(f"NumPy: {is_module_installed("numpy")}")
        self.ui.scipy_label.setText(f"SciPy: {is_module_installed("scipy")}")
        self.ui.pandas_label.setText(f"Pandas: {is_module_installed("pandas")}")
        self.ui.pytorch_label.setText(f"PyTorch: {is_module_installed("torch")}")
        self.ui.tensorflow_label.setText(f"TensorFlow: {is_module_installed("tensorflow")}")
        self.ui.torch_cuda_support_label.setText(f"Podpora Torch s CUDA: načítavam...")
        self.ui.tensorflow_cuda_support_label.setText("Podpora TensorFlow s CUDA: načítavam...")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
