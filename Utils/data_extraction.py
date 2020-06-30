from os import listdir


def get_filenames(folder):
    """
    Get .csv and .out files to read turbostats and power-meter data
    :param folder: folder where to search
    :return: path to read turbostats and power-meter data
    """
    files = listdir(folder)
    filename1 = ''
    filename2 = ''
    for file in files:
        if file[-3:] == 'out':
            filename1 = folder+file
        if file[-3:] == 'csv':
            filename2 = folder+file
    return filename1, filename2


def get_power_meter(folder,subdir='Power-meter/'):
    """
    Get .csv files to read data obtained by the power-meter soft by Gael Guennebaut
    https://gitlab.inria.fr/guenneba/mac-power-meter/-/tree/master
    :param folder: where to search
    :param subdir: subdir
    :return: path to a the file
    """
    files = listdir(folder + subdir )
    filename = ''
    for file in files:
        try:
            if file[-3:] == 'csv' and file[:15] == 'power_meter_log':
                filename = folder + subdir+ file
        except:
            filename = ''
    return filename