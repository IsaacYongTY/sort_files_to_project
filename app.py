import os, shutil, re, zhon
from os import path

project_directories = []

with open('project_directories.txt', 'r') as f:
    project_directories = f.read()
    project_directories = project_directories.split('\n')

affixes = ['IG', 'Spotify', '4KHD', 'no', 'sub', '1080p', '抖音', 'MASTER']

def remove_affixes(input):

    filename_array = input.split()
 
    for affix in affixes:
        if(filename_array.count(affix)):
            filename_array.remove(affix)

    str1 = ' '
    result = str1.join(filename_array)

    return result


def clean_up_text(input):


    filename = os.path.split(input)[1]
    filename = os.path.splitext(filename)[0]
    filename = remove_affixes(filename)

    # Check for Chinese character
    song_title = re.findall(r'[\u4e00-\u9fff]+', filename)
    str1 = ''
    song_title = str1.join(song_title)

    if song_title:
        print('Contains chinese characters')
        extension = os.path.splitext(input)[1]

    return song_title, extension

def find_destination_main(song_title, project_directories):
    
    print(song_title)
    for directory in project_directories:
        for folder in os.listdir(directory):
            if(folder.find(song_title) >= 0):
                result = f'{directory}/{folder}'
                return result

    print("Folder doesn't exist")
    exit()



def find_subfolder(destination_base, extension):
    if(extension == '.mp4' or extension == '.mov'):
        destination = f'{destination_base}/01_VIDEOS'
        print('Video')
        return destination
    elif(extension == '.mp3' or extension == '.wav' or extension == '.flac'):
        destination = f'{destination_base}/02_AUDIOS'
        print('Music')
        return destination
    elif(extension == '.psd' or extension == '.jpg' or extension == '.png'):
        destination = f'{destination_base}/03_GRAPHICS'
        print('Pictures')
        return destination
    elif(extension == '.txt' or extension == '.lrc'):
        destination = f'{destination_base}/04_DOCS'
        print('Documents')
        return destination
    else:
        exit()

def move_file(source, destination, extension):
    filename = os.path.split(source)[1]
    filename = os.path.splitext(filename)[0]
   
    if(os.path.isfile(f'{destination}/{filename}{extension}')):
        os.rename(source, f'{destination}/{filename} copy{extension}')

        return 
    
    if(os.path.isdir(destination)):
        print(f'Path exist: {destination}')
        shutil.move(source, destination)
    else:
        print('Destination folder does not exist, file is not moved')


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.sort_button = QtWidgets.QPushButton(self.centralwidget)
        self.sort_button.setGeometry(QtCore.QRect(270, 330, 113, 32))
        self.sort_button.setObjectName("sort_button")

        self.operation_status_label = QtWidgets.QLabel(self.centralwidget)
        self.operation_status_label.setGeometry(QtCore.QRect(120, 260, 91, 16))
        self.operation_status_label.setObjectName("operation_status_label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 90, 800, 100))
        self.label_2.setAcceptDrops(True)
        self.label_2.setObjectName("label_2")

        self.select_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_button.setGeometry(QtCore.QRect(110, 330, 113, 32))
        self.select_button.setObjectName("select_button")

       # self.song_title = QT

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionCopy)
        self.menuFile.addAction(self.actionPaste)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.files = []

        self.select_button.clicked.connect(self.select_files)
        self.sort_button.clicked.connect(lambda: self.sort_files(self.files))

    def select_files(self):
        self.files = QtWidgets.QFileDialog.getOpenFileNames()[0]
        print(self.files)

        self.preview = ''

        for file in self.files:
            
            self.preview += file + '\n'
            self.label_2.setText(self.preview)
            self.label_2.adjustSize()
            self.label_2.repaint()
            print(file)
        
        return self.files

    def sort_files(self, files):
        if not self.files:
           self.operation_status_label.setText('No files selected')
           self.operation_status_label.adjustSize()
           self.operation_status_label.repaint()
        else:

            status_text = ''
            for file in files:

                data = clean_up_text(file)
                song_title = data[0]
                extension = data[1]
                destination_base = find_destination_main(song_title,project_directories)

                destination = find_subfolder(destination_base, extension)
                move_file(file, destination, extension)

                status_text += f'{os.path.split(file)[1]} moved to {destination}\n'
                self.operation_status_label.setText(status_text)
                self.operation_status_label.adjustSize()
                self.operation_status_label.repaint()

                self.label_2.setText("Show the Files Here")
                self.label_2.adjustSize()
                self.label_2.repaint()

                self.files = []
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sort_button.setText(_translate("MainWindow", "Sort"))
        self.operation_status_label.setText(_translate("MainWindow", "Placeholder"))
        self.label_2.setText(_translate("MainWindow", "Show The Files Here"))
        self.select_button.setText(_translate("MainWindow", "Select Files"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Create a new file"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "Copy a file"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste the file"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())







