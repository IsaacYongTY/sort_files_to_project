import os, shutil
from os import path

input_path = input('File path:')
print(input_path)
project_directories = ['/Users/isaacyong/Dropbox/00_PROJECTS','/Users/isaacyong/Dropbox/00_PROJECTS/00_Archive']

affixes = ['IG', 'Spotify', '4KHD', 'no sub', '1080p', '抖音']

def clean_up_text(input):
    
    filename = os.path.splitext(
        os.path.split(input)[1]
    )[0]

    extension = os.path.splitext(input)[1]
    filename_array = filename.split()
 
    for affix in affixes:
        if(filename_array.count(affix)):
            filename_array.remove(affix)

    str1 = ' '
    song_title = str1.join(filename_array)

    return song_title, extension

def find_destination_main(song_title, project_directories):
    for directory in project_directories:
       
        for folder in os.listdir(directory):
            print(folder)
            if(folder.find(song_title) >= 0):
                result = f'{directory}/{folder}'
                print(directory)

                print(folder)
                return result

    print("Folder doesn't exist")
    exit()



def find_subfolder(destination_base, extension):
    if(extension == '.mp4' or extension == '.mov'):
        destination = f'{destination_base}/01_VIDEOS'
        print('Video')
        return destination
    elif(extension == '.mp3' or extension == '.wav' or extension == '.flac'):
        destination = f'{destination_base}/02_MUSIC'
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

def move_file(source, destination, extension):
    filename = os.path.split(source)[1]
    filename = os.path.splitext(filename)[0]
   
    print(filename)
    if(os.path.isfile(f'{destination}/{filename}{extension}')):
        os.rename(source, f'{destination}/{filename} copy{extension}')

        return 
    
    shutil.move(source, destination)



def undo():
    shutil.move()

data = clean_up_text(input_path)
song_title = data[0]
extension = data[1]
destination_base = find_destination_main(song_title,project_directories)


destination = find_subfolder(destination_base, extension)
move_file(input_path, destination, extension)






