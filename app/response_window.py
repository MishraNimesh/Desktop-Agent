from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PySide6.QtCore import Qt

class ResponseWindow(QDialog):
    """Displays the final AI answer in a styled, frameless window."""
    def __init__(self, answer: str, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("AI Answer")
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; border-radius: 8px; padding: 12px; }
            QTextEdit { background-color: #1e1e1e; color: #f0f0f0; border: none; font-size: 11pt; }
            QPushButton { background-color: #3a3a3a; color: #f0f0f0; border: none; padding: 6px 12px; margin-top: 8px; border-radius: 4px; }
            QPushButton:hover { background-color: #505050; }
        """)
        self.init_ui(answer)

    def init_ui(self, answer: str):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        
        label = QLabel("Answer:")
        label.setStyleSheet("color:#f0f0f0;font-weight:bold;")
        layout.addWidget(label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlainText(answer)
        layout.addWidget(self.text_edit)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.adjustSize()
        
        # Center the window on the active screen
        screen = self.screen()
        if screen:
            self.move(screen.geometry().center() - self.rect().center())
