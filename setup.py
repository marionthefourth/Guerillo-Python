import os.path

import esky.bdist_esky
from esky.bdist_esky import Executable as Executable_Esky
from cx_Freeze import setup, Executable
from guerillo.config import SCRIPTS, RESOURCES, BIN

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# INCLUDED_FILES = RESOURCES.ALL
# INCLUDED_FILES += SCRIPTS.ALL

INCLUDED_FILES = [("res\\img", "lib\\res\\img")]
INCLUDED_FILES.append(("bin", "lib\\bin"))
#INCLUDED_FILES.append(("bin", "lib\\bin"))
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'))
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'))

#
# ESKY_INCLUDED_FILES = [
#     (RESOURCES.DOWNARROW, "lib\\"+RESOURCES.DOWNARROW),
#     (RESOURCES.LOGINBUTTON, "lib\\"+RESOURCES.LOGINBUTTON),
#     (RESOURCES.PANO, "lib\\"+RESOURCES.PANO),
#     (RESOURCES.ICON, "lib\\"+RESOURCES.ICON),
#     (RESOURCES.SEARCHBUTTON, "lib\\"+RESOURCES.SEARCHBUTTON),
#     (RESOURCES.SBGREYSCALE, "lib\\"+RESOURCES.SBGREYSCALE),
#     (RESOURCES.SIGNUPBUTTON, "lib\\"+RESOURCES.SIGNUPBUTTON),
#     (BIN.CHROMEDRIVER,"lib\\"+BIN.CHROMEDRIVER),
#     (BIN.Folders.REPORTS+"2018-05-15 21-03.csv","lib\\"+BIN.Folders.REPORTS+"2018-05-15 21-03.csv"),
#     (BIN.Folders.EXPORTS+"01012018-05012018 150000.00 150001.00 2018-05-15 210338-149380.csv",
#      "lib\\"+BIN.Folders.EXPORTS+"01012018-05012018 150000.00 150001.00 2018-05-15 210338-149380.csv")
# ]


ESKY_INCLUDED_FILES = [
    ("lib\\res\\img\\",RESOURCES.ALL)
]

setup(
    name="Guerillo",
    version="0.9.0",
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
    executables=[Executable(SCRIPTS.MAIN, base="Win32GUI", targetName="Guerillo.exe")]
)
# include_files = [("res\\img", "lib\\res\\img"),(INCLUDED_FILES)]

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
