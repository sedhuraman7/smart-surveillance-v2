# Easy AI Training Guide (Google Colab)

Sir, idhu dhaan "Roboflow Method". Romba simple. Follow pannunga.

### Step 1: Open Google Colab
1.  Click this link: [Open Google Colab](https://colab.research.google.com/#create=true)
2.  (Mukkiyam) Go to Menu: **Runtime** -> **Change runtime type** -> Select **T4 GPU**.
3.  Click **Save**.

### Step 2: Get Dataset (Roboflow)
1.  Go to this link: [Roboflow Universe - Violence](https://universe.roboflow.com/search?q=violence)
2.  Select a dataset (e.g., "Violence Detection" or "Suspicious").
3.  Click **"Download this Dataset"**.
4.  Select Format: **YOLOv8**.
5.  Select **"Show Download Code"**.
6.  Copy that code (It looks like `!pip install roboflow...`).

### Step 3: Train (Copy & Paste this into Colab)
Colab-la first cell-la indha code-a paste panni Run pannunga:

```python
# 1. Install YOLO
!pip install ultralytics

# 2. PASTE YOUR ROBOFLOW CODE HERE (The one you copied)
# Example:
# !pip install roboflow
# from roboflow import Roboflow
# ... (your snippets) ...

# 3. Train the Model
from ultralytics import YOLO

# Load standard brain
model = YOLO("yolov8n.pt") 

# Train on your new data
# Note: 'data.yaml' location might change based on dataset name. 
# Usually it is inside a folder named like the dataset.
# Check the file folder icon on the left to see the name.
model.train(data="/content/datasetname/data.yaml", epochs=50, imgsz=640)
```

### Step 4: Download Result
1.  Wait for training (approx 30 mins - 1 hour).
2.  Go to **Files (Left Icon)** -> `runs` -> `detect` -> `train` -> `weights`.
3.  Right click **`best.pt`** -> Download.
4.  Cop file to `e:\Smart Surveillance System2\` folder.

### Step 5: Update Code
After copying `best.pt`, open `config.py` in your laptop and change:
```python
MODEL_PATH = "best.pt"
CONFIDENCE_THRESHOLD = 0.50 # Reset to 0.5 for custom model
```
