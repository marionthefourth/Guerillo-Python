import csv
import os
from sys import platform
from jedi.evaluate.utils import ignored
from guerillo.config import FileExtensions, Folders, FileHeaders, Storage, General, OperatingSystems, KeyFiles


class FileStorage:

    @staticmethod
    def read(file_name, county_filter=None):
        """ Gets Directory of File Based on Name/Extension """
        file_path = None
        if not county_filter:
            if FileStorage.is_special_file(file_name):
                file_path = FileStorage.direct_to_folder(
                    FileStorage.get_root_path(),
                    [FileStorage.root_to_special_file(file_name)]
                ) + file_name
        else:
            if county_filter == "Pinellas":
                file_path = file_name

        if os.path.isfile(file_path):
            if FileStorage.get_file_extension(file_path) == FileExtensions.CSV:
                with open(file_path,'r') as file:
                    reader = csv.reader(file)
                    return list(reader)
            else:
                with open(file_path, 'r') as file:
                    return file.readlines()
        elif os.path.isfile(file_name):
            with open(file_name, 'r') as file:
                return file.readlines()
        else:
            return ["", ""]  # Returns Safe Data if File Doesn't Exist

    @staticmethod
    def get_webdriver():
        return FileStorage.direct_to_folder(
                    FileStorage.get_root_path(),
                    [FileStorage.root_to_special_file(KeyFiles.WEBDRIVER)]
                ) + KeyFiles.WEBDRIVER

    @staticmethod
    def save_data_to_csv(file_name, data):
        csv_file = csv.writer(open(file_name, 'w', newline=''))
        for row in data:
            csv_file.writerow(row)

    @staticmethod
    def rename(file_name, new_file_name):
        os.rename(file_name, new_file_name)

    @staticmethod
    def handle_timeout(driver, file):
        import time
        start_time = time.time()
        while not os.path.isfile(file):
            if (time.time() - start_time) >= 8:
                print(General.DOWNLOADING_ERROR)
                driver.quit()
                quit()
            pass

    @staticmethod
    def is_special_file(file_name):
        for file in KeyFiles.get():
            if file_name == file:
                return True

    @staticmethod
    def root_to_special_file(file_name):
        if file_name == KeyFiles.NATIONAL_COUNTY:
            return Folders.ANSI_DATA
        elif file_name == KeyFiles.WEBDRIVER:
            return Folders.WEB_DRIVERS

    @staticmethod
    def get_root_path():
        return os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."), ".."))

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
    def get_full_path(file_path):
        return FileStorage.direct_to_folder(FileStorage.get_root_path(), file_path)

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
    def get_csv_file_header(file_extension):
        return {
            FileExtensions.TXT: (
                Storage.UID,
                Storage.INDEX,
                Storage.TERMS,
                Storage.NUM_RESULTS,
                Storage.DATE,
                Storage.TIME
            ),
        }.get(file_extension, ())

    @staticmethod
    def get_csv_file_row(file_extension, values):
        return {
            FileExtensions.TXT: (
                values[Storage.UID],
                values[Storage.INDEX],
                values[Storage.TERMS],
                values[Storage.NUM_RESULTS],
                values[Storage.DATE],
                values[Storage.TIME]
            ),
        }.get(file_extension, ())

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
