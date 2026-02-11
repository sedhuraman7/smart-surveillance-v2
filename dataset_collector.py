import cv2
import os
import time

# Configuration
SAVE_DIR = "dataset_raw"
CLASSES = ["violence", "chain_snatching", "dog_bite", "accident", "normal"]

# Ensure directories exist
for cls in CLASSES:
    os.makedirs(f"{SAVE_DIR}/{cls}", exist_ok=True)

def collect_data():
    cap = cv2.VideoCapture(0) # Use 0 for Laptop Webcam
    
    print("--------------------------------------------------")
    print("   DATASET COLLECTOR TOOL - Smart Surveillance    ")
    print("--------------------------------------------------")
    print("Press these keys to save images:")
    print(" [V] - Violence / Fighting (Act it out!)")
    print(" [C] - Chain Snatching (Act it out!)")
    print(" [D] - Dog Bite (Point at a dog photo or simulation)")
    print(" [A] - Accident (Point at a toy car crash or monitor)")
    print(" [N] - Normal / Nothing (Very Important!)")
    print(" [Q] - Quit")
    print("--------------------------------------------------")

    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret: break

        cv2.imshow("Data Collector", frame)
        key = cv2.waitKey(1) & 0xFF

        save_class = None
        if key == ord('v'): save_class = "violence"
        elif key == ord('c'): save_class = "chain_snatching"
        elif key == ord('d'): save_class = "dog_bite"
        elif key == ord('a'): save_class = "accident"
        elif key == ord('n'): save_class = "normal"
        elif key == ord('q'): break

        if save_class:
            timestamp = int(time.time() * 1000)
            filename = f"{SAVE_DIR}/{save_class}/{save_class}_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            count += 1
            print(f"[{count}] Saved -> {filename}")

    cap.release()
    cv2.destroyAllWindows()
    print("Collection Finished!")

if __name__ == "__main__":
    collect_data()
