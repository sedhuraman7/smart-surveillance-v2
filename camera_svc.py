import cv2
import threading
import time
from collections import deque
import config

class CameraService:
    def __init__(self):
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        # Set Resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, config.FPS)
        
        self.running = False
        self.current_frame = None
        self.lock = threading.Lock()
        
        # Buffer to store last 10 seconds of video
        # FPS * 10 seconds. Assuming approx 20-30 FPS actual.
        buffer_size = config.FPS * 10 
        self.frame_buffer = deque(maxlen=buffer_size)

    def start(self):
        if not self.cap.isOpened():
            print("[CAMERA ERROR] Could not open camera.")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)
        self.thread.start()

    def _capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.current_frame = frame
                    self.frame_buffer.append(frame)
            else:
                # If reading from a file, loop it!
                if isinstance(config.CAMERA_INDEX, str):
                    print("[CAMERA] Video file ended. Restarting...")
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    continue
                
                print("[CAMERA] Frame read failed. Retrying...")
                time.sleep(1)
            time.sleep(0.01) # Small sleep to prevent CPU hogging

    def get_frame(self):
        with self.lock:
            return self.current_frame if self.current_frame is not None else None

    def get_buffer(self):
        with self.lock:
            return list(self.frame_buffer)

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
