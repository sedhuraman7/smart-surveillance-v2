import cv2
import requests
import time
import numpy as np
import threading

# Configuration
SERVER_URL = "http://YOUR_LAB_URL_HERE:5000/upload_frame" 
# Example: http://surveillance.labs.selfmade.ninja/upload_frame

CAMERA_INDEX = 0  # 0 for USB Cam, "libcamerasrc ..." for Pi Cam
FRAME_WIDTH = 640 # Keep low for faster upload
FRAME_HEIGHT = 480
FPS = 15          # Don't overload network

def main():
    print("---------------------------------------------------")
    print("   Raspberry Pi Camera Streamer (Client)           ")
    print("---------------------------------------------------")
    
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, FPS)
    
    if not cap.isOpened():
        print("[ERROR] Camera not found!")
        return

    print(f"Connecting to Server: {SERVER_URL}")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Frame read failed.")
            time.sleep(1)
            continue
        
        # Optimize: Resize/Compress before sending
        # Resize if huge (e.g. 1080p -> 640p)
        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        
        # Encode to JPEG (Quality 80 is good balance)
        _, img_encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        data = img_encoded.tobytes()
        
        try:
            # Send to Server (HTTP POST)
            response = requests.post(
                SERVER_URL, 
                data=data, 
                headers={'Content-Type': 'application/octet-stream'}
            )
            
            if response.status_code == 200:
                print(".", end="", flush=True) # Success indicator
            else:
                print("x", end="", flush=True) # Fail indicator
                
        except Exception as e:
            print(f"\n[ERROR] Connection Failed: {e}")
            time.sleep(1) # Backoff
            
        # Optional Local Preview (If Pi has monitor)
        # cv2.imshow('Pi Camera Local', frame)
        # if cv2.waitKey(1) == ord('q'): break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
