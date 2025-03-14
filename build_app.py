import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'singlish_gui.py',  # Your main script
    '--onefile',        # Create a single executable
    '--windowed',       # Run without console window
    '--icon=icon.ico',  # Icon for the executable
    '--name=Singlish',  # Name of the output executable
    '--add-data=icon.ico;.',  # Include the icon file
    '--clean',          # Clean PyInstaller cache
    '--noconfirm'       # Replace output directory without asking
])
