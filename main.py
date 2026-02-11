import time
import cv2
import config
from camera_svc import CameraService
from gps_svc import GPSService
from ai_inference import AIModel
import utils
import alert_svc

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

def main():
    print("---------------------------------------------------")
    print("   Smart Command Center (Dual AI) - Starting...    ")
    print("---------------------------------------------------")

    gps = GPSService()
    gps.start()
    cam = CameraService()
    cam.start()
    ai = AIModel()
    
    time.sleep(2)
    print("System Monitoring Active. Press 'q' to exit.")

    last_alert_time = 0

    try:
        while True:
            frame = cam.get_frame()
            if frame is None: continue
            
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
                
                # Logic: Road Accident (Car + Person close OR just Car for demo)
                # For demo, we keep 'Car Detected' as traffic monitor if no other danger
                if not incident_type and cars:
                     # Uncomment below to make it strict (Car + Person overlap)
                     # But for demo, let's keep it responsive:
                     pass # incident_type = "Vehicle Spotted (Monitor)" 

            # 3. Trigger Alert
            current_time = time.time()
            if incident_type and (current_time - last_alert_time > config.ALERT_COOLDOWN):
                print(f"!!! ALARM: {incident_type} !!!")
                
                lat, lon = gps.get_location()
                frame_buffer = cam.get_buffer()
                img_path, vid_path = utils.save_evidence(frame_buffer, annotated_frame, incident_type)
                alert_svc.send_alert(incident_type, lat, lon, img_path, vid_path)
                
                last_alert_time = current_time

            # Display
            cv2.imshow("Smart Surveillance Feed", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        cam.stop()
        gps.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
