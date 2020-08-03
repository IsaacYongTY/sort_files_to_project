from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys

print('test')

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("Sort Files to Project")
        self.initUI()

    def initUI(self):
        self.button = QtWidgets.QPushButton(self)
        self.button.setText('Sort')
        self.button.move(50,50)
        self.button.clicked.connect(self.sort_files)


        self.selected_files_label = QtWidgets.QLabel(self)
        self.selected_files_label.setText("Path shown here")
        self.selected_files_label.move(50,0)

    def sort_files(self):
        self.button.setText('working')
        self.button.repaint()
       
        


app = QApplication(sys.argv)
win = MyWindow()        

win.show()
sys.exit((app.exec()))