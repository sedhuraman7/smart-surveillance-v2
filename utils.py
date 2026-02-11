import cv2
import os
import datetime
import config

def ensure_evidence_dir():
    if not os.path.exists(config.LOCATION_SAVE_DIR):
        os.makedirs(config.LOCATION_SAVE_DIR)

def save_evidence(frame_buffer, current_frame, incident_type):
    """
    Saves last 10 seconds of video (from buffer) and current image.
    frame_buffer: list of recent frames (queue)
    """
    ensure_evidence_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sanitize filename (Windows doesn't like :)
    safe_incident = incident_type.replace(":", "").replace("!", "").replace(" ", "_")
    
    # 1. Save Image
    image_filename = f"{config.LOCATION_SAVE_DIR}/{safe_incident}_{timestamp}.jpg"
    cv2.imwrite(image_filename, current_frame)
    
    # 2. Save Video Clip
    # Assuming buffer has frames from past X seconds. 
    # We write them to a file.
    video_filename = f"{config.LOCATION_SAVE_DIR}/{safe_incident}_{timestamp}.mp4"
    
    if not frame_buffer:
        return image_filename, None

    height, width, _ = frame_buffer[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID'
    out = cv2.VideoWriter(video_filename, fourcc, config.FPS, (width, height))
    
    for f in frame_buffer:
        out.write(f)
    out.write(current_frame) # Add the incident frame
    out.release()
    
    print(f"[EVIDENCE] Saved: {image_filename} & {video_filename}")
    return image_filename, video_filename

def draw_overlay(frame, text):
    cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return frame
