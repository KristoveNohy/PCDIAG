import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle("Hello")

        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Hello")
        self.label.move(100, 100)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click me!")
        self.b1.clicked.connect(self.clicked)


    def clicked(self):
        self.label.setText("Changed")

    def update(self):
        self.label.adjustSize()
        

def app():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

app()

    