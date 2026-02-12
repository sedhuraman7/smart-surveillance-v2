from flask import Flask, render_template, Response, request, send_from_directory
import cv2
import numpy as np
import time
import os
from ai_inference import AIModel
import utils
import alert_svc
import threading
import alert_svc
import threading
import config
from database_svc import db

app = Flask(__name__)

# Global storage for the latest frame from Pi
latest_frame = None
lock = threading.Lock()
last_alert_time = 0

# Initialize AI (Runs on Server)
print("[SERVER] Loading AI Models...")
ai = AIModel()
print("[SERVER] AI Ready.")

def process_ai_logic(frame):
    """
    Runs AI detection on the frame and handles alerts.
    Returns the annotated frame.
    """
    # 1. Run AI
    detections, annotated_frame = ai.run_inference(frame)
    
    incident_type = None
    
    # 2. Analyze Detections (Same Logic as before)
    danger_signals = [d for d in detections if d['type'] == 'danger']
    if danger_signals:
        top_danger = max(danger_signals, key=lambda x: x['conf'], default=None)
        if top_danger:
            incident_type = f"CRITICAL: {top_danger['label']} Detected!"

    if not incident_type:
        # Check General Model Logic (Dog Bite etc.)
        gen_signals = [d for d in detections if d['type'] == 'general']
        dogs = [d for d in gen_signals if d['label'] == 'dog']
        persons = [d for d in gen_signals if d['label'] == 'person']
        
        for dog in dogs:
            for person in persons:
                # Simple distance check logic
                # (Reusing proximity logic here would be ideal, simplified for speed)
                pass 

    # 3. Alert Trigger (Simplified for Server)
    # We rely on the AI Class's internal drawings for now.
    current_time = time.time()
    global last_alert_time
    
    if incident_type and (current_time - last_alert_time > config.ALERT_COOLDOWN):
        print(f"!!! SERVER ALERT: {incident_type} !!!")
        
        # Save Evidence (Image & Video)
        # Note: 'frame_buffer' is tricky here as we only get 1 frame at a time.
        # For now, we save JUST the image. Video loop buffer needs more logic.
        print("Saving Evidence...")
        img_path, vid_path = utils.save_evidence([frame], annotated_frame, incident_type)
        
        # Send Alert (Simulated)
        # In real Pi, we might send GPS too. Here we assume static/server location for now.
        location = "13.0827, 80.2707"
        alert_svc.send_alert(incident_type, 13.0827, 80.2707, img_path, vid_path)
        
        # Log to Database
        db.log_incident(incident_type, img_path, vid_path, location)
        
        last_alert_time = current_time
        
    return annotated_frame

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evidence/<path:filename>')
def serve_evidence(filename):
    return send_from_directory('evidence', filename)

@app.route('/gallery')
def gallery():
    evidence_dir = 'evidence'
    if not os.path.exists(evidence_dir):
        os.makedirs(evidence_dir)
        
    files = os.listdir(evidence_dir)
    # Filter for .jpg and .mp4
    files = [f for f in files if f.endswith(('.jpg', '.mp4'))]
    files.sort(reverse=True) # Newest first
    
    return render_template('gallery.html', files=files)

@app.route('/upload_frame', methods=['POST'])
def upload_frame():
    """
    Endpoint for Raspberry Pi to push frames to.
    """
    global latest_frame
    
    try:
        # Read raw bytes from request
        file_bytes = np.frombuffer(request.data, np.uint8)
        # Decode image
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if frame is not None:
            # Process AI immediately (or just store it for a worker thread)
            # For simplicity, we process it here (might slow down FPS slightly but ensures sync)
            processed_frame = process_ai_logic(frame)
            
            with lock:
                latest_frame = processed_frame
                
        return "Received", 200
    except Exception as e:
        print(f"[ERROR] Upload Failed: {e}")
        return "Error", 500

def generate_dashboard_stream():
    """
    Yields the latest processed frames to the web dashboard.
    """
    global latest_frame
    
    while True:
        with lock:
            if latest_frame is None:
                # If no frame yet, wait a bit
                time.sleep(0.1)
                continue
            
            # Encode to JPEG for Browser
            ret, buffer = cv2.imencode('.jpg', latest_frame)
            frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.03) # Cap at ~30 FPS

@app.route('/video_feed')
def video_feed():
    return Response(generate_dashboard_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # Host 0.0.0.0 is crucial for Lab
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
