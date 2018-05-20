
import os, subprocess, shutil, sys

""" JERRYRIGGED IMPORT TIME"""
class Version:
    def __init__(self, split_version_name):
        self.major = int(split_version_name[0])
        self.minor = int(split_version_name[1])
        self.build = int(split_version_name[2])

    def __repr__(self):
        return str(self.major) + "." + str(self.minor) + "." + str(self.build)

    def __lt__(self, other):  # lt stands for lesser than
        if self.major < other.major:
            return True
        if self.minor < other.minor:
            return True
        if self.build < other.build:
            return True
        return False

    def __gt__(self, other):  # gt stands for greater than
        if self.major > other.major:
            return True
        if self.minor > other.minor:
            return True
        if self.build > other.build:
            return True
        return False

    def __eq__(self, other):  # eq -- equal to
        return self.major == other.major and self.minor == other.minor and self.build == other.build

    def __str__(self):
        return str(self.major) + "." + str(self.minor) + "." + str(self.build)

    def get_full_version_name(self):
        return "Guerillo-" + str(self) + ".win32"

class VersionFinder:
    @staticmethod
    def get_version_names(versions):
        list_to_return = []
        for version in versions:
            version_name = version.split("-")
            if len(version_name) > 1:
                version_name = version_name[1]
                list_to_return.append(version_name)
        for i, name in enumerate(list_to_return):
            list_to_return[i] = list_to_return[i].replace(".win32", "")
        return list_to_return

    @staticmethod
    def create_version_object_list(names_list):
        version_object_list = []
        for name in names_list:
            split_version_name = name.split(".")
            version_object_list.append(Version(split_version_name))
        return version_object_list

    @staticmethod
    def find_newest_version_object(version_objects_list):
        newest_version = version_objects_list[0]
        for version in version_objects_list:
            if version > newest_version:
                newest_version = version
        return newest_version

    @staticmethod
    def get_versions_dir():
        path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "appdata")
        versions = os.listdir(path)
        return versions

    @staticmethod
    def get_newest_version():
        version_names_list = VersionFinder.get_version_names(VersionFinder.get_versions_dir())
        my_version_object_list = VersionFinder.create_version_object_list(version_names_list)
        winner = VersionFinder.find_newest_version_object(my_version_object_list)
        newest_version = winner.get_full_version_name()
        return newest_version

    @staticmethod
    def clear_old_versions(newest_version):
        path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "appdata")
        version_names_list = VersionFinder.get_version_names(VersionFinder.get_versions_dir())
        my_version_object_list = VersionFinder.create_version_object_list(version_names_list)
        for version in my_version_object_list:
            if version.get_full_version_name() != newest_version:
                shutil.rmtree(os.path.join(path, version.get_full_version_name()), ignore_errors=False)
"""End of Gh-JERRYrigged import"""

#find newest version, assign it, then clear any old versions
newestversion = VersionFinder.get_newest_version()
VersionFinder.clear_old_versions(newestversion)
#open the main file in the proper version folder
path = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),"appdata")
folder_to_run_from = os.path.join(path,newestversion)
file_to_run = folder_to_run_from+"\\__main__.exe"
subprocess.call(file_to_run)



#if AutoUpdater had to run, re-do the above
