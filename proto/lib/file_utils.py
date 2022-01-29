import os
import shutil


def folder_exists(folder_path: str) -> bool:
    """
    Check if folder exists.

    :param folder_path the path of the folder to look for.
    """
    return os.path.isdir(folder_path)


def create_clean_folder(folder_path: str):
    """
    Create a clean folder removing the old one if it exists.

    :param folder_path the path of the folder to look up.
    """
    if folder_exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)


def delete_folder(*folder_path: str):
    """
    Delete a list of folders if folder exists.

    :param folder_path: the list of paths of the folder to look up.
    """
    for folder in folder_path:
        if folder_exists(folder):
            shutil.rmtree(folder)


def delete_file(*file_path: str):
    """
    Delete a list of files if files exists.

    :param file_path: the list of paths o the file to look up
    """
    for path in file_path:
        if os.path.exists(path):
            os.remove(path)
