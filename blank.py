import sys
import torch
import torchvision.models as models
import time
import psutil
import GPUtil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

class BenchmarkThread(QThread):
    update_signal = pyqtSignal(dict)  # Signál na aktualizáciu GUI

    def run(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = models.resnet50(pretrained=True).to(device)
        model.eval()

        batch_size = 32
        input_tensor = torch.randn(batch_size, 3, 224, 224).to(device)
        num_iterations = 100

        torch.cuda.synchronize() if torch.cuda.is_available() else None
        start_time = time.time()

        for i in range(num_iterations):
            with torch.no_grad():
                model(input_tensor)

            # Priebežná aktualizácia GUI
            elapsed_time = time.time() - start_time
            time_per_batch = elapsed_time / (i + 1)
            latency = time_per_batch / batch_size * 1000
            fps = batch_size / time_per_batch

            gpu = GPUtil.getGPUs()[0] if torch.cuda.is_available() else None
            cpu_usage = psutil.cpu_percent()
            ram_usage = psutil.virtual_memory().used / (1024 ** 3)
            vram_usage = gpu.memoryUsed / 1024 if gpu else 0

            flops_per_image = 4.1 * (10 ** 9)
            flops = (flops_per_image * fps) / (10 ** 12)

            self.update_signal.emit({
                "FPS": f"{fps:.2f}",
                "Latencia (ms)": f"{latency:.2f}",
                "FLOPs (TFLOPs)": f"{flops:.2f}",
                "CPU Load": f"{cpu_usage:.1f}%",
                "RAM Usage (GB)": f"{ram_usage:.2f}",
                "VRAM Usage (GB)": f"{vram_usage:.2f}"
            })

        torch.cuda.synchronize() if torch.cuda.is_available() else None

class BenchmarkApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AI Benchmark - ResNet-50")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()

        self.benchmark_btn = QPushButton("Spustiť Benchmark")
        self.benchmark_btn.clicked.connect(self.run_benchmark)
        self.layout.addWidget(self.benchmark_btn)

        self.result_labels = {}
        for text in ["FPS", "Latencia (ms)", "FLOPs (TFLOPs)", "CPU Load", "RAM Usage (GB)", "VRAM Usage (GB)"]:
            label = QLabel(f"{text}: -")
            self.layout.addWidget(label)
            self.result_labels[text] = label

        self.setLayout(self.layout)

    def run_benchmark(self):
        self.benchmark_btn.setEnabled(False)  # Deaktivovať tlačidlo počas benchmarku
        self.benchmark_thread = BenchmarkThread()
        self.benchmark_thread.update_signal.connect(self.update_results)
        self.benchmark_thread.finished.connect(lambda: self.benchmark_btn.setEnabled(True))
        self.benchmark_thread.start()

    def update_results(self, results):
        for key, value in results.items():
            self.result_labels[key].setText(f"{key}: {value}")

# Spustenie aplikácie
app = QApplication(sys.argv)
window = BenchmarkApp()
window.show()
sys.exit(app.exec_())
