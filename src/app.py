import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QToolBar, QAction, QStatusBar, QPushButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

sys.path.insert(0, 'src/borrar.py')
import borrar

sys.path.insert(0, 'src/funciones.py')
import funciones

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Merli")

        button_inicio = QPushButton('Iniciar', self)
        button_inicio.clicked.connect(borrar.main)
        button_inicio.resize(button_inicio.sizeHint())
        button_inicio.move(50, 20)

        button_cerrar = QPushButton('Apagar', self)
        button_cerrar.clicked.connect(funciones.cerrar)
        button_cerrar.resize(button_cerrar.sizeHint())
        button_cerrar.move(50, 50)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()