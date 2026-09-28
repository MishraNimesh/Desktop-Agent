from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QInputDialog
from PySide6.QtCore import Qt, Signal, Slot
from .screen_capture import capture_primary_screen
from .gemini_client import analyze_image, GeminiError
from .response_window import ResponseWindow

class Launcher(QDialog):
    # Qt Signal to safely show the window from the hotkey thread
    show_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowTitle("AI Assistant")
        self.setStyleSheet("""
            QDialog { background-color: #2b2b2b; border-radius: 8px; padding: 12px; }
            QLabel { color: #f0f0f0; font-size: 14pt; font-weight: bold; margin-bottom: 8px; text-align: center; }
            QPushButton { background-color: #3a3a3a; color: #f0f0f0; border: none; padding: 8px 12px; margin: 4px; border-radius: 4px; font-size: 12pt; }
            QPushButton:hover { background-color: #505050; }
        """)
        self.init_ui()
        self.show_signal.connect(self._show)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(QLabel("✦ AI Assistant"))
        
        screen_btn = QPushButton("🖥 Screen")
        screen_btn.clicked.connect(self.handle_screen)
        layout.addWidget(screen_btn)

        doodle_btn = QPushButton("✏ Doodle")
        doodle_btn.clicked.connect(self.handle_doodle)
        layout.addWidget(doodle_btn)
        
        self.setLayout(layout)
        self.adjustSize()
        
        screen = self.screen()
        if screen:
            self.move(screen.geometry().center() - self.rect().center())

    @Slot()
    def _show(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def show_launcher(self):
        self.show_signal.emit()

    def handle_doodle(self):
        self.hide()
        from .doodle_window import DoodleWindow
        self.doodle_win = DoodleWindow()
        self.doodle_win.show()

    def handle_screen(self):
        self.hide()
        
        try:
            screenshot_path = capture_primary_screen()
        except Exception as e:
            self._show_error(f"Capture failed: {e}")
            return
            
        question, ok = QInputDialog.getText(self, "Ask", "Enter your question:")
        if not ok or not question.strip():
            return
            
        try:
            answer = analyze_image(screenshot_path, question.strip())
        except GeminiError as e:
            self._show_error(str(e))
            return
            
        resp_win = ResponseWindow(answer)
        resp_win.exec()

    def _show_error(self, msg: str):
        err_dialog = QDialog(self)
        err_dialog.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        err_dialog.setStyleSheet("background-color:#3a3a3a;color:#ff6666;padding:10px;border-radius:5px;")
        
        layout = QVBoxLayout(err_dialog)
        layout.addWidget(QLabel(msg))
        err_dialog.setLayout(layout)
        err_dialog.adjustSize()
        err_dialog.show()
        
        from PySide6.QtCore import QTimer
        QTimer.singleShot(3000, err_dialog.close)
