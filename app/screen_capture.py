import io
import time
from pathlib import Path
import mss
from PIL import Image

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "temp_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

def capture_primary_screen() -> Path:
    """Captures the primary monitor and saves it to a temporary PNG."""
    with mss.mss() as sct:
        # Index 1 is typically the primary monitor in mss
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        filename = SCREENSHOT_DIR / f"screenshot_{int(time.time() * 1000)}.png"
        img.save(filename, "PNG")
        
        return filename
