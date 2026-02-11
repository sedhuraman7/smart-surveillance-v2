import requests
import json
import threading
import config

def send_alert(incident_type, lat, lon, image_path, video_path):
    """
    Sends alert to the server in a separate thread to avoid blocking main loop.
    """
    t = threading.Thread(target=_send_alert_task, args=(incident_type, lat, lon, image_path))
    t.start()

def _send_alert_task(incident_type, lat, lon, image_path):
    print(f"--- [ALERT TRIGGERED] ---")
    print(f"Type: {incident_type}")
    print(f"Location: {lat}, {lon}")
    print(f"Evidence: {image_path}")
    
    payload = {
        "device_id": config.DEVICE_ID,
        "incident_type": incident_type,
        "latitude": lat,
        "longitude": lon,
        "timestamp": "Now"
    }
    
    # Example API Call (Commented out effectively)
    try:
        # files = {'image': open(image_path, 'rb')}
        # response = requests.post(config.SERVER_URL, data=payload, files=files, timeout=5)
        # print("Server Response:", response.status_code)
        
        # Simulating Network Delay
        import time
        time.sleep(1) 
        print(">> Alert Sent Successfully to Head Office (Simulated)")
        
    except Exception as e:
        print(f"Failed to send alert: {e}")
