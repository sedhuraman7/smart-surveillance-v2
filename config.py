import os

# System Configuration
DEVICE_ID = "PI_SURVEILLANCE_01"
LOCATION_SAVE_DIR = "evidence"

# Simulation Mode
IS_SIMULATION = True 

# Camera Settings
# Camera Settings
# For Selfmade Ninja Lab, upload a video file and use its path string e.g. "path/to/video.mp4"
CAMERA_INDEX = 0  # 0 for Webcam, or string "video.mp4" for file simulation
FRAME_WIDTH = 1280 
FRAME_HEIGHT = 720
FPS = 30

# GPS Settings
GPS_SERIAL_PORT = "COM3"
GPS_BAUD_RATE = 9600

# AI Models (DUAL POWER)
MODEL_GENERAL_PATH = "yolov8n.pt"  # Detects Car, Dog, Person
MODEL_VIOLENCE_PATH = "best.pt"    # Detects Violence, Gun, Knife

# Confidence
CONF_GENERAL = 0.50
CONF_VIOLENCE = 0.40 # Custom models might need lower confidence initially

# Alert Cooldown (Seconds)
ALERT_COOLDOWN = 10 
