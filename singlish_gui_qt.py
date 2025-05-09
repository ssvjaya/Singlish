import os
import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit,
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont
from singlish import transliterate
from history_window import HistoryWindow  # Import the HistoryWindow class
from PyQt6.QtGui import QIcon

def resource_path(relative_path):
    """Get the absolute path to a resource, works for both development and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temporary folder _MEIPASS where bundled files are extracted
        path = os.path.join(sys._MEIPASS, relative_path)
    else:
        path = os.path.join(os.path.dirname(__file__), relative_path)
    
    # Normalize the path for compatibility
    path = os.path.normpath(path)
    
    # Verify if the file exists
    if not os.path.exists(path):
        print(f"Resource not found: {path}")
    return path

class TransliteratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Singlish Transliterator")
        self.setGeometry(100, 100, 800, 600)

        # Remove the default title bar and enable transparency
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Main widget containing the title bar and main layout
        self.main_widget1 = QWidget()
        self.setCentralWidget(self.main_widget1)
        self.main_layout1 = QVBoxLayout(self.main_widget1)
        self.main_layout1.setContentsMargins(0, 0, 0, 0)
        self.main_widget1.setObjectName("main_widget_container")

        # Custom title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(20, 2, 2, 2)

        self.title_label = QLabel("Singlish Transliterator", self.title_bar)
        self.title_label.setObjectName("title_bar_label")
        font = QFont("Arial", 12)  # Use Arial font
        font.setWeight(QFont.Weight.Bold)
        self.title_label.setFont(font)
        self.title_bar_layout.addWidget(self.title_label)

        # Button container for minimize, maximize, and close buttons
        self.button_container = QHBoxLayout()
        self.button_container.setSpacing(0)

        self.minimize_button = QPushButton("—")
        self.minimize_button.setFixedSize(40, 35)
        self.minimize_button.setObjectName("title_bar_button")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.button_container.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("🗖")
        self.maximize_button.setFixedSize(40, 35)
        self.maximize_button.setObjectName("title_bar_button")
        self.maximize_button.clicked.connect(self.handle_maximize_button)
        self.button_container.addWidget(self.maximize_button)

        self.close_button = QPushButton("⨉")
        self.close_button.setFixedSize(40, 35)
        self.close_button.setObjectName("title_bar_button_close")
        self.close_button.clicked.connect(self.close)
        self.button_container.addWidget(self.close_button)

        self.title_bar_layout.addLayout(self.button_container)
        self.main_layout1.addWidget(self.title_bar)

        # Main widget containing other elements
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 0, 20, 20)
        self.main_layout1.addWidget(self.main_widget)

        # Enable dragging and double-click functionality for the custom title bar
        self.title_bar.mousePressEvent = self.start_drag
        self.title_bar.mouseMoveEvent = self.perform_drag
        self.title_bar.mouseDoubleClickEvent = self.handle_title_bar_double_click  # Separate double-click event

        # Dark mode toggle using QPushButton with icons and text
        self.dark_mode = False
        self.dark_mode_button = QPushButton(" Dark Mode")  # Add text to the button
        self.dark_mode_button.setFont(QFont("Arial", 11))  # Use Arial font
        self.dark_mode_button.setCheckable(True)
        self.dark_mode_button.setFixedSize(120, 40)  # Adjust size to fit text and icon
        self.dark_mode_button.setObjectName("dark_mode_button_checkbox")  # Set the correct ObjectName

        # Load icons for dark mode toggle
        self.dark_mode_on_icon = QIcon(resource_path("resources/check-focus.png"))
        self.dark_mode_off_icon = QIcon(resource_path("resources/check-unsel-dis.png"))
        self.dark_mode_button.setIcon(self.dark_mode_off_icon)
        self.dark_mode_button.setIconSize(self.dark_mode_button.size() - QSize(80, 20))  # Adjust icon size

        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)
        self.main_layout.addWidget(self.dark_mode_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # English text input
        self.english_label = QLabel("Type English Text:")
        self.english_label.setFont(QFont("Arial", 12))  # Use Arial font
        self.main_layout.addWidget(self.english_label)

        self.english_text = QTextEdit()
        self.english_text.setFont(QFont("Arial", 12))  # Use Arial font
        self.english_text.textChanged.connect(self.update_text)
        self.main_layout.addWidget(self.english_text)

        # Sinhala text output
        self.sinhala_label = QLabel("සිංහල අකුරු:")
        self.sinhala_label.setFont(QFont("Arial", 12))  # Use Arial font
        self.main_layout.addWidget(self.sinhala_label)

        self.sinhala_text = QTextEdit()
        self.sinhala_text.setFont(QFont("Iskoola Pota", 14))
        self.sinhala_text.setReadOnly(True)
        self.main_layout.addWidget(self.sinhala_text)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(QFont("Arial", 12))  # Use Arial font
        self.clear_button.setMinimumSize(120, 40)
        self.clear_button.clicked.connect(self.clear_text)
        self.button_layout.addWidget(self.clear_button)

        self.copy_button = QPushButton("Copy Sinhala")
        self.copy_button.setFont(QFont("Arial", 12))  # Use Arial font
        self.copy_button.setMinimumSize(120, 40)
        self.copy_button.clicked.connect(self.copy_sinhala)
        self.button_layout.addWidget(self.copy_button)

        self.help_button = QPushButton("Help")
        self.help_button.setFont(QFont("Arial", 12))  # Use Arial font
        self.help_button.setMinimumSize(120, 40)
        self.help_button.clicked.connect(self.show_help)
        self.button_layout.addWidget(self.help_button)

        self.history_button = QPushButton("History")
        self.history_button.setFont(QFont("Arial", 12))  # Use Arial font
        self.history_button.setMinimumSize(120, 40)
        self.history_button.clicked.connect(self.show_history)
        self.button_layout.addWidget(self.history_button)

        self.button_layout.setSpacing(20)
        self.button_layout.setContentsMargins(0, 10, 0, 0)
        self.main_layout.addLayout(self.button_layout)

        # Initialize history list
        self.history = []

        # Initial light mode styling
        self.apply_light_mode()

    def start_drag(self, event):
        """Start dragging the window when the left mouse button is pressed."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def perform_drag(self, event):
        """Perform dragging of the window."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.dark_mode_button.setIcon(self.dark_mode_on_icon)
            self.dark_mode_button.setText(" Dark Mode")  # Update text for light mode
            self.apply_dark_mode()
        else:
            self.dark_mode_button.setIcon(self.dark_mode_off_icon)
            self.dark_mode_button.setText(" Dark Mode")  # Update text for dark mode
            self.apply_light_mode()

    def apply_dark_mode(self):
        self.setStyleSheet(f"""
            QMainWindow {{ 
                background-color: transparent; /* Fully transparent */
            }}
            QWidget#main_widget_container {{ 
                background-color: #202020;
                border-radius: 5px; /* Rounded corners */
                border: 1px solid #444444;
            }}
            QWidget#title_bar {{ 
                background-color: #202020;
                border-top-left-radius: 5px; /* Rounded corners for the top */
                border-top-right-radius: 5px;
            }}
            QLabel {{ color: white; }}
            QTextEdit {{ 
                background-color: #1E1E1E; /* Dark background for QTextEdit */
                color: white; /* White text color */
                border: 1px solid #444444; /* Optional border for QTextEdit */
            }}
            QPushButton {{ background-color: #444444; color: white; border: none; }}
            QPushButton:hover {{ background-color: #0078D4; }}

            QPushButton#dark_mode_button_checkbox {{ 
                background-color: #202020;
                color: white;
                border: none;
                text-align: left; /* Align text to the left */
            }}
            QPushButton#dark_mode_button_checkbox:hover {{ background-color: #202020; }}
            
            /* Specific styles for title bar buttons */
            QPushButton#title_bar_button_close {{
                background-color: #202020;
                color: white;
                border: none;
                font-size: 14px;
                border-top-right-radius: 5px;
            }}

            QPushButton#title_bar_button {{
                background-color: #202020;
                color: white;
                border: none;
                font-size: 14px;
            }}
            /* Specific hover for close button */
            QPushButton#title_bar_button_close:hover {{
                background-color: #F70000;
            }}
            QPushButton#title_bar_button:hover {{
                background-color: #444444;
            }}
            QWidget#title_bar {{ background-color: #444444; }}
        """)

    def apply_light_mode(self):
        self.setStyleSheet(f"""
            QMainWindow {{ 
                background-color: transparent; /* Fully transparent */
            }}
            QWidget#main_widget_container {{ 
                background-color: #F3F3F3;
                border-radius: 5px; /* Rounded corners */
                border: 1px solid #CCCCCC;
            }}
            QWidget#title_bar {{ 
                background-color: #F3F3F3;
                border-top-left-radius: 5px; /* Rounded corners for the top */
                border-top-right-radius: 5px;
            }}
            QLabel {{ color: black; }}
            QTextEdit {{ 
                background-color: white; /* Dark background for QTextEdit */
                color: black; /* White text color */
                border: 1px solid #444444; /* Optional border for QTextEdit */
            }}
            QPushButton {{ background-color: #E0E0E0; color: black; border: none; }}
            QPushButton:hover {{ background-color: #C4C4C4; }}

            QPushButton#dark_mode_button_checkbox {{
                background-color: #F3F3F3; 
                color: black; 
                border: none; 
                text-align: left; /* Align text to the left */
            }}
            QPushButton#dark_mode_button_checkbox:hover {{ background-color: #F3F3F3; }}

            QPushButton#title_bar_button {{
                background-color: #F3F3F3;
                color: black;
                border: none;
                font-size: 14px;
            }}
            QPushButton#title_bar_button_close {{
                background-color: #F3F3F3;
                color: black;
                border: none;
                font-size: 14px;
                border-top-right-radius: 5px;
            }}
            QPushButton#title_bar_button_close:hover {{
                background-color: #F70000;
            }}
            /* Specific hover for close button */
            QPushButton#title_bar_button:hover {{
                background-color: #E0E0E0;
            }}
            QWidget#title_bar {{ background-color: #F3F3F3; }}
        """)

    def update_text(self):
        english = self.english_text.toPlainText().strip()
        sinhala = transliterate(english) if english else ""
        self.sinhala_text.setPlainText(sinhala)
        scrollbar = self.sinhala_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_text(self):
        self.english_text.clear()
        self.sinhala_text.clear()

    def copy_sinhala(self):
        sinhala_text = self.sinhala_text.toPlainText().strip()
        if sinhala_text:
            QApplication.clipboard().setText(sinhala_text)
            # Add directly to the database
            history_window = HistoryWindow([], self.dark_mode)
            history_window.add_history_item(sinhala_text)
            history_window.close()  # Ensure the database connection is closed
            self.show_popup_message("Sinhala text copied to clipboard!")

    def show_popup_message(self, message):
        popup = QLabel(message, self)
        popup.setFont(QFont("Arial", 12))  # Use Arial font
        popup.setStyleSheet("""
            QLabel {
                background-color: #444444; color: white; 
                border-radius: 5px; padding: 10px; border-radius: 5px;
                
            }
        """ if self.dark_mode else """
            QLabel {
                background-color: #E0E0E0; color: black; 
                border-radius: 5px; padding: 10px; border-radius: 5px;
                
            }
        """)
        popup.setAlignment(Qt.AlignmentFlag.AlignCenter)
        popup.setFixedSize(300, 50)
        popup.move(self.width() // 2 - popup.width() // 2, self.height() // 2 - popup.height() // 2)
        popup.show()

        # Automatically hide the popup after 2 seconds
        QTimer.singleShot(2000, popup.deleteLater)

    def show_help(self):
        help_text = """How to use the Sinhala Transliterator:

1. Basic vowels:
   - a -> අ, aa -> ආ, A -> ඇ, Ae -> ඈ
   - i -> ඉ, ii -> ඊ
   - u -> උ, uu -> ඌ
   - e -> එ, ee -> ඒ
   - o -> ඔ, oo -> ඕ

2. Consonants:
   - k -> ක්, g -> ග්, ch -> ච්
   - t -> ට්, d -> ඩ්
   - n -> න්, p -> ප්, b -> බ්
   - m -> ම්, y -> ය්, r -> ර්
   - l -> ල්, w/v -> ව්, s -> ස්

3. Special combinations:
   - Type 'ga' for ග, 'gi' for ගි
   - Type 'ma' for ම, 'mi' for මි
   - Type 'nda' for ඳ, 'mba' for ඹ

Note: Use capital letters for special characters like 'A' for ඇ."""
        self.show_message("Help", help_text)

    def show_message(self, title, text):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        if self.dark_mode:
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #202020; color: white;
                }
                QPushButton {
                    background-color: #444444; color: white; border: 2px solid #555555;
                    border-radius: 5px; padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
            """)
        else:
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #FDFDFD; color: black;
                }
                QPushButton {
                    background-color: #E0E0E0; color: black; border: 2px solid #D0D0D0;
                    border-radius: 5px; padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #D0D0D0;
                }
            """)
        msg_box.exec()

    def handle_maximize_button(self):
        """Toggle between maximized and normal window states when the maximize button is clicked."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def handle_title_bar_double_click(self, event):
        """Toggle between maximized and normal window states when the title bar is double-clicked."""
        from PyQt6.QtCore import QEvent  # Import QEvent for event type checking
        if event.type() == QEvent.Type.MouseButtonDblClick:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

    def show_history(self):
        history_window = HistoryWindow(self.history, self.dark_mode)
        history_window.show()  # Use show() instead of exec()

def main():
    app = QApplication([])
    window = TransliteratorGUI()
    window.show()
    app.exec()


if __name__ == "__main__": 
    main()
