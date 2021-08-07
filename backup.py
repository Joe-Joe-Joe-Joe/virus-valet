import os
from time import time


def get_folder_list():
    drive, path = os.path.splitdrive(__file__)
    pathlist = []
    while True:
        values = os.path.split(path)
        if not values[1]:
            pathlist.append(drive + '\\')
            pathlist.reverse()
            return pathlist
        path = values[0]
        pathlist.append(values[1])


def join_folder_list(folder_list):
    output = ""
    for i in folder_list:
        output = os.path.join(output, i)
    return output

folder_list = get_folder_list()
current_folder = join_folder_list(folder_list[:-1])
backups_folder = join_folder_list(folder_list[:-2] + ["Backups", str(time())])
os.system(f'xcopy "{current_folder}" "{backups_folder}" /E /H /C /I')
