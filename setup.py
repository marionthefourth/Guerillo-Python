from distutils.core import setup
from guerillo.config import SCRIPTS, PACKAGES
from setuptools import setup, find_packages

include_files = []
from cx_Freeze import setup, Executable

setup(
    name="Guerillo",
    version="0.8.2",
    options={"build_exe": {
        'packages': find_packages(),
        'include_msvcr': True,
    }},
    executables=[Executable("__main__.py", base="Win32GUI")]
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
