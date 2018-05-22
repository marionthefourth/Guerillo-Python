import os.path

from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

INCLUDED_FILES = []
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'))
INCLUDED_FILES.append(os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'))

setup(
    name="StartGuerillo",
    version="1.0.0",
    author="Panoramic, Co.",
    options={
        "build_exe": {
            #'packages': "versionfinder.py",
            'include_files': INCLUDED_FILES,
            'include_msvcr': True,
        },
        'bdist_esky': {
            'freezer_module': 'cx_freeze',
        }
    },
    executables=[Executable("Guerillo.py", base="Win32GUI", targetName="Guerillo.exe",icon="phone.ico")]
)
