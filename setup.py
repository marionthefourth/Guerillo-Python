import os.path

import esky.bdist_esky
from esky.bdist_esky import Executable as Executable_Esky
from cx_Freeze import setup, Executable
from guerillo.config import SCRIPTS, RESOURCES, BIN

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

INCLUDED_FILES = [("res\\img", "lib\\res\\img")]
INCLUDED_FILES.append(("bin", "lib\\bin"))
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'))
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'))

ESKY_INCLUDED_FILES = [
    ("lib\\res\\img\\", RESOURCES.ALL),
    ("lib\\bin\\exports\\",[BIN.Folders.EXPORTS+"default.csv"]),
    ("lib\\bin\\reports\\",[BIN.Folders.REPORTS+"default.csv"]),
    ("lib\\bin\\web_drivers\\",[BIN.Folders.WEB_DRIVERS+"chromedriver.exe"]),
    ("",
     [
      os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
      os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll')
      ]
     )
]

setup(
    name="Guerillo",
    version="0.9.188",
    author="Panoramic, Co.",
    options={
        "build_exe": {
            # 'packages': PACKAGES.ALL,
            'include_files': INCLUDED_FILES,
            'include_msvcr': True,
        },
        'bdist_esky': {
            'freezer_module': 'cx_freeze',
        }
    },
    data_files=ESKY_INCLUDED_FILES,
    scripts=[
        Executable_Esky(
            SCRIPTS.MAIN,
            gui_only=True,
            icon=RESOURCES.ICON,
        ),
    ],
    #executables=[Executable(SCRIPTS.MAIN, base="Win32GUI", targetName="Guerillo.exe")]
)
