from ultralytics import YOLO
import config
import cv2

class AIModel:
    def __init__(self):
        print(f"[AI] Loading General Model: {config.MODEL_GENERAL_PATH}...")
        self.model_gen = YOLO(config.MODEL_GENERAL_PATH)
        
        print(f"[AI] Loading Violence Model: {config.MODEL_VIOLENCE_PATH}...")
        try:
            self.model_vio = YOLO(config.MODEL_VIOLENCE_PATH)
            self.has_violence_model = True
        except Exception as e:
            print(f"[WARNING] 'best.pt' not found. Violence detection will be disabled. Error: {e}")
            self.has_violence_model = False
            
        print("[AI] Systems Ready.")

    def run_inference(self, frame):
        """
        Runs logic on BOTH models and combines results.
        OPTIMIZED: Only Cars + Violence. Resizes frame for speed.
        """
        # OPTIMIZATION: Resize frame for faster AI processing
        # 320x320 is good enough for large objects like Cars/Guns
        input_frame = cv2.resize(frame, (320, 320)) 
        
        combined_detections = []
        annotated_frame = frame.copy() # Draw on original resolution frame
        
        # Scaling factor to map 320x boxes back to ORIGINAL frame size
        scale_x = frame.shape[1] / 320
        scale_y = frame.shape[0] / 320
        
        # 1. Run General Model (Car Only) 🚗
        # Classes: 2=car (Removed 0=person, 16=dog)
        results_gen = self.model_gen(input_frame, verbose=False, conf=config.CONF_GENERAL, classes=[2])
        for r in results_gen:
            # We must map boxes back to original size manually since we resized input
            for box in r.boxes:
                # Get coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # Scale back
                x1, x2 = x1 * scale_x, x2 * scale_x
                y1, y2 = y1 * scale_y, y2 * scale_y
                
                # Draw Box (Green for General)
                cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                cls_id = int(box.cls[0])
                label = self.model_gen.names[cls_id]
                cv2.putText(annotated_frame, label, (int(x1), int(y1)-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                
                combined_detections.append({
                    "type": "general",
                    "label": label,
                    "box": [x1, y1, x2, y2],
                    "conf": float(box.conf[0])
                })

        # 2. Run Violence Model (Critical Priority) 👊🔪
        if self.has_violence_model:
            results_vio = self.model_vio(input_frame, verbose=False, conf=config.CONF_VIOLENCE)
            for r in results_vio:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = self.model_vio.names[cls_id]
                    
                    if label.lower() != "normal":
                        # Scale back
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        x1, x2 = x1 * scale_x, x2 * scale_x
                        y1, y2 = y1 * scale_y, y2 * scale_y
                        
                        # Draw RED box for Danger
                        cv2.rectangle(annotated_frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 3)
                        cv2.putText(annotated_frame, f"DANGER: {label}", (int(x1), int(y1)-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                        
                        combined_detections.append({
                            "type": "danger",
                            "label": label, 
                            "box": [x1, y1, x2, y2],
                            "conf": float(box.conf[0])
                        })
        
        return combined_detections, annotated_frame
