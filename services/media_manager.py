import os
import shutil


def remove_media(media):
    try:
        os.remove(media)
    except FileNotFoundError:
        pass


def rename_directory(dir_old_name, dir_new_name):
    try:
        shutil.move(dir_old_name, dir_new_name)
    except FileNotFoundError:
        pass
