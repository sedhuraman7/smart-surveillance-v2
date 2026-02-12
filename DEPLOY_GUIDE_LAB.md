# Deployment Guide for Selfmade Ninja Lab 🚀

Congratulations on getting your hands on a Selfmade Ninja Lab! Let's get your **Smart Surveillance System** up and running in the cloud.

Because the Lab is a remote server (Ubuntu), it doesn't have a physical USB camera attached. We will run it in **Web Dashboard Mode** and use a **Video File** to simulate the camera feed.

## 1. Prepare Your Local Code (Already Done!) ✅

I have already:
- Created `web_server.py` to launch a beautiful dashboard.
- Created `templates/index.html` for the interface.
- Updated `requirements.txt` with Flask.
- Configured `.gitignore` to skip large files.
- Initialized a local Git repository.

## 2. Push Code to GitHub / GitLab ☁️

1.  **Create a Blank Repository** on GitHub or GitLab (name it `smart-surveillance-v2`).
2.  **Push your code** from your local terminal:

```bash
git remote add origin <YOUR_REPO_URL>
git branch -M main
git push -u origin main
```

*(Note: Replace `<YOUR_REPO_URL>` with your actual repository URL).*

## 3. Clone in Selfmade Ninja Lab 🖥️

1.  Open your **Lab Terminal** (the black screen in your browser).
2.  Clone your repository:

```bash
git clone <YOUR_REPO_URL>
cd smart-surveillance-v2
```

## 4. Setup Environment 🛠️

Run these commands in the Lab Terminal to install Python libraries:

```bash
pip install -r requirements.txt
# If pip is not found, try: pip3 install -r requirements.txt
# If you get permission errors, use: pip install --user -r requirements.txt
```

## 5. Upload a Test Video 📹

Since there is no webcam, you need a video file to analyze.
1.  Upload a video file (e.g., `test_video.mp4`) to the `smart-surveillance-v2` folder in the Lab. 
    - You can use the **File Manager** (if available in dashboard) OR `scp` OR `wget` a sample video.
2.  Edit `config.py` in the Lab:
    - Open the file: `nano config.py`
    - Change `CAMERA_INDEX = 0` to `CAMERA_INDEX = "test_video.mp4"` (use the upload filename).
    - Save and exit (Ctrl+X, Y, Enter).

## 6. Run the System 🚀

Start the web server:

```bash
python web_server.py
```

It should say "Running on http://0.0.0.0:5000".

## 7. Connect via "New Domain" 🌐

1.  Go to the **Selfmade Ninja Dashboard**.
2.  Look for **"Port Forwarding"** or **"New Domain"** feature.
3.  Create a new domain mapping:
    - **Port**: `5000` (This is where our Flask app runs).
    - **Protocol**: HTTP/TCP.
4.  Open the generate URL (e.g., `https://surveillance-user.selfmade.ninja`).
5.  **Wow!** You should see your Smart Dashboard live! 🎉

---

### Troubleshooting
- **Display Error**: If you see "Can't open display", make sure you are running `web_server.py`, NOT `main.py`. `main.py` requires a desktop monitor.
- **Slow Video**: The lab might be slow for AI inference. If so, edit `config.py` in the lab and reduce resolution (`FRAME_WIDTH = 640`).
