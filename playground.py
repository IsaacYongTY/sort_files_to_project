from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Sort Files to Folder")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.move(50,50)
        self.label.setText("My first label")
        

        self.button1 = QtWidgets.QPushButton(self)
        self.button1.setText('Click me!')
        self.button1.clicked.connect(self.button_clicked)
        self.button1.move(80, 80)

    def button_clicked(self):
        print('Clicked!')
        self.label.setText("YOur btton is pressed")
        self.label.repaint()
        self.update()

    def update(self):
        self.label.adjustSize()
        self.label.repaint()

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    
    win.show()
    sys.exit(app.exec_())

print('running')
window()