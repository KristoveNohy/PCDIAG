import torch, time
import torchvision.models as models
from PyQt5 import QtCore
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
