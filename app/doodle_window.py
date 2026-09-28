from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QInputDialog
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QPainter, QPen, QColor, QPainterPath

from .screen_capture import capture_primary_screen
from .gemini_client import analyze_image, GeminiError
from .response_window import ResponseWindow

class DoodleWindow(QWidget):
    """A full-screen, transparent window that lets the user draw over their screen."""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        screen = self.screen()
        if screen:
            self.setGeometry(screen.geometry())

        self.paths = []
        self.current_path = None
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        
        self.done_btn = QPushButton("✅ Done")
        self.done_btn.setStyleSheet("""
            QPushButton { background-color: #2b2b2b; color: #f0f0f0; border-radius: 8px; padding: 12px 24px; font-size: 12pt; font-weight: bold; border: 2px solid #505050; }
            QPushButton:hover { background-color: #3a3a3a; border-color: #4CAF50; }
        """)
        self.done_btn.clicked.connect(self.finish_doodle)
        
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton { background-color: #2b2b2b; color: #f0f0f0; border-radius: 8px; padding: 12px 24px; font-size: 12pt; font-weight: bold; border: 2px solid #505050; margin-left: 10px; }
            QPushButton:hover { background-color: #3a3a3a; border-color: #F44336; }
        """)
        self.cancel_btn.clicked.connect(self.close)

        top_layout.addWidget(self.done_btn)
        top_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(top_layout)
        layout.addStretch()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_path = QPainterPath()
            self.current_path.moveTo(event.position())
            self.paths.append(self.current_path)

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.current_path is not None:
            self.current_path.lineTo(event.position())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.current_path = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fill with a nearly invisible color so Windows catches mouse events
        painter.fillRect(self.rect(), QColor(255, 255, 255, 1))
        
        pen = QPen(QColor(255, 60, 60, 220))
        pen.setWidth(6)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
        
        for path in self.paths:
            painter.drawPath(path)

    def finish_doodle(self):
        self.done_btn.hide()
        self.cancel_btn.hide()
        
        QCoreApplication.processEvents()
        
        try:
            screenshot_path = capture_primary_screen()
        except Exception as e:
            print(f"Capture failed: {e}")
            self.close()
            return

        self.close()
        
        question, ok = QInputDialog.getText(None, "Ask", "What is your question about your doodle?")
        if not ok or not question.strip():
            return
            
        try:
            answer = analyze_image(screenshot_path, question.strip())
            resp_win = ResponseWindow(answer)
            resp_win.exec()
        except GeminiError as e:
            print(str(e))

