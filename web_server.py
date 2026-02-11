from flask import Flask, render_template, Response
import cv2
import time
import config
from camera_svc import CameraService
from gps_svc import GPSService
from ai_inference import AIModel
import utils
import alert_svc

app = Flask(__name__)

# Initialize Services Global
# In a real production app, use proper app context or extensions, 
# but for this script, global is fine.
gps = None
cam = None
ai = None

def check_proximity(box1, box2, threshold_ratio=0.8):
    # Checks if two boxes are close (for Dog Bite or Accident logic)
    # box: [x1, y1, x2, y2]
    w1 = box1[2] - box1[0]
    w2 = box2[2] - box2[0]
    avg_width = (w1 + w2) / 2
    
    c1_x = (box1[0] + box1[2]) / 2
    c2_x = (box2[0] + box2[2]) / 2
    
    distance = abs(c1_x - c2_x)
    return distance < (avg_width * threshold_ratio)

def generate_frames():
    global cam, gps, ai
    
    # Ensure services are started
    if not cam: start_services()
    
    last_alert_time = 0

    while True:
        frame = cam.get_frame()
        if frame is None:
            # If no frame, yield a blank or loading frame?
            # Or just wait a bit.
            time.sleep(0.1)
            continue
        
        # 1. Run AI (Get detections from BOTH brains)
        detections, annotated_frame = ai.run_inference(frame)
        
        incident_type = None
        
        # 2. Analyze Detections
        
        # A. High Priority: Violence / Weapon (From New Model)
        danger_signals = [d for d in detections if d['type'] == 'danger']
        if danger_signals:
            # Pick the highest confidence danger
            top_danger = max(danger_signals, key=lambda x: x['conf'], default=None)
            if top_danger:
                incident_type = f"CRITICAL: {top_danger['label']} Detected!"

        # B. Medium Priority: Interaction Logic (From General Model)
        if not incident_type:
            gen_signals = [d for d in detections if d['type'] == 'general']
            dogs = [d for d in gen_signals if d['label'] == 'dog']
            persons = [d for d in gen_signals if d['label'] == 'person']
            cars = [d for d in gen_signals if d['label'] == 'car']
            
            # Logic: Dog Bite (Dog + Person close)
            for dog in dogs:
                for person in persons:
                    if check_proximity(dog['box'], person['box'], 0.5):
                        incident_type = "Dog Bite Risk Detected"
                        break
            
            # Logic: Road Accident
            # (Kept simple as per main.py)
            pass 

        # 3. Trigger Alert
        current_time = time.time()
        if incident_type and (current_time - last_alert_time > config.ALERT_COOLDOWN):
            print(f"!!! ALARM: {incident_type} !!!")
            
            lat, lon = gps.get_location()
            frame_buffer = cam.get_buffer()
            # Note: save_evidence might print to console, which is fine
            # We run this in background thread ideally, but for now inline is okay 
            # as long as it doesn't block video too much.
            # actually save_evidence uses cv2.imwrite which is fast.
            img_path, vid_path = utils.save_evidence(frame_buffer, annotated_frame, incident_type)
            
            # Send alert (async usually, but here in main thread is ok for demo)
            # alert_svc.send_alert might block if network is slow.
            # Todo: make alert_svc async if needed.
            alert_svc.send_alert(incident_type, lat, lon, img_path, vid_path)
            
            last_alert_time = current_time

            # Update frame with Red Border or Text to show alert on web?
            # annotated_frame is already drawn by ai.run_inference, 
            # maybe add extra text for incident_type
            cv2.putText(annotated_frame, f"ALERT: {incident_type}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Encode Frame
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        if not ret: continue
            
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_services():
    global cam, gps, ai
    print("Starting Services...")
    gps = GPSService()
    gps.start()
    cam = CameraService()
    cam.start()
    ai = AIModel()
    print("Services Started.")

if __name__ == "__main__":
    start_services()
    # Host 0.0.0.0 is crucial for Selfmade Ninja Lab port forwarding
    app.run(host='0.0.0.0', port=5000, debug=False)
