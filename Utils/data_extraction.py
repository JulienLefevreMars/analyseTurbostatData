from os import listdir

def get_filenames(folder):
    files = listdir(folder)
    filename1 = ''
    filename2 = ''
    for file in files:
        if file[-3:] == 'out':
            filename1 = folder+file
        if file[-3:] == 'csv':
            filename2 = folder+file
    return filename1, filename2