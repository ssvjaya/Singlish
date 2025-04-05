import PyQt6.QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QTextEdit,
    QPushButton, QCheckBox, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QFontDatabase
from singlish import transliterate

class TransliteratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load the Inter font dynamically
        font_id = QFontDatabase.addApplicationFont("Inter-Regular.ttf")
        if font_id == -1:
            print("Failed to load Inter font.")
        else:
            print("Inter font loaded successfully.")

        self.setWindowTitle("English to Sinhala Transliterator")
        self.setGeometry(100, 100, 800, 600)

        # Remove the default title bar
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Main widget1 containing the title bar and main widget
        self.main_widget1 = QWidget()
        self.setCentralWidget(self.main_widget1)
        self.main_layout1 = QVBoxLayout(self.main_widget1)
        self.main_layout1.setContentsMargins(0, 0, 0, 0)  # No margins for main_widget1

        # Custom title bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(35)
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(20, 0, 0, 0)  # No margins for the title bar

        self.title_label = QLabel("English to Sinhala Transliterator")
        font = QFont("Inter", 12)
        font.setWeight(QFont.Weight.Bold)  # Set the font to bold
        self.title_label.setFont(font)
        self.title_bar_layout.addWidget(self.title_label)

        # Button container for minimize, maximize, and close buttons
        self.button_container = QHBoxLayout()
        self.button_container.setSpacing(0)  # Remove spacing between buttons

        # Minimize button
        self.minimize_button = QPushButton("—")  # Unicode for minimize symbol
        self.minimize_button.setFixedSize(40, 35)
        self.minimize_button.setObjectName("title_bar_button")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.button_container.addWidget(self.minimize_button)

        # Maximize/Restore button
        self.maximize_button = QPushButton("🗖")  # Unicode for maximize symbol
        self.maximize_button.setFixedSize(40, 35)
        self.maximize_button.setObjectName("title_bar_button")
        self.maximize_button.clicked.connect(self.toggle_maximize_restore)
        self.button_container.addWidget(self.maximize_button)

        # Close button
        self.close_button = QPushButton("✕")
        self.close_button.setFixedSize(40, 35)
        self.close_button.setObjectName("title_bar_button")
        self.close_button.clicked.connect(self.close)
        self.button_container.addWidget(self.close_button)

        # Add button container to the title bar layout
        self.title_bar_layout.addLayout(self.button_container)

        # Add the title bar to main_widget1
        self.main_layout1.addWidget(self.title_bar)

        # Main widget containing other elements
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(20, 0, 20, 20)  # Margins for the body (no top margin)

        # Add main_widget to main_widget1
        self.main_layout1.addWidget(self.main_widget)

        # Enable dragging the custom title bar
        self.title_bar.mousePressEvent = self.start_drag
        self.title_bar.mouseMoveEvent = self.perform_drag

        # Add consistent styling for the title bar and buttons
        self.setStyleSheet("""
            QWidget#title_bar {
                background-color: #444444;
            }
            QPushButton#title_bar_button {
                border: none;
                background-color: #444444;
                color: white;
            }
            QPushButton#title_bar_button:hover {
                background-color: #555555;
            }
        """)
        self.title_bar.setObjectName("title_bar")

        # Dark mode toggle
        self.dark_mode = False
        self.dark_mode_checkbox = QCheckBox("Dark Mode")
        self.dark_mode_checkbox.setFont(QFont("Inter", 11))  # Changed font to Inter
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)
        self.main_layout.addWidget(self.dark_mode_checkbox, alignment=Qt.AlignmentFlag.AlignLeft)

        # English text input
        self.english_label = QLabel("Type English Text:")
        self.english_label.setFont(QFont("Inter", 12))  # Changed font to Inter
        self.main_layout.addWidget(self.english_label)

        self.english_text = QTextEdit()
        self.english_text.setFont(QFont("Inter", 12))  # Changed font to Inter
        self.english_text.textChanged.connect(self.update_text)
        self.main_layout.addWidget(self.english_text)

        # Sinhala text output
        self.sinhala_label = QLabel("සිංහල අකුරු:")
        self.sinhala_label.setFont(QFont("Inter", 12))  # Changed font to Inter
        self.main_layout.addWidget(self.sinhala_label)

        self.sinhala_text = QTextEdit()
        self.sinhala_text.setFont(QFont("Iskoola Pota", 14))
        self.sinhala_text.setReadOnly(True)
        self.main_layout.addWidget(self.sinhala_text)

        # Buttons with increased size and thickness
        self.button_layout = QHBoxLayout()
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFont(QFont("Inter", 12))  # Changed font to Inter
        self.clear_button.setMinimumSize(120, 40)  # Increase button size
        self.clear_button.clicked.connect(self.clear_text)
        self.button_layout.addWidget(self.clear_button)

        self.copy_button = QPushButton("Copy Sinhala")
        self.copy_button.setFont(QFont("Inter", 12))  # Changed font to Inter
        self.copy_button.setMinimumSize(120, 40)  # Increase button size
        self.copy_button.clicked.connect(self.copy_sinhala)
        self.button_layout.addWidget(self.copy_button)

        self.help_button = QPushButton("Help")
        self.help_button.setFont(QFont("Inter", 12))  # Changed font to Inter
        self.help_button.setMinimumSize(120, 40)  # Increase button size
        self.help_button.clicked.connect(self.show_help)
        self.button_layout.addWidget(self.help_button)

        # Add more spacing to the button layout
        self.button_layout.setSpacing(20)  # Increased spacing between buttons

        self.main_layout.addLayout(self.button_layout)

        # Add custom styling for button thickness
        self.setStyleSheet("""
            QPushButton {
                padding: 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton {
                border: none;
                background-color: #444444;
                color: white;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            QPushButton#close_button:hover {
                background-color: #444444;
            }
            QWidget#title_bar {
                background-color: #444444;
            }
            QPushButton#title_bar_button {
                border: none;
                background-color: #444444;
                color: white;
            }
            QPushButton#title_bar_button:hover {
                background-color: #555555;
            }
        """)
        self.close_button.setObjectName("close_button")

        # Initial light mode styling
        self.apply_light_mode()

    def start_drag(self, event):
        """Start dragging the window."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def perform_drag(self, event):
        """Perform the dragging of the window."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def toggle_dark_mode(self):
        """Toggle between light and dark mode."""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

    def apply_dark_mode(self):
        """Apply dark mode styling."""
        self.setStyleSheet("""
            QMainWindow { background-color: #2E2E2E; color: white; }
            QLabel { color: white; }
            QTextEdit { background-color: #1E1E1E; color: white; }
            QPushButton { background-color: #444444; color: white; border: none; }
            QPushButton:hover { background-color: #333; color: white; border: none; }
            QCheckBox { color: white; }
            QWidget#title_bar { background-color: #444444; }
            QPushButton#close_button { background-color: #444444; color: white; border: none; }
            QPushButton#close_button:hover { background-color: #333; border: none; }
        """)
        self.title_bar.setObjectName("title_bar")
        self.close_button.setObjectName("close_button")

        # Set dark mode styling for QMessageBox
        QMessageBox.setStyleSheet(QMessageBox(), """
            QMessageBox {
                background-color: #2E2E2E;
                color: white;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)

    def apply_light_mode(self):
        """Apply light mode styling."""
        self.setStyleSheet("""
            QMainWindow { background-color: #F0F0F0; color: black; }
            QLabel { color: black; }
            QTextEdit { background-color: white; color: black; }
            QPushButton { background-color: #E0E0E0; color: black; border: none; }
            QPushButton:hover { background-color: #D0D0D0; color: black; border: none; }
            QCheckBox { color: black; }
            QWidget#title_bar { background-color: #E0E0E0; }
            QPushButton#close_button { background-color: #E0E0E0; color: black; border: none; }
            QPushButton#close_button:hover { background-color: #D0D0D0; }
        """)
        self.title_bar.setObjectName("title_bar")
        self.close_button.setObjectName("close_button")

        # Reset QMessageBox styling to default for light mode
        QMessageBox.setStyleSheet(QMessageBox(), "")

    def update_text(self):
        """Update the Sinhala text based on the English input."""
        english = self.english_text.toPlainText().strip()
        sinhala = transliterate(english) if english else ""
        self.sinhala_text.setPlainText(sinhala)
        
        # Auto-scroll to the bottom
        scrollbar = self.sinhala_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def clear_text(self):
        """Clear both text areas."""
        self.english_text.clear()
        self.sinhala_text.clear()

    def copy_sinhala(self):
        """Copy Sinhala text to clipboard."""
        sinhala_text = self.sinhala_text.toPlainText().strip()
        if (sinhala_text):
            QApplication.clipboard().setText(sinhala_text)
            self.show_message("Success", "Sinhala text copied to clipboard!")

    def show_help(self):
        """Show help information."""
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
        """Show a QMessageBox with dark mode support."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2E2E2E;
                color: white;
            }
            QPushButton {
                background-color: #444444;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        msg_box.exec()

    def toggle_maximize_restore(self):
        """Toggle between maximized and restored window states."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

def main():
    app = QApplication([])
    window = TransliteratorGUI()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
