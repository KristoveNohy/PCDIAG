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
