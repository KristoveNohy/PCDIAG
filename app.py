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
        
        self.ui.run_test_button.clicked.connect(self.run_test)
        self.ui.export_results_button.clicked.connect(self.export_results)
        self.startWorkers()
        self.start_usage_monitoring()
        self.initHardwareDiagnostics()

##################################################
######### VLASTNOSTI #############################
##################################################
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
            gpu = self.system["gpu"][index]
            self.ui.gpu_driver_version.setText(f"Verzia ovládača: {gpu['driver_version']}")
            self.ui.gpu_cuda_cores_label.setText(f"Počet CUDA jadier: {gpu['cuda_cores']}")
            self.ui.gpu_cuda_capability_label.setText(f"CUDA compute Capability: {gpu['cuda_cp']}")
            vram_gb = gpu['vram'] / (1024 ** 3)
            self.ui.gpu_compute_units_label.setText(f"počet výpočtových jednotiek {gpu["CU"]}")
            self.ui.gpu_vram_label.setText(f"VRAM kapacita: {vram_gb:.2f} GB")


    def populate_storage_combobox(self):
        self.ui.storage_combo_box.clear()
        for disk in self.system["storage"]:
            self.ui.storage_combo_box.addItem(disk["model"])

    def on_storage_selection_changed(self):
        index = self.ui.storage_combo_box.currentIndex()
        if 0 <= index < len(self.system["storage"]):
            disk = self.system["storage"][index]
            self.ui.storage_capacity_label.setText(f"Kapacita: {disk["size_gb"]:.2f} GB")
            self.ui.storage_read_label.setText(f"Rozhranie: {disk["interface"]}")
            self.ui.storage_write_label.setText(f"RPM: {disk["rpm"]}")
            self.ui.storage_type_label.setText(f"Typ: {disk["media_type"]}")

            
    def initHardwareDiagnostics(self):
        # Prvé načítanie údajov
        self.system = get_system_info()
        self.populate_gpu_combobox()
        self.populate_storage_combobox()
        self.ui.gpu_combo_box.currentIndexChanged.connect(self.on_gpu_selection_changed)
        self.ui.storage_combo_box.currentIndexChanged.connect(self.on_storage_selection_changed)

        self.on_storage_selection_changed()
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
        # disk = psutil.disk_usage('/')
        # total_gb = disk.total / (1024 ** 3)
        # self.ui.storage_capacity_label.setText(f"Kapacita: {total_gb:.2f} GB")
        # self.ui.storage_type_label.setText("Typ uložiska: SSD/HD")  # placeholder

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
##################################################
##################################################

##################################################
######## TESTOVANIE ##############################
##################################################
    def run_test(self) -> None:
        self.test_type = self.ui.benchmark_combo_box.currentText()
        benchmark_type = self.ui.benchmark_combo_box.currentIndex()
        self.ui.run_test_button.setEnabled(False)
        if benchmark_type == 0:
            self.start_inference_test()
        elif benchmark_type == 1:
            self.start_training_test()
        else:
            QtWidgets.QMessageBox.warning(self, "Varovanie", "Neznámy typ benchmarku.")

    def start_inference_test(self) -> None:
        from benchmark import InferenceWorker
        import torch
        # Výber zariadenia


        device_id = self.ui.device_combo_box.currentIndex()
        self.device_name = self.ui.device_combo_box.currentText()
        if device_id:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            device = torch.device('cpu')

        self.batch_size = self.ui.batch_size_spin_box.value()
        self.num_batches = self.ui.num_batches_spin_box.value()

        # Vytvorenie vlákna a workera pre inferenčný test
        self.inference_thread = QtCore.QThread()
        self.inference_worker = InferenceWorker(self.batch_size, self.num_batches, device)
        self.inference_worker.moveToThread(self.inference_thread)

        self.inference_thread.started.connect(self.inference_worker.run)
        self.inference_worker.progress.connect(self.update_inference_stats)
        self.inference_worker.logMessage.connect(self.log_message)
        self.inference_worker.finished.connect(self.on_inference_finished)
        self.inference_worker.finished.connect(self.inference_thread.quit)
        self.inference_worker.finished.connect(self.inference_worker.deleteLater)
        self.inference_thread.finished.connect(self.inference_thread.deleteLater)

        self.inference_thread.start()

    def update_inference_stats(self, processed, elapsed, avg_batch_time, fps) -> None:
        self.ui.elapsed_time_label.setText(f"uplynutý čas: {elapsed:.4f} s")
        self.ui.processed_items_label.setText(f"spracované batche: {processed}")
        self.ui.average_time_label.setText(f"pomer čas/batch: {avg_batch_time:.4f} s")
        self.ui.fps_label.setText(f"FPS: {fps:.2f}")

    def on_inference_finished(self, result_msg: str) -> None:
        self.ui.run_test_button.setEnabled(True)
        self.ui.export_results_button.setEnabled(True)
        QtWidgets.QMessageBox.information(self, "Výsledky inferenčného testu", result_msg)


    def start_training_test(self) -> None:
        from benchmark import TrainingWorker
        import torch
        self.ui.run_test_button.setEnabled(False)
        self.device_name = device_text = self.ui.device_combo_box.currentText()
        if device_text.startswith("GPU"):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            device = torch.device('cpu')

        self.batch_size = self.ui.batch_size_spin_box.value()
        self.num_batches = self.ui.num_batches_spin_box.value()

        self.training_thread = QtCore.QThread()
        self.training_worker = TrainingWorker(self.batch_size, self.num_batches, device)
        self.training_worker.moveToThread(self.training_thread)

        self.training_thread.started.connect(self.training_worker.run)
        self.training_worker.progress.connect(self.update_training_stats)
        self.training_worker.logMessage.connect(self.log_message)
        self.training_worker.finished.connect(self.on_training_finished)
        self.training_worker.finished.connect(self.training_thread.quit)
        self.training_worker.finished.connect(self.training_worker.deleteLater)
        self.training_thread.finished.connect(self.training_thread.deleteLater)

        self.training_thread.start()

    def update_training_stats(self, processed, elapsed, avg_batch_time) -> None:
        self.ui.elapsed_time_label.setText(f"uplynutý čas: {elapsed:.4f} s")
        self.ui.processed_items_label.setText(f"spracované batche: {processed}")
        self.ui.average_time_label.setText(f"pomer čas/batch: {avg_batch_time:.4f} s")
        self.ui.fps_label.setText("")
    
    def on_training_finished(self, result_msg: str) -> None:
        self.ui.run_test_button.setEnabled(True)
        self.ui.export_results_button.setEnabled(True)
        QtWidgets.QMessageBox.information(self, "Výsledky tréningového testu", result_msg)
        self.log_message(result_msg)

    def log_message(self, message: str) -> None:
        # Jednoduché logovanie do konzoly – môžete rozšíriť o logovanie do textového poľa
        print(message)

    # Spustenie vlákna pre monitorovanie využitia systémových zdrojov
    def start_usage_monitoring(self) -> None:
        self.usage_thread = QtCore.QThread()
        self.usage_worker = UsageWorker(interval=1.0)
        self.usage_worker.moveToThread(self.usage_thread)
        self.usage_thread.started.connect(self.usage_worker.run)
        self.usage_worker.usageUpdated.connect(self.update_usage_stats)
        self.usage_thread.start()

    def update_usage_stats(self, cpu, ram, gpu, vram) -> None:
        self.ui.cpu_usage_label.setText(f"využitie CPU: {cpu:.1f}%")
        self.ui.ram_usage_label.setText(f"využitie RAM: {ram:.1f}%")
        self.ui.gpu_usage_label.setText(f"využitie GPU: {gpu:.1f}%")
        self.ui.vram_usage_label.setText(f"využitie VRAM: {vram:.1f}%")

    def export_results(self) -> None:
        """
        Exportuje aktuálne výsledky z labelov do textového súboru.
        """
        # Získajte texty výsledkov
        results_text = (
            f"{self.test_type}\n"
            f"zariadenie: {self.device_name}\n"
            f"velkost batchu: {self.batch_size}\n"
            f"pocet batchov: {self.num_batches}\n\n"
            f"{self.ui.elapsed_time_label.text()}\n"
            f"{self.ui.processed_items_label.text()}\n"
            f"{self.ui.average_time_label.text()}\n"
            f"{self.ui.fps_label.text()}\n"
        )

        # Otvorte dialóg pre uloženie súboru
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Exportovať výsledky",
            "",
            "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)",
            options=options
        )
        
        if file_name:
            try:
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(results_text)
                QtWidgets.QMessageBox.information(self, "Export", "Výsledky boli úspešne exportované.")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Chyba", f"Export sa nepodaril: {e}")
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
