import sys
import time
import torch
import torchvision.models as models
from PyQt5 import QtCore, QtWidgets

# Worker pre inferenčný test
class InferenceWorker(QtCore.QObject):
    # Signály: počet spracovaných batchov, uplynutý čas, priemerný čas na batch a FPS
    progress = QtCore.pyqtSignal(int, float, float, float)
    finished = QtCore.pyqtSignal(str)
    logMessage = QtCore.pyqtSignal(str)

    def __init__(self, batch_size, num_batches, device, parent=None):
        super().__init__(parent)
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.device = device
        self._isRunning = True

    @QtCore.pyqtSlot()
    def run(self):
        self.logMessage.emit("Načítavam model ResNet50 pre inferenciu...")
        model = models.resnet50(pretrained=True).to(self.device)
        model.eval()
        dummy_input = torch.randn(self.batch_size, 3, 224, 224).to(self.device)

        self.logMessage.emit("Prebieha warm-up pre inferenciu...")
        warmup_iterations = 10
        with torch.no_grad():
            for _ in range(warmup_iterations):
                _ = model(dummy_input)

        self.logMessage.emit("Spúšťam inferenčný test...")
        start_time = time.time()
        for i in range(self.num_batches):
            if not self._isRunning:
                break
            batch_start = time.time()
            with torch.no_grad():
                _ = model(dummy_input)
            batch_time = time.time() - batch_start
            elapsed = time.time() - start_time
            avg_batch_time = elapsed / (i + 1)
            fps = self.batch_size / avg_batch_time if avg_batch_time > 0 else 0
            # Vysielame aktuálne štatistiky
            self.progress.emit(i + 1, elapsed, avg_batch_time, fps)
        total_time = time.time() - start_time
        self.finished.emit(f"Inferenčný test dokončený: Celkový čas = {total_time:.4f} s")

    def stop(self):
        self._isRunning = False

# Worker pre tréningový test
class TrainingWorker(QtCore.QObject):
    # Signály: počet spracovaných batchov, uplynutý čas a priemerný čas na batch
    progress = QtCore.pyqtSignal(int, float, float)
    finished = QtCore.pyqtSignal(str)
    logMessage = QtCore.pyqtSignal(str)

    def __init__(self, batch_size, num_batches, device, parent=None):
        super().__init__(parent)
        self.batch_size = batch_size
        self.num_batches = num_batches
        self.device = device
        self._isRunning = True

    @QtCore.pyqtSlot()
    def run(self):
        self.logMessage.emit("Načítavam model ResNet50 pre tréning...")
        model = models.resnet50(pretrained=False).to(self.device)
        model.train()
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
        dummy_input = torch.randn(self.batch_size, 3, 224, 224).to(self.device)
        dummy_target = torch.randint(0, 1000, (self.batch_size,)).to(self.device)

        self.logMessage.emit("Prebieha warm-up pre tréning...")
        warmup_iterations = 5
        for _ in range(warmup_iterations):
            optimizer.zero_grad()
            outputs = model(dummy_input)
            loss = criterion(outputs, dummy_target)
            loss.backward()
            optimizer.step()

        self.logMessage.emit("Spúšťam tréningový test...")
        start_time = time.time()
        for i in range(self.num_batches):
            if not self._isRunning:
                break
            batch_start = time.time()
            optimizer.zero_grad()
            outputs = model(dummy_input)
            loss = criterion(outputs, dummy_target)
            loss.backward()
            optimizer.step()
            elapsed = time.time() - start_time
            avg_batch_time = elapsed / (i + 1)
            self.progress.emit(i + 1, elapsed, avg_batch_time)
        total_time = time.time() - start_time
        self.finished.emit(f"Tréningový test dokončený: Celkový čas = {total_time:.4f} s")

    def stop(self):
        self._isRunning = False

# Hlavná trieda GUI
class MyTestWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyTestWidget, self).__init__(parent)
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.testing_layout = None
        self.createTestingTab()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.tab_widget)

    def createTestingTab(self) -> None:
        # Vytvorenie tabu pre testovanie
        self.testing_tab = QtWidgets.QWidget()
        self.testing_tab.setObjectName("testing_tab")
        self.testing_layout = QtWidgets.QVBoxLayout(self.testing_tab)
        self.testing_layout.setObjectName("testing_layout")

        self.createLoadGroup()
        self.createTestMethodGroup()
        self.createResultsGroup()

        self.tab_widget.addTab(self.testing_tab, "Testovanie")

    def createLoadGroup(self) -> None:
        self.load_group_box = QtWidgets.QGroupBox(self.testing_tab)
        self.load_group_box.setObjectName("load_group_box")
        self.load_grid_layout = QtWidgets.QGridLayout(self.load_group_box)
        self.load_grid_layout.setObjectName("load_grid_layout")

        self.cpu_usage_label = QtWidgets.QLabel("CPU usage:", self.load_group_box)
        self.cpu_usage_label.setObjectName("cpu_usage_label")
        self.load_grid_layout.addWidget(self.cpu_usage_label, 0, 0)

        self.gpu_usage_label = QtWidgets.QLabel("GPU usage:", self.load_group_box)
        self.gpu_usage_label.setObjectName("gpu_usage_label")
        self.load_grid_layout.addWidget(self.gpu_usage_label, 1, 0)

        self.ram_usage_label = QtWidgets.QLabel("RAM usage:", self.load_group_box)
        self.ram_usage_label.setObjectName("ram_usage_label")
        self.load_grid_layout.addWidget(self.ram_usage_label, 2, 0)

        self.vram_usage_label = QtWidgets.QLabel("VRAM usage:", self.load_group_box)
        self.vram_usage_label.setObjectName("vram_usage_label")
        self.load_grid_layout.addWidget(self.vram_usage_label, 3, 0)

        self.testing_layout.addWidget(self.load_group_box)

    def createTestMethodGroup(self) -> None:
        self.test_method_group_box = QtWidgets.QGroupBox(self.testing_tab)
        self.test_method_group_box.setObjectName("test_method_group_box")
        self.test_method_grid_layout = QtWidgets.QGridLayout(self.test_method_group_box)
        self.test_method_grid_layout.setObjectName("test_method_grid_layout")

        self.device_label = QtWidgets.QLabel("Zariadenie:", self.test_method_group_box)
        self.device_label.setObjectName("device_label")
        self.test_method_grid_layout.addWidget(self.device_label, 0, 0)

        self.device_combo_box = QtWidgets.QComboBox(self.test_method_group_box)
        self.device_combo_box.setObjectName("device_combo_box")
        self.device_combo_box.addItem("CPU")
        self.device_combo_box.addItem("GPU #0")
        self.test_method_grid_layout.addWidget(self.device_combo_box, 0, 2)

        self.benchmark_label = QtWidgets.QLabel("Typ benchmarku:", self.test_method_group_box)
        self.benchmark_label.setObjectName("benchmark_label")
        self.test_method_grid_layout.addWidget(self.benchmark_label, 1, 0)

        self.benchmark_combo_box = QtWidgets.QComboBox(self.test_method_group_box)
        self.benchmark_combo_box.setObjectName("benchmark_combo_box")
        self.benchmark_combo_box.addItem("Inferenčný benchmark")
        self.benchmark_combo_box.addItem("Tréningový benchmark")
        self.test_method_grid_layout.addWidget(self.benchmark_combo_box, 1, 2)

        self.batch_size_label = QtWidgets.QLabel("Batch size:", self.test_method_group_box)
        self.batch_size_label.setObjectName("batch_size_label")
        self.test_method_grid_layout.addWidget(self.batch_size_label, 2, 0)

        self.batch_size_spin_box = QtWidgets.QSpinBox(self.test_method_group_box)
        self.batch_size_spin_box.setObjectName("batch_size_spin_box")
        self.batch_size_spin_box.setMinimum(1)
        self.batch_size_spin_box.setMaximum(1024)
        self.batch_size_spin_box.setValue(1)
        self.test_method_grid_layout.addWidget(self.batch_size_spin_box, 2, 2)

        self.num_batches_label = QtWidgets.QLabel("Počet batchov:", self.test_method_group_box)
        self.num_batches_label.setObjectName("num_batches_label")
        self.test_method_grid_layout.addWidget(self.num_batches_label, 3, 0)

        self.num_batches_spin_box = QtWidgets.QSpinBox(self.test_method_group_box)
        self.num_batches_spin_box.setObjectName("num_batches_spin_box")
        self.num_batches_spin_box.setMinimum(1)
        self.num_batches_spin_box.setMaximum(10000)
        self.num_batches_spin_box.setValue(100)
        self.test_method_grid_layout.addWidget(self.num_batches_spin_box, 3, 2)

        self.run_test_button = QtWidgets.QPushButton("Spustiť test", self.test_method_group_box)
        self.run_test_button.setObjectName("run_test_button")
        self.test_method_grid_layout.addWidget(self.run_test_button, 7, 0)

        self.export_results_button = QtWidgets.QPushButton("Exportovať výsledky", self.test_method_group_box)
        self.export_results_button.setEnabled(False)
        self.export_results_button.setObjectName("export_results_button")
        self.test_method_grid_layout.addWidget(self.export_results_button, 8, 0)

        self.testing_layout.addWidget(self.test_method_group_box)

        # Pri stlačení tlačidla sa spustí metóda run_test, ktorá vyberie správny test
        self.run_test_button.clicked.connect(self.run_test)

    def createResultsGroup(self) -> None:
        self.results_group_box = QtWidgets.QGroupBox(self.testing_tab)
        self.results_group_box.setObjectName("results_group_box")
        self.results_grid_layout = QtWidgets.QGridLayout(self.results_group_box)
        self.results_grid_layout.setObjectName("results_grid_layout")

        self.elapsed_time_label = QtWidgets.QLabel("Elapsed time:", self.results_group_box)
        self.elapsed_time_label.setObjectName("elapsed_time_label")
        self.results_grid_layout.addWidget(self.elapsed_time_label, 0, 0)

        self.processed_items_label = QtWidgets.QLabel("Processed batches:", self.results_group_box)
        self.processed_items_label.setObjectName("processed_items_label")
        self.results_grid_layout.addWidget(self.processed_items_label, 1, 0)

        self.average_time_label = QtWidgets.QLabel("Avg time per batch:", self.results_group_box)
        self.average_time_label.setObjectName("average_time_label")
        self.results_grid_layout.addWidget(self.average_time_label, 2, 0)

        self.fps_label = QtWidgets.QLabel("FPS:", self.results_group_box)
        self.fps_label.setObjectName("fps_label")
        self.results_grid_layout.addWidget(self.fps_label, 3, 0)

        self.testing_layout.addWidget(self.results_group_box)

    # Spustenie testu podľa výberu (inferencia / tréning)
    def run_test(self) -> None:
        benchmark_type = self.benchmark_combo_box.currentText()
        if benchmark_type == "Inferenčný benchmark":
            self.start_inference_test()
        elif benchmark_type == "Tréningový benchmark":
            self.start_training_test()
        else:
            QtWidgets.QMessageBox.warning(self, "Varovanie", "Neznámy typ benchmarku.")

    def start_inference_test(self) -> None:
        # Výber zariadenia
        device_text = self.device_combo_box.currentText()
        if device_text.startswith("GPU"):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            device = torch.device('cpu')

        batch_size = self.batch_size_spin_box.value()
        num_batches = self.num_batches_spin_box.value()

        # Vytvorenie vlákna a workera pre inferenčný test
        self.inference_thread = QtCore.QThread()
        self.inference_worker = InferenceWorker(batch_size, num_batches, device)
        self.inference_worker.moveToThread(self.inference_thread)

        self.inference_thread.started.connect(self.inference_worker.run)
        self.inference_worker.progress.connect(self.update_inference_stats)
        self.inference_worker.logMessage.connect(self.log_message)
        self.inference_worker.finished.connect(self.on_inference_finished)
        self.inference_worker.finished.connect(self.inference_thread.quit)
        self.inference_worker.finished.connect(self.inference_worker.deleteLater)
        self.inference_thread.finished.connect(self.inference_thread.deleteLater)

        self.inference_thread.start()

    def start_training_test(self) -> None:
        device_text = self.device_combo_box.currentText()
        if device_text.startswith("GPU"):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        else:
            device = torch.device('cpu')

        batch_size = self.batch_size_spin_box.value()
        num_batches = self.num_batches_spin_box.value()

        self.training_thread = QtCore.QThread()
        self.training_worker = TrainingWorker(batch_size, num_batches, device)
        self.training_worker.moveToThread(self.training_thread)

        self.training_thread.started.connect(self.training_worker.run)
        self.training_worker.progress.connect(self.update_training_stats)
        self.training_worker.logMessage.connect(self.log_message)
        self.training_worker.finished.connect(self.on_training_finished)
        self.training_worker.finished.connect(self.training_thread.quit)
        self.training_worker.finished.connect(self.training_worker.deleteLater)
        self.training_thread.finished.connect(self.training_thread.deleteLater)

        self.training_thread.start()

    # Aktualizácia štatistík pre inferenčný test
    def update_inference_stats(self, processed, elapsed, avg_batch_time, fps) -> None:
        self.elapsed_time_label.setText(f"Elapsed time: {elapsed:.4f} s")
        self.processed_items_label.setText(f"Processed batches: {processed}")
        self.average_time_label.setText(f"Avg time per batch: {avg_batch_time:.4f} s")
        self.fps_label.setText(f"FPS: {fps:.2f}")

    # Aktualizácia štatistík pre tréningový test
    def update_training_stats(self, processed, elapsed, avg_batch_time) -> None:
        self.elapsed_time_label.setText(f"Elapsed time: {elapsed:.4f} s")
        self.processed_items_label.setText(f"Processed batches: {processed}")
        self.average_time_label.setText(f"Avg time per batch: {avg_batch_time:.4f} s")
        self.fps_label.setText("FPS: N/A")

    def on_inference_finished(self, result_msg: str) -> None:
        QtWidgets.QMessageBox.information(self, "Výsledky inferenčného testu", result_msg)
        self.log_message(result_msg)

    def on_training_finished(self, result_msg: str) -> None:
        QtWidgets.QMessageBox.information(self, "Výsledky tréningového testu", result_msg)
        self.log_message(result_msg)

    def log_message(self, message: str) -> None:
        # Jednoduché logovanie do konzoly – môžete rozšíriť o logovanie do textového poľa
        print(message)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyTestWidget()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec_())
