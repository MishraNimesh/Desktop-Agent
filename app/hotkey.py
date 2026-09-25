import keyboard
from .config import HOTKEY
from .launcher import Launcher

_launcher_instance = None

def _hotkey_callback():
    """Trigger the launcher UI to appear on the main Qt thread."""
    if _launcher_instance is not None:
        _launcher_instance.show_launcher()

def register_hotkey(launcher_instance):
    """Registers the global hotkey to show the assistant."""
    global _launcher_instance
    _launcher_instance = launcher_instance
    try:
        keyboard.add_hotkey(HOTKEY, _hotkey_callback)
        print(f"Successfully registered hotkey: {HOTKEY}")
    except Exception as e:
        print(f"Failed to register hotkey: {e}")
