import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tkinter", "os"],
    "include_files": ["sinhala akuru.txt"],
}

# base="Win32GUI" should be used only for Windows GUI app
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="Singlish",
    version="1.0",
    description="English to Sinhala Transliterator",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "singlish_gui.py",
            base=base,
            icon="icon.ico",  # You'll need to create an icon file
            target_name="Singlish.exe"
        )
    ]
)
