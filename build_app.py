import PyInstaller.__main__
import os

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    'singlish_gui_qt.py',  # Your main script
    '--onedir',        # Create a directory-based executable (faster startup)
    '--windowed',       # Run without console window
    '--icon=icon.ico',  # Icon for the executable
    '--name=SinglishQt 1.93',  # Name of the output executable
    f'--add-data={os.path.join(current_dir, "icon.ico")};.',  # Include the icon file
    f'--add-data={os.path.join(current_dir, "check-focus.png")};resources',  # Include the checkbox checked style file
    f'--add-data={os.path.join(current_dir, "check-unsel-dis.png")};resources',  # Include the checkbox unchecked style file
    '--clean',          # Clean PyInstaller cache
    '--noconfirm'       # Replace output directory without asking
])
