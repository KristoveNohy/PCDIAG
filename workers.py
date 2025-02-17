from PyQt5 import QtCore

class TorchWorker(QtCore.QObject):
    torch_info_ready = QtCore.pyqtSignal(dict)

    def run(self):
        info = {}
        try:
            import torch
            # Použijeme priamo torch.cuda.is_available()
            info["cuda_available"] = torch.cuda.is_available()
        except ImportError:
            info["cuda_available"] = False
        self.torch_info_ready.emit(info)

class TensorWorker(QtCore.QObject):
    tensor_info_ready = QtCore.pyqtSignal(dict)

    def run(self):
        info = {}
        try:
            import tensorflow as tf
            info["cuda_available"] = tf.test.is_built_with_cuda()
        except ModuleNotFoundError:
            info["cuda_available"] = False
        
        self.tensor_info_ready.emit(info)

class UsageWorker(QtCore.QObject):
    usageUpdated = QtCore.pyqtSignal(float, float, float, float)  # CPU, RAM, GPU, VRAM
    finished = QtCore.pyqtSignal()

    def __init__(self, interval=1.0, parent=None):
        super().__init__(parent)
        self.interval = interval  # interval v sekundách
        self._running = True

    @QtCore.pyqtSlot()
    def run(self):
        import psutil, GPUtil, time
        while self._running:
            cpu_usage = psutil.cpu_percent(interval=None)
            ram_usage = psutil.virtual_memory().percent
            gpu_usage = 0.0
            vram_usage = 0.0
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu_usage = gpus[0].load * 100.0  # load je v rozmedzí 0-1
                    vram_usage = gpus[0].memoryUtil * 100.0
            except Exception as e:
                pass
            self.usageUpdated.emit(cpu_usage, ram_usage, gpu_usage, vram_usage)
            time.sleep(self.interval)
        self.finished.emit()

    def stop(self):
        self._running = False


