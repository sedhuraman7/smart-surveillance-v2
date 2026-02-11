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
        """
        combined_detections = []
        annotated_frame = frame.copy()
        
        # 1. Run General Model (Car, Dog, Person)
        # Classes: 0=person, 2=car, 16=dog
        results_gen = self.model_gen(frame, verbose=False, conf=config.CONF_GENERAL, classes=[0, 2, 16])
        for r in results_gen:
            annotated_frame = r.plot() # Draw basic boxes
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = self.model_gen.names[cls_id]
                combined_detections.append({
                    "type": "general",
                    "label": label,
                    "box": box.xyxy[0].tolist(),
                    "conf": float(box.conf[0])
                })

        # 2. Run Violence Model (If available)
        if self.has_violence_model:
            results_vio = self.model_vio(frame, verbose=False, conf=config.CONF_VIOLENCE)
            for r in results_vio:
                # We expect classes like: 'Violent', 'Gun', 'Knife', 'Normal'
                # Note: We Ignore 'Normal' class if present to save space
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = self.model_vio.names[cls_id]
                    
                    if label.lower() != "normal":
                        # Draw RED box for Danger
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                        cv2.putText(annotated_frame, f"DANGER: {label}", (x1, y1-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                        
                        combined_detections.append({
                            "type": "danger",
                            "label": label, # 'Violent', 'Gun'
                            "box": box.xyxy[0].tolist(),
                            "conf": float(box.conf[0])
                        })
        
        return combined_detections, annotated_frame
