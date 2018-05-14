from distutils.core import setup
from guerillo.config import SCRIPTS, PACKAGES, RESOURCES
from setuptools import setup, find_packages


include_files = []
from cx_Freeze import setup, Executable
import os.path

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')


INCLUDED_FILES = RESOURCES.ALL
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'))
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'))

print(INCLUDED_FILES)

setup(
    name="Guerillo",
    version="0.8.2",
    author = "Panoramic, Co.",
    options={
        "build_exe": {
            'packages': PACKAGES.ALL,
            'include_files': INCLUDED_FILES,
            'include_msvcr': True,
        },
    },
    executables=[Executable(SCRIPTS.MAIN, base="Win32GUI",targetName="Guerillo.exe")]
)
"""
setup(
    name='Guerillo',
    version='0.8.2',
    options={"bdist_esky": {
        "freezer_module": "py2app",
        "freezer_options": {"includes": find_packages()},
    }},
    scripts=SCRIPTS.ALL
)
"""
"""
    scripts=[
        Executable_Esky(
            SCRIPTS.ALL,
            gui_only=False,
            # icon = XPTO  # Use an icon if you want.
        ),
    ],
    requirements="",
    'bdist_esky': {
            'freezer_module': 'cx_freeze',
        }
    """
