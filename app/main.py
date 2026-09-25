import sys
import signal
from PySide6.QtWidgets import QApplication
from .launcher import Launcher
from .hotkey import register_hotkey

def main():
    app = QApplication(sys.argv)
    
    launcher = Launcher()
    register_hotkey(launcher)
    
    print("AI Assistant started. Press Ctrl+Shift+Space to launch.")
    
    # Allow Ctrl+C to close the Qt event loop from the terminal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
