import os
from sys import platform
from jedi.evaluate.utils import ignored
from guerillo.config import FileExtensions, Folders, FileHeaders, Storage, General, OperatingSystems, KeyFiles


class FileStorage:

    @staticmethod
    def read(file_name):
        """ Get's Directory of File Based on Name/Extension """
    # TODO - Fix this code to be dynamic
        """ file_path = FileStorage.direct_to_folder(
            FileStorage.get_root_path(),
            [FileStorage.get_file_folder(FileStorage.get_file_extension(file_name))]
        ) + file_name """

        file_path = None
        if FileStorage.is_special_file(file_name):
            file_path = FileStorage.direct_to_folder(
                FileStorage.get_root_path(),
                [FileStorage.root_to_special_file(file_name)]
            ) + file_name

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                return file.readlines()
        elif os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                return file.readlines()
        else:
            return ["", ""]  # Returns Safe Data if File Doesn't Exist

    @staticmethod
    def is_special_file(file_name):
        for file in KeyFiles.get():
            if file_name == file:
                return True

    @staticmethod
    def root_to_special_file(file_name):
        if file_name == KeyFiles.NATIONAL_COUNTY:
            return Folders.ANSI_DATA

    @staticmethod
    def get_root_path():
        return os.path.abspath(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), ".."), ".."), ".."))

    @staticmethod
    def get_file_exists(full_file_name_with_path):
        return os.path.isfile(full_file_name_with_path)

    @staticmethod
    def get_full_file_path(file_extension):
        return FileStorage.direct_to_folder(
            file_path=FileStorage.get_root_path(),
            folder=FileStorage.get_file_folder(file_extension)
        )

    @staticmethod
    def get_file_name_with_path(file_extension, index=0, secondary_file_extension=None):
        file_name_with_path = FileStorage.get_full_file_path(file_extension)
        file_name_with_path += FileStorage.get_file_base_name(file_extension, secondary_file_extension)
        return file_name_with_path + index + file_extension if index != 0 else file_extension

    @staticmethod
    def get_file_extension(full_file_name):
        for extension in [FileExtensions.TXT, FileExtensions.CSV]:
            if extension in full_file_name:
                return extension

        return None

    @staticmethod
    def get_file_index(file_name):
        file_name = file_name.replace(FileStorage.get_file_base_name(FileStorage.get_file_extension(file_name), ""), "")
        return file_name.replace(FileStorage.get_file_extension(file_name), "")

    @staticmethod
    def get_file_base_name(file_extension, secondary_extension):
        return {
            FileExtensions.TXT: FileHeaders.LINKS_RESULT
        }.get(file_extension, FileHeaders.MCAT if secondary_extension is FileExtensions.MP3 else FileHeaders.LCAT)


    @staticmethod
    def direct_to_folder(file_path, folder):
        for folder in folder:
            if General.BACKWARDS_SLASH in folder:
                if platform in [OperatingSystems.LINUX, OperatingSystems.LINUX2]:
                    pass
                elif platform is OperatingSystems.OSX:
                    pass
                else:  # platform is OperatingSystems.WINDOWS
                    folder = folder.replace(General.BACKWARDS_SLASH, General.DBL_FORWARDS_SLASH)

            file_path += folder

        with ignored(OSError):
            os.makedirs(file_path)

        return file_path

    @staticmethod
    def get_file_folder(file_extension):
        return {
            FileExtensions.TXT: Folders.ANSI_DATA,
        }.get(file_extension, None)
