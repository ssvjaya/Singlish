#!/bin/bash

# Navigate to the directory containing the Python script
cd /c:/Users/Samila/Videos/Python/Singlish

# Create the executable with an icon
pyinstaller --onefile --icon=icon.ico singlish_gui_qt.py

# Notify the user
echo "Executable created in the dist directory."
