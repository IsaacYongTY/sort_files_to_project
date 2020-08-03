# Get song title by removing affix

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