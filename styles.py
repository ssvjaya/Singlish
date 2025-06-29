# Light mode styles
LIGHT_MODE_STYLE = """
QMainWindow { 
    background-color: transparent; /* Fully transparent */
}
QWidget#main_widget_container { 
    background-color: #F3F3F3;
    border-radius: 5px; /* Rounded corners */
    border: 1px solid #CCCCCC;
}
QWidget#sub_widget_container {
    background-color: #F3F3F3;
    border-bottom-left-radius: 5px; /* Rounded corners */
    border-bottom-right-radius: 5px; /* Rounded corners */
    border: 1px solid #CCCCCC;
}

QWidget#history_widget_container {
    background-color: #F3F3F3;
    border-radius: 5px; /* Rounded corners */
    border: 1px solid #CCCCCC;
}
QWidget#title_bar { 
    background-color: #F3F3F3;
    border-top-left-radius: 5px; /* Rounded corners for the top */
    border-top-right-radius: 5px;
}
QLabel#title_bar_label {
    color: black;
    font-size: 14px;
    font-weight: bold;
}
QLabel { color: black; }
QTextEdit { 
    background-color: white; 
    color: black; 
    border: 1px solid #444444; 
    border-radius: 5px; 
}
QPushButton { background-color: #E0E0E0; color: black; border: none; }
QPushButton:hover { background-color: #C4C4C4; }
QPushButton#dark_mode_button_checkbox {
    background-color: #F3F3F3; 
    color: black; 
    border: none; 
    text-align: left; 
}
QPushButton#dark_mode_button_checkbox:hover { background-color: #F3F3F3; }
QPushButton#title_bar_button {
    background-color: #F3F3F3;
    color: black;
    border: none;
    font-size: 14px;
}
QPushButton#title_bar_button_close {
    background-color: #F3F3F3;
    color: black;
    border: none;
    font-size: 14px;
    border-top-right-radius: 5px;
}
QPushButton#title_bar_button_close:hover { background-color: #F70000; }
QPushButton#title_bar_button:hover { background-color: #E0E0E0; }
"""

# Dark mode styles
DARK_MODE_STYLE = """
QMainWindow { 
    background-color: transparent; /* Fully transparent */
}
QWidget#main_widget_container { 
    background-color: #202020;
    border-radius: 5px; /* Rounded corners */
    border: 1px solid #444444;
}
QWidget#sub_widget_container {
    background-color: #202020;
    border-bottom-left-radius: 5px; /* Rounded corners */
    border-bottom-right-radius: 5px; /* Rounded corners */
    border: 1px solid #444444;
}
QLabel#title_bar_label {
    color: white;
    font-size: 14px;
    font-weight: bold;
}
QWidget#history_widget_container {
    background-color: #202020;
    border-radius: 5px; /* Rounded corners */
    border: 1px solid #444444;
}
QWidget#title_bar { 
    background-color: #202020;
    border-top-left-radius: 5px; /* Rounded corners for the top */
    border-top-right-radius: 5px;
}
QLabel { color: white; }
QTextEdit { 
    background-color: #1E1E1E; 
    color: white; 
    border: 1px solid #444444; 
    border-radius: 5px; 
}
QPushButton { background-color: #444444; color: white; border: none; }
QPushButton:hover { background-color: #0078D4; }
QPushButton#dark_mode_button_checkbox {
    background-color: #202020;
    color: white;
    border: none;
    text-align: left; 
}
QPushButton#dark_mode_button_checkbox:hover { background-color: #202020; }
QPushButton#title_bar_button_close {
    background-color: #202020;
    color: white;
    border: none;
    font-size: 14px;
    border-top-right-radius: 5px;
}
QPushButton#title_bar_button {
    background-color: #202020;
    color: white;
    border: none;
    font-size: 14px;
}
QPushButton#title_bar_button_close:hover { background-color: #F70000; }
QPushButton#title_bar_button:hover { background-color: #444444; }
"""
