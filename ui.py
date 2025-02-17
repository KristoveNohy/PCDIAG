from PyQt5 import QtCore, QtWidgets
class Ui_MainWindow:
    def setupUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        # Nastavenie hlavného okna
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        # Vytvorenie centrálneho widgetu a hlavného layoutu
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setObjectName("grid_layout")

        # Pridanie licenčného labelu
        self.createLicenceLabel()
        # Vytvorenie a naplnenie TabWidgetu
        self.createTabWidget()

        # Umiestnenie TabWidgetu do hlavného layoutu
        self.grid_layout.addWidget(self.tab_widget, 0, 0)
        MainWindow.setCentralWidget(self.central_widget)

        # Nastavenie textov widgetov a konečné prepojenie signálov
        self.retranslateUi(MainWindow)
        self.tab_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def createLicenceLabel(self) -> None:
        self.licence_label = QtWidgets.QLabel(self.central_widget)
        self.licence_label.setObjectName("licence_label")
        self.grid_layout.addWidget(self.licence_label, 1, 0, 1, 1, QtCore.Qt.AlignBottom)

    def createTabWidget(self) -> None:
        self.tab_widget = QtWidgets.QTabWidget(self.central_widget)
        self.tab_widget.setEnabled(True)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                              QtWidgets.QSizePolicy.MinimumExpanding)
        size_policy.setHeightForWidth(self.tab_widget.sizePolicy().hasHeightForWidth())
        self.tab_widget.setSizePolicy(size_policy)
        self.tab_widget.setObjectName("tab_widget")

        # Vytvorenie jednotlivých kariet
        self.createPCPropertiesTab()
        self.createTestingTab()
        self.createInfoTab()

    def createPCPropertiesTab(self) -> None:
        # Tab pre vlastnosti PC
        self.pc_properties_tab = QtWidgets.QWidget()
        self.pc_properties_tab.setObjectName("pc_properties_tab")
        self.pc_properties_layout = QtWidgets.QVBoxLayout(self.pc_properties_tab)
        self.pc_properties_layout.setObjectName("pc_properties_layout")

        # Rozloženie pre hardvérové parametre (CPU, Uložisko, RAM)
        self.createHardwareParamsLayout()
        # Rozloženie pre GPU a Software parametre
        self.createGpuSoftwareLayout()

        self.tab_widget.addTab(self.pc_properties_tab, "")

    def createHardwareParamsLayout(self) -> None:
        self.hardware_params_layout = QtWidgets.QHBoxLayout()
        self.hardware_params_layout.setObjectName("hardware_params_layout")
        self.createCpuGroup()
        self.createStorageGroup()
        self.createRamGroup()
        self.pc_properties_layout.addLayout(self.hardware_params_layout)

    def createCpuGroup(self) -> None:
        self.cpu_group_box = QtWidgets.QGroupBox(self.pc_properties_tab)
        self.cpu_group_box.setObjectName("cpu_group_box")
        self.cpu_grid_layout = QtWidgets.QGridLayout(self.cpu_group_box)
        self.cpu_grid_layout.setObjectName("cpu_grid_layout")

        self.cpu_name_label = QtWidgets.QLabel(self.cpu_group_box)
        self.cpu_name_label.setObjectName("cpu_name_label")
        self.cpu_grid_layout.addWidget(self.cpu_name_label, 0, 0)

        self.cpu_logical_label = QtWidgets.QLabel(self.cpu_group_box)
        self.cpu_logical_label.setObjectName("cpu_logical_label")
        self.cpu_grid_layout.addWidget(self.cpu_logical_label, 1, 0)

        self.cpu_physical_label = QtWidgets.QLabel(self.cpu_group_box)
        self.cpu_physical_label.setObjectName("cpu_physical_label")
        self.cpu_grid_layout.addWidget(self.cpu_physical_label, 2, 0)

        self.cpu_freq_label = QtWidgets.QLabel(self.cpu_group_box)
        self.cpu_freq_label.setObjectName("cpu_freq_label")
        self.cpu_grid_layout.addWidget(self.cpu_freq_label, 3, 0)

        self.hardware_params_layout.addWidget(self.cpu_group_box)

    def createStorageGroup(self) -> None:
        self.storage_group_box = QtWidgets.QGroupBox(self.pc_properties_tab)
        self.storage_group_box.setObjectName("storage_group_box")
        self.storage_grid_layout = QtWidgets.QGridLayout(self.storage_group_box)
        self.storage_grid_layout.setObjectName("storage_grid_layout")

        self.storage_combo_box = QtWidgets.QComboBox(self.storage_group_box)
        self.storage_combo_box.setObjectName("storage_combo_box")
        self.storage_combo_box.addItem("Disk #0")
        self.storage_grid_layout.addWidget(self.storage_combo_box, 0, 0)

        self.storage_type_label = QtWidgets.QLabel(self.storage_group_box)
        self.storage_type_label.setObjectName("storage_type_label")
        self.storage_grid_layout.addWidget(self.storage_type_label, 1, 0)

        self.storage_read_label = QtWidgets.QLabel(self.storage_group_box)
        self.storage_read_label.setObjectName("storage_read_label")
        self.storage_grid_layout.addWidget(self.storage_read_label, 2, 0)

        self.storage_write_label = QtWidgets.QLabel(self.storage_group_box)
        self.storage_write_label.setObjectName("storage_write_label")
        self.storage_grid_layout.addWidget(self.storage_write_label, 3, 0)

        self.storage_capacity_label = QtWidgets.QLabel(self.storage_group_box)
        self.storage_capacity_label.setObjectName("storage_capacity_label")
        self.storage_grid_layout.addWidget(self.storage_capacity_label, 4, 0)

        self.hardware_params_layout.addWidget(self.storage_group_box)

    def createRamGroup(self) -> None:
        self.ram_group_box = QtWidgets.QGroupBox(self.pc_properties_tab)
        self.ram_group_box.setObjectName("ram_group_box")
        self.ram_grid_layout = QtWidgets.QGridLayout(self.ram_group_box)
        self.ram_grid_layout.setObjectName("ram_grid_layout")

        self.ram_total_label = QtWidgets.QLabel(self.ram_group_box)
        self.ram_total_label.setObjectName("ram_total_label")
        self.ram_grid_layout.addWidget(self.ram_total_label, 0, 0)

        self.ram_channels_label = QtWidgets.QLabel(self.ram_group_box)
        self.ram_channels_label.setObjectName("ram_channels_label")
        self.ram_grid_layout.addWidget(self.ram_channels_label, 1, 0)

        self.ram_type_label = QtWidgets.QLabel(self.ram_group_box)
        self.ram_type_label.setObjectName("ram_type_label")
        self.ram_grid_layout.addWidget(self.ram_type_label, 2, 0)

        self.ram_freq_label = QtWidgets.QLabel(self.ram_group_box)
        self.ram_freq_label.setObjectName("ram_freq_label")
        self.ram_grid_layout.addWidget(self.ram_freq_label, 3, 0)

        self.hardware_params_layout.addWidget(self.ram_group_box)

    def createGpuSoftwareLayout(self) -> None:
        self.gpu_software_layout = QtWidgets.QHBoxLayout()
        self.gpu_software_layout.setObjectName("gpu_software_layout")
        self.createGpuGroup()
        self.createSoftwareGroup()
        self.pc_properties_layout.addLayout(self.gpu_software_layout)

    def createGpuGroup(self) -> None:
        self.gpu_group_box = QtWidgets.QGroupBox(self.pc_properties_tab)
        self.gpu_group_box.setObjectName("gpu_group_box")
        self.gpu_grid_layout = QtWidgets.QGridLayout(self.gpu_group_box)
        self.gpu_grid_layout.setObjectName("gpu_grid_layout")

        self.gpu_combo_box = QtWidgets.QComboBox(self.gpu_group_box)
        self.gpu_combo_box.setObjectName("gpu_combo_box")
        self.gpu_combo_box.addItem("GPU #0")
        self.gpu_grid_layout.addWidget(self.gpu_combo_box, 0, 0)


        # Layout pre GPU parametre
        gpu_params_layout = QtWidgets.QGridLayout()
        gpu_params_layout.setContentsMargins(20, 20, 20, 20)
        gpu_params_layout.setObjectName("gpu_params_layout")

        self.gpu_vram_label = QtWidgets.QLabel(self.gpu_group_box)
        self.gpu_vram_label.setObjectName("gpu_vram_label")
        gpu_params_layout.addWidget(self.gpu_vram_label, 0, 0)


        self.gpu_cuda_cores_label = QtWidgets.QLabel(self.gpu_group_box)
        self.gpu_cuda_cores_label.setObjectName("gpu_cuda_cores_label")
        gpu_params_layout.addWidget(self.gpu_cuda_cores_label, 1, 0)

        self.gpu_cuda_capability_label = QtWidgets.QLabel(self.gpu_group_box)
        self.gpu_cuda_capability_label.setObjectName("gpu_cuda_capability_label")
        gpu_params_layout.addWidget(self.gpu_cuda_capability_label, 2, 0)

        self.gpu_compute_units_label = QtWidgets.QLabel(self.gpu_group_box)
        self.gpu_compute_units_label.setObjectName("gpu_compute_units_label")
        gpu_params_layout.addWidget(self.gpu_compute_units_label, 3, 0)

        self.gpu_driver_version = QtWidgets.QLabel(self.gpu_group_box)
        self.gpu_driver_version.setObjectName("gpu_driver_version")
        gpu_params_layout.addWidget(self.gpu_driver_version, 4, 0)

        self.gpu_grid_layout.addLayout(gpu_params_layout, 1, 0, 1, 2)
        self.gpu_software_layout.addWidget(self.gpu_group_box)

    def createSoftwareGroup(self) -> None:
        self.software_group_box = QtWidgets.QGroupBox(self.pc_properties_tab)
        self.software_group_box.setObjectName("software_group_box")
        self.software_grid_layout = QtWidgets.QGridLayout(self.software_group_box)
        self.software_grid_layout.setObjectName("software_grid_layout")

        self.python_label = QtWidgets.QLabel(self.software_group_box)
        self.python_label.setObjectName("python_label")
        self.software_grid_layout.addWidget(self.python_label, 0, 0)

        self.cuda_support_label = QtWidgets.QLabel(self.software_group_box)
        self.cuda_support_label.setObjectName("cuda_support_label")
        self.software_grid_layout.addWidget(self.cuda_support_label, 1, 0)

        self.cudnn_support_label = QtWidgets.QLabel(self.software_group_box)
        self.cudnn_support_label.setObjectName("cudnn_support_label")
        self.software_grid_layout.addWidget(self.cudnn_support_label, 2, 0)

        self.numpy_label = QtWidgets.QLabel(self.software_group_box)
        self.numpy_label.setObjectName("numpy_label")
        self.software_grid_layout.addWidget(self.numpy_label, 3, 0)

        self.scipy_label = QtWidgets.QLabel(self.software_group_box)
        self.scipy_label.setObjectName("scipy_label")
        self.software_grid_layout.addWidget(self.scipy_label, 4, 0)

        self.pandas_label = QtWidgets.QLabel(self.software_group_box)
        self.pandas_label.setObjectName("pandas_label")
        self.software_grid_layout.addWidget(self.pandas_label, 5, 0)

        self.pytorch_label = QtWidgets.QLabel(self.software_group_box)
        self.pytorch_label.setObjectName("pytorch_label")
        self.software_grid_layout.addWidget(self.pytorch_label, 6, 0)

        self.tensorflow_label = QtWidgets.QLabel(self.software_group_box)
        self.tensorflow_label.setObjectName("tensorflow_label")
        self.software_grid_layout.addWidget(self.tensorflow_label, 7, 0)

        self.torch_cuda_support_label = QtWidgets.QLabel(self.software_group_box)
        self.torch_cuda_support_label.setObjectName("torch_cuda_support_label")
        self.software_grid_layout.addWidget(self.torch_cuda_support_label, 8, 0)

        self.tensorflow_cuda_support_label = QtWidgets.QLabel(self.software_group_box)
        self.tensorflow_cuda_support_label.setObjectName("tensorflow_cuda_support_label")
        self.software_grid_layout.addWidget(self.tensorflow_cuda_support_label, 9, 0)

        self.gpu_software_layout.addWidget(self.software_group_box)

    def createTestingTab(self) -> None:
        # Tab pre testovanie
        self.testing_tab = QtWidgets.QWidget()
        self.testing_tab.setObjectName("testing_tab")
        self.testing_layout = QtWidgets.QVBoxLayout(self.testing_tab)
        self.testing_layout.setObjectName("testing_layout")

        self.createLoadGroup()
        self.createTestMethodGroup()
        self.createResultsGroup()

        self.tab_widget.addTab(self.testing_tab, "")

    def createLoadGroup(self) -> None:
        self.load_group_box = QtWidgets.QGroupBox(self.testing_tab)
        self.load_group_box.setObjectName("load_group_box")
        self.load_grid_layout = QtWidgets.QGridLayout(self.load_group_box)
        self.load_grid_layout.setObjectName("load_grid_layout")

        self.cpu_usage_label = QtWidgets.QLabel(self.load_group_box)
        self.cpu_usage_label.setObjectName("cpu_usage_label")
        self.load_grid_layout.addWidget(self.cpu_usage_label, 0, 0)

        self.gpu_usage_label = QtWidgets.QLabel(self.load_group_box)
        self.gpu_usage_label.setObjectName("gpu_usage_label")
        self.load_grid_layout.addWidget(self.gpu_usage_label, 1, 0)

        self.ram_usage_label = QtWidgets.QLabel(self.load_group_box)
        self.ram_usage_label.setObjectName("ram_usage_label")
        self.load_grid_layout.addWidget(self.ram_usage_label, 2, 0)

        self.vram_usage_label = QtWidgets.QLabel(self.load_group_box)
        self.vram_usage_label.setObjectName("vram_usage_label")
        self.load_grid_layout.addWidget(self.vram_usage_label, 3, 0)

        self.testing_layout.addWidget(self.load_group_box)

    def createTestMethodGroup(self) -> None:
        self.test_method_group_box = QtWidgets.QGroupBox(self.testing_tab)
        self.test_method_group_box.setObjectName("test_method_group_box")
        self.test_method_grid_layout = QtWidgets.QGridLayout(self.test_method_group_box)
        self.test_method_grid_layout.setObjectName("test_method_grid_layout")

        self.device_label = QtWidgets.QLabel(self.test_method_group_box)
        self.device_label.setObjectName("device_label")
        self.test_method_grid_layout.addWidget(self.device_label, 0, 0)

        self.run_test_button = QtWidgets.QPushButton(self.test_method_group_box)
        self.run_test_button.setObjectName("run_test_button")
        self.test_method_grid_layout.addWidget(self.run_test_button, 7, 0)

        self.device_combo_box = QtWidgets.QComboBox(self.test_method_group_box)
        self.device_combo_box.setObjectName("device_combo_box")
        self.device_combo_box.addItem("CPU")
        self.device_combo_box.addItem("GPU #0")
        self.test_method_grid_layout.addWidget(self.device_combo_box, 0, 2)

        self.benchmark_combo_box = QtWidgets.QComboBox(self.test_method_group_box)
        self.benchmark_combo_box.setObjectName("benchmark_combo_box")
        self.benchmark_combo_box.addItem("Inferenčný benchmark")
        self.benchmark_combo_box.addItem("treningový benchmark")
        self.test_method_grid_layout.addWidget(self.benchmark_combo_box, 1, 2)

        self.benchmark_label = QtWidgets.QLabel(self.test_method_group_box)
        self.benchmark_label.setObjectName("benchmark_label")
        self.test_method_grid_layout.addWidget(self.benchmark_label, 1, 0)

        self.export_results_button = QtWidgets.QPushButton(self.test_method_group_box)
        self.export_results_button.setEnabled(False)
        self.export_results_button.setObjectName("export_results_button")
        self.test_method_grid_layout.addWidget(self.export_results_button, 8, 0)

        self.testing_layout.addWidget(self.test_method_group_box)

    def createResultsGroup(self) -> None:
        self.results_group_box = QtWidgets.QGroupBox(self.testing_tab)
        self.results_group_box.setObjectName("results_group_box")
        self.results_grid_layout = QtWidgets.QGridLayout(self.results_group_box)
        self.results_grid_layout.setObjectName("results_grid_layout")

        self.elapsed_time_label = QtWidgets.QLabel(self.results_group_box)
        self.elapsed_time_label.setObjectName("elapsed_time_label")
        self.results_grid_layout.addWidget(self.elapsed_time_label, 0, 0)

        self.processed_items_label = QtWidgets.QLabel(self.results_group_box)
        self.processed_items_label.setObjectName("processed_items_label")
        self.results_grid_layout.addWidget(self.processed_items_label, 1, 0)

        self.average_time_label = QtWidgets.QLabel(self.results_group_box)
        self.average_time_label.setObjectName("average_time_label")
        self.results_grid_layout.addWidget(self.average_time_label, 2, 0)

        self.fps_label = QtWidgets.QLabel(self.results_group_box)
        self.fps_label.setObjectName("fps_label")
        self.results_grid_layout.addWidget(self.fps_label, 3, 0)

        self.testing_layout.addWidget(self.results_group_box)

    def createInfoTab(self) -> None:
        # Tab s informáciami o programe
        self.info_tab = QtWidgets.QWidget()
        self.info_tab.setObjectName("info_tab")
        self.info_layout = QtWidgets.QVBoxLayout(self.info_tab)
        self.info_layout.setObjectName("info_layout")

        self.info_label = QtWidgets.QLabel(self.info_tab)
        self.info_label.setObjectName("info_label")
        self.info_layout.addWidget(self.info_label, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.tab_widget.addTab(self.info_tab, "")

    def retranslateUi(self, MainWindow: QtWidgets.QMainWindow) -> None:
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PCDiagAI"))
        self.licence_label.setText(_translate("MainWindow",
            "<html><head/><body><p align=\"center\">Tento program je pod licenciou MIT</p></body></html>"))
        self.cpu_group_box.setTitle(_translate("MainWindow", "Procesor"))
        self.cpu_name_label.setText(_translate("MainWindow", "CPU: N/A"))
        self.cpu_logical_label.setText(_translate("MainWindow", "Pocet logickych jadier:"))
        self.cpu_physical_label.setText(_translate("MainWindow", "Pocet fyzických jadier:"))
        self.cpu_freq_label.setText(_translate("MainWindow", "Frekvencia:"))
        self.storage_group_box.setTitle(_translate("MainWindow", "Uložisko"))
        self.storage_combo_box.setItemText(0, _translate("MainWindow", "Disk #0"))
        self.storage_type_label.setText(_translate("MainWindow", "Typ uložiska:"))
        self.storage_read_label.setText(_translate("MainWindow", "Rýchlosť čítania:"))
        self.storage_write_label.setText(_translate("MainWindow", "Rýchlosť zápisu:"))
        self.storage_capacity_label.setText(_translate("MainWindow", "Kapacita:"))
        self.ram_group_box.setTitle(_translate("MainWindow", "Operačná Pamäť"))
        self.ram_total_label.setText(_translate("MainWindow", "Kapacita:"))
        self.ram_channels_label.setText(_translate("MainWindow", "Pocet kanalov:"))
        self.ram_type_label.setText(_translate("MainWindow", "Typ:"))
        self.ram_freq_label.setText(_translate("MainWindow", "Frekvencia:"))
        self.gpu_group_box.setTitle(_translate("MainWindow", "Grafické Karty"))
        self.gpu_combo_box.setItemText(0, _translate("MainWindow", "GPU #0"))
        self.gpu_driver_version.setText(_translate("MainWindow", "Názov:"))
        self.gpu_vram_label.setText(_translate("MainWindow", "VRAM kapacita:"))
        self.gpu_cuda_cores_label.setText(_translate("MainWindow", "Pocet CUDA jadier:"))
        self.gpu_cuda_capability_label.setText(_translate("MainWindow", "CUDA compute capability:"))
        self.gpu_compute_units_label.setText(_translate("MainWindow", "Počet výpočtových jednotiek:"))
        self.software_group_box.setTitle(_translate("MainWindow", "Software"))
        self.python_label.setText(_translate("MainWindow", "Python:"))
        self.cuda_support_label.setText(_translate("MainWindow", "CUDA:"))
        self.cudnn_support_label.setText(_translate("MainWindow", "CUDNN:"))
        self.numpy_label.setText(_translate("MainWindow", "NumPy:"))
        self.scipy_label.setText(_translate("MainWindow", "SciPy:"))
        self.pandas_label.setText(_translate("MainWindow", "Pandas:"))
        self.pytorch_label.setText(_translate("MainWindow", "PyTorch:"))
        self.tensorflow_label.setText(_translate("MainWindow", "TensorFlow:"))
        self.torch_cuda_support_label.setText(_translate("MainWindow", "Podpora Torch s CUDA:"))
        self.tensorflow_cuda_support_label.setText(_translate("MainWindow", "Podpora TensorFlow s CUDA:"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.pc_properties_tab), _translate("MainWindow", "Diagnostika PC"))
        self.load_group_box.setTitle(_translate("MainWindow", "zataženie"))
        self.cpu_usage_label.setText(_translate("MainWindow", "Využitie CPU:"))
        self.gpu_usage_label.setText(_translate("MainWindow", "Využitie GPU:"))
        self.ram_usage_label.setText(_translate("MainWindow", "Využitie RAM:"))
        self.vram_usage_label.setText(_translate("MainWindow", "Využitie VRAM:"))
        self.test_method_group_box.setTitle(_translate("MainWindow", "Spôsob testovania"))
        self.device_label.setText(_translate("MainWindow", "zariadenie:"))
        self.run_test_button.setText(_translate("MainWindow", "Spustiť test"))
        self.device_combo_box.setItemText(0, _translate("MainWindow", "CPU"))
        self.device_combo_box.setItemText(1, _translate("MainWindow", "GPU #0"))
        self.benchmark_combo_box.setItemText(0, _translate("MainWindow", "Inferenčný benchmark"))
        self.benchmark_combo_box.setItemText(1, _translate("MainWindow", "treningový benchmark"))
        self.benchmark_label.setText(_translate("MainWindow", "výber benchmarku:"))
        self.export_results_button.setText(_translate("MainWindow", "exportovať výsledky do ..."))
        self.results_group_box.setTitle(_translate("MainWindow", "výsledky"))
        self.elapsed_time_label.setText(_translate("MainWindow", "uplynulý čas:"))
        self.processed_items_label.setText(_translate("MainWindow", "Spracovaných prvkov:"))
        self.average_time_label.setText(_translate("MainWindow", "Priemerný čas na prvok:"))
        self.fps_label.setText(_translate("MainWindow", "FPS:"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.testing_tab), _translate("MainWindow", "Testovanie"))
        self.info_label.setText(_translate("MainWindow",
            "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Program na diagnostiku pc pre prácu s AI</span></p>"
            "<p><span style=\" font-weight:600;\">    Verzia: 1.0.0</span></p>"
            "<p><span style=\" font-weight:600;\">    Licencia: MIT</span></p>"
            "<p><span style=\" font-weight:600;\">    vytvoril: Kristian Lančarič</span></p>"
            "<p><span style=\" font-weight:600;\">    GitHub: </span>"
            "<a href=\"https://github.com/KristoveNohy/\"><span style=\" text-decoration: underline; color:#0000ff;\">KristoveNohy</span></a>"
            "</p></body></html>"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.info_tab), _translate("MainWindow", "Informácie o programe"))
