import sqlite3
from functools import partial
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from styles import LIGHT_MODE_STYLE, DARK_MODE_STYLE  # Import styles

class HistoryWindow(QWidget):  # History window using QWidget
    DB_FILE = "history.db"  # SQLite database file

    def __init__(self, history, dark_mode):
        super().__init__()
        self.setWindowTitle("History")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setGeometry(200, 100, 800, 600)  # Set window size
        self.setObjectName("main_widget_container")  # Match the style name

        
        # Main layout
        self.main_widget = QWidget(self)  # Set the parent to self
        self.main_layout = QVBoxLayout(self.main_widget)
        self.setLayout(self.main_layout)  # Directly set the layout for the main widget
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Assign dark_mode to an instance variable
        self.dark_mode = dark_mode

        # Initialize the database
        self.init_db()

        # Merge passed history with loaded history
        self.add_history_items(history)


        # Title bar
        self.title_bar = QWidget(self)
        self.title_bar.setObjectName("title_bar")  # Match the style name
        self.title_bar.setFixedHeight(35)
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(20, 2, 2, 2)  # Remove right-side padding

        self.title_label = QLabel("History", self.title_bar)
        self.title_label.setObjectName("title_bar_label")  # Match the style name
        self.title_label.setFont(QFont("Arial", 12))
        self.title_bar_layout.addWidget(self.title_label)

        self.close_button = QPushButton("✕", self.title_bar)
        self.close_button.setObjectName("title_bar_button_close")  # Match the style name
        self.close_button.setFixedSize(40, 35)
        self.close_button.clicked.connect(self.close)
        self.title_bar_layout.addWidget(self.close_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)  # Align to top-right corner

        self.main_layout.addWidget(self.title_bar)

        # History content
        self.history_widget = QWidget(self)
        self.history_layout = QVBoxLayout(self.history_widget)
        self.history_layout.setContentsMargins(30, 30, 30, 30)
        self.history_layout.setObjectName("history_widget_container")  # Match the style name

        self.populate_history()

        self.main_layout.addWidget(self.history_widget)

        # Clear all button
        self.clear_all_button = QPushButton("Clear All", self)
        self.clear_all_button.setFont(QFont("Arial", 12))
        self.clear_all_button.setFixedSize(120, 40)
        self.clear_all_button.clicked.connect(self.clear_all_history)
        self.main_layout.addWidget(self.clear_all_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Apply styling
        self.apply_styling(dark_mode)

        self._is_dragging = False  # Track dragging state
        self._drag_start_position = None  # Store initial mouse position

    def init_db(self):
        """Initialize the SQLite database and create the history table if it doesn't exist."""
        if not hasattr(self, 'conn') or not self.conn:
            self.conn = sqlite3.connect(self.DB_FILE)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT UNIQUE NOT NULL
                )
            """)
            self.conn.commit()

    def add_history_items(self, items):
        """Add multiple history items to the database."""
        for item in items:
            self.add_history_item(item)

    def add_history_item(self, text):
        """Add a single history item to the database."""
        try:
            self.cursor.execute("INSERT OR IGNORE INTO history (text) VALUES (?)", (text,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding history item: {e}")

    def get_all_history(self):
        """Retrieve all history items from the database."""
        self.cursor.execute("SELECT text FROM history")
        return [row[0] for row in self.cursor.fetchall()]

    def delete_history_item(self, text):
        """Delete a specific history item from the database."""
        try:
            self.cursor.execute("DELETE FROM history WHERE text = ?", (text,))
            self.conn.commit()
            self.populate_history()  # Refresh the UI
        except sqlite3.Error as e:
            print(f"Error deleting history item: {e}")

    def clear_all_history(self):
        """Clear all history items from the database."""
        try:
            self.cursor.execute("DELETE FROM history")
            self.conn.commit()
            self.populate_history()  # Refresh the UI
        except sqlite3.Error as e:
            print(f"Error clearing history: {e}")

    def populate_history(self):
        """Populate the history UI with items from the database."""
        # Clear existing layout
        for i in reversed(range(self.history_layout.count())):
            widget = self.history_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        history = self.get_all_history()
        if history:
            for item in history:
                item_layout = QHBoxLayout()  # Layout for each history item
                label = QLabel(item, self.history_widget)
                label.setFont(QFont("Arial", 12))
                label.setWordWrap(True)
                label.setStyleSheet(
                    "border: 1px solid #ccc; padding: 10px;" if not self.dark_mode else
                    "border: 1px solid #555; padding: 10px; color: white;"
                )
                item_layout.addWidget(label)

                copy_button = QPushButton("Copy", self.history_widget)
                copy_button.setFont(QFont("Arial", 10))
                copy_button.setFixedSize(80, 30)
                copy_button.clicked.connect(partial(self.copy_to_clipboard, item))
                item_layout.addWidget(copy_button)

                delete_button = QPushButton("Delete", self.history_widget)
                delete_button.setFont(QFont("Arial", 10))
                delete_button.setFixedSize(80, 30)
                delete_button.clicked.connect(partial(self.delete_history_item, item))
                item_layout.addWidget(delete_button)

                self.history_layout.addLayout(item_layout)
        else:
            # Display a message when no history is available
            no_history_label = QLabel("No history available.", self.history_widget)
            no_history_label.setFont(QFont("Arial", 12))
            no_history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.history_layout.addWidget(no_history_label)

    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)

    def closeEvent(self, event):
        """Ensure the database connection is closed when the window is closed."""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
        super().closeEvent(event)

    def apply_styling(self, dark_mode):
        """Apply light or dark mode styles with a border."""
        border_style = "border: 2px solid black;" if not dark_mode else "border: 2px solid white;"
        self.setStyleSheet(f"""
            QWidget#main_widget_container {{
                {border_style}
            }}
        """ + (DARK_MODE_STYLE if dark_mode else LIGHT_MODE_STYLE))

    def mousePressEvent(self, event):
        """Handle mouse press event to start dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._drag_start_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move event to drag the window."""
        if self._is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """Handle mouse release event to stop dragging."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False
            event.accept()
