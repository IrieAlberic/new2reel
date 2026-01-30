import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

try:
    from src.editor import VideoEditor
    print("VideoEditor imported successfully!")
except Exception as e:
    print(f"Failed to import VideoEditor: {e}")
