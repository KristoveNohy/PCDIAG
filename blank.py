import sys
import platform
import wmi
from PyQt5 import QtWidgets, QtCore

def get_all_gpu_info():
    """
    Získa zoznam GPU informácií ako dictionary.
    Každá položka obsahuje kľúče: "Name", "AdapterRAM" a "DriverVersion".
    """
    gpu_info = []
    if platform.system() == "Windows":
        try:
            c = wmi.WMI()
            for gpu in c.Win32_VideoController():
                name = gpu.Name
                # Prístup cez Properties_ pre AdapterRAM
                adapter_ram = gpu.Properties_["AdapterRAM"].Value
                # Ak je adapter_ram záporná, predpokladáme 32-bitové číslo a upravíme ho:
                if adapter_ram is not None and adapter_ram < 0:
                    adapter_ram += (1 << 32)
                driver_version = gpu.DriverVersion
                gpu_info.append({
                    "Name": name,
                    "AdapterRAM": adapter_ram,
                    "DriverVersion": driver_version,
                })
        except Exception as e:
            gpu_info.append({"Name": f"Chyba: {e}", "AdapterRAM": "N/A", "DriverVersion": "N/A"})
    else:
        # Pre iné platformy môžeš doplniť vlastný kód
        gpu_info.append({"Name": "GPU (placeholder)", "AdapterRAM": "N/A", "DriverVersion": "N/A"})
    return gpu_info

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Výber GPU")
        self.resize(500, 300)
        
        # Vytvoríme centrálny widget a layout
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
        layout = QtWidgets.QVBoxLayout(widget)
        
        # Vytvorenie QComboBoxu pre výber GPU
        self.gpu_combo = QtWidgets.QComboBox(self)
        layout.addWidget(self.gpu_combo)
        
        # Label, kde budú zobrazené detaily o GPU
        self.info_label = QtWidgets.QLabel(self)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        
        # Načítame informácie o GPU
        self.gpus = get_all_gpu_info()
        # Naplníme combobox názvami GPU
        for gpu in self.gpus:
            self.gpu_combo.addItem(gpu["Name"])
        
        # Pripojíme signál, ktorý reaguje na zmenu výberu
        self.gpu_combo.currentIndexChanged.connect(self.display_gpu_info)
        
        # Ak je aspoň jedna GPU, zobrazíme jej info
        if self.gpus:
            self.display_gpu_info(0)
    
    def display_gpu_info(self, index):
        if index < 0 or index >= len(self.gpus):
            self.info_label.setText("Informácie nie sú dostupné")
            return
        
        gpu = self.gpus[index]
        # Formátujeme informácie pre prehľadný výpis
        info_text = (
            f"Názov: {gpu.get('Name', 'N/A')}\n"
            f"VRAM: {gpu.get('AdapterRAM', 'N/A')} bajtov\n"
            f"Driver: {gpu.get('DriverVersion', 'N/A')}"
        )
        self.info_label.setText(info_text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
