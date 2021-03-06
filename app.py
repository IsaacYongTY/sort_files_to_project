# -*- coding: utf-8 -*-

import os, shutil, re, sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from hanziconv import HanziConv

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()

        self.relative_path = '.'
        self.directory = self.get_correct_path(self.relative_path)

        uic.loadUi(f'{self.directory}/sort_files_to_project.ui', self)

        self.affixes = ['IG', 'Spotify', '4KHD', 'no', 'sub', '1080p', '抖音', 'MASTER']

        self.files = []
        self.project_directories = []

        self.selectButton.clicked.connect(self.select_files)
        self.sortButton.clicked.connect(lambda: self.sort_files(self.files))
        self.browseButton.clicked.connect(self.browse_path)



        with open(f'{self.directory}/default_directory.txt', 'r') as f:
            root_directory = f.read()
            self.rootDirectoryInput.setText(root_directory)


        self.add_subfolders_to_search(self.rootDirectoryInput.text())

        self.show()

    def browse_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()
        print(path)
        self.rootDirectoryInput.setText(path)

    def get_correct_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')

        return os.path.join(base_path, relative_path)

    def add_subfolders_to_search(self, directory):

            paths = ['',
                     '00_ARCHIVE',
                     '00_ARCHIVE/2018 and older',
                     '00_ARCHIVE/2019',
                     '00_ARCHIVE/2020',
                     '000_INCUBATOR'
                     ]

            for path in paths:
                self.project_directories.append(f'{directory}/{path}')

    def remove_affixes(self, filename, affixes):

        filename_array = filename.split()

        for affix in affixes:
            if filename_array.count(affix):
                filename_array.remove(affix)

        delimiter = ' '
        result = delimiter.join(filename_array)

        return result

    def get_title_and_extension(self, path):

        filename = os.path.split(path)[1]
        filename = os.path.splitext(filename)[0]
        filename = self.remove_affixes(filename, self.affixes)

        # Check for Chinese character
        song_title = re.findall(r'[\u4e00-\u9fff]+', filename)
        delimiter = ''
        song_title = delimiter.join(song_title)

        if song_title:
            print('Contains chinese characters')
            extension = os.path.splitext(path)[1]
            song_title = HanziConv.toSimplified(song_title)

            return song_title, extension

        else:
            return False

    def select_files(self):
        self.files = QtWidgets.QFileDialog.getOpenFileNames()[0]
        print(self.files)

        self.preview = ''

        for file in self.files:
            
            self.preview += file + '\n'
            self.selectedFilesLabel.setText(self.preview)
            self.selectedFilesLabel.repaint()
            print(file)
        
        return self.files

    def find_destination_main(self, song_title, project_directories):

        print(song_title)
        for directory in project_directories:
            for folder in os.listdir(directory):
                if folder.find(song_title) >= 0:

                    result = f'{directory}/{folder}'

                    return result
        return False


    def find_subfolder(self, destination_base, extension):
        if extension == '.mp4' or extension == '.mov':
            destination = f'{destination_base}/01_VIDEOS'
            print('Video')
            return destination
        elif extension == '.mp3' or extension == '.wav' or extension == '.flac':
            destination = f'{destination_base}/02_AUDIOS'
            print('Music')
            return destination
        elif extension == '.psd' or extension == '.jpg' or extension == '.png':
            destination = f'{destination_base}/03_GRAPHICS'
            print('Pictures')
            return destination
        elif extension == '.txt' or extension == '.lrc' or extension == '.pdf' or extension == '.csv':
            destination = f'{destination_base}/04_DOCS'
            print('Documents')
            return destination
        else:
            exit()

    def move_file(self, source, destination, extension):
        filename = os.path.split(source)[1]
        filename = os.path.splitext(filename)[0]

        if os.path.isfile(f'{destination}/{filename}{extension}'):
            os.rename(source, f'{destination}/{filename} copy{extension}')

            return

        shutil.move(source, destination)


    def sort_files(self, files):
        if not self.files:
            self.operationStatusLabel.setText('No files selected')
            self.operationStatusLabel.repaint()
        else:

            status_text = ''
            for file in files:

                data = self.get_title_and_extension(file)

                if data:
                    simplified_song_title = data[0]
                    extension = data[1]

                    destination_base = self.find_destination_main(simplified_song_title,self.project_directories)
                    file_name = os.path.split(file)[1]

                    print(destination_base)

                    status_text = ''

                    if destination_base:

                        destination_subfolder = self.find_subfolder(destination_base, extension)

                        if not os.path.isdir(destination_subfolder):

                            create_folder_message = QMessageBox.question(self, "Create subfolder", f"Target subfolder doesn't exist.\nDo you want to create {destination_subfolder} and move the file?", QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)

                            if create_folder_message == QMessageBox.Yes:
                                os.mkdir(destination_subfolder)

                            else:
                                status_text += f"Target subfolder doesn't exist for {file_name}. File is not moved.\n"

                            print(f'Path exist: {destination_subfolder}')

                        if os.path.isdir(destination_subfolder):
                            self.move_file(file, destination_subfolder, extension)
                            status_text += f'{file_name} moved to {destination_subfolder}\n'

                    else:
                        status_text += f"Destination doesn't exist for {file_name}. File is not moved.\n"


                    self.operationStatusLabel.setText(status_text)
                    self.operationStatusLabel.repaint()

                    self.selectedFilesLabel.setText("Show the Files Here")
                    self.selectedFilesLabel.repaint()

                    self.files = []

                else:
                    self.operationStatusLabel.setText("Doesn't contain Chinese characters")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()

    sys.exit(app.exec_())







