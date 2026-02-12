# Raspberry Pi Setup Guide 🍓

This guide will help you set up your Raspberry Pi to act as the "Camera Client". It will capture video and send it to your Selfmade Ninja Lab for AI processing.

## 1. Prerequisites 📋
- Raspberry Pi (3, 4, or 5 recommended)
- MicroSD Card (16GB+) with **Raspberry Pi OS** installed.
- USB Webcam OR Raspberry Pi Camera Module.
- Internet Connection (WiFi or Ethernet).

## 2. Connect Hardware 🔌
1.  Connect your **Camera** to the Pi.
2.  Connect **Power** to turn on the Pi.
3.  Connect a **Monitor & Keyboard** (or ANY SSH terminal).

## 3. Install Software Dependencies 🐍
Open the **Terminal** on your Raspberry Pi and run these commands:

1.  **Update System:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

2.  **Install Python & Pip:**
    ```bash
    sudo apt install python3-pip python3-opencv -y
    ```

3.  **Install Required Libraries:**
    ```bash
    pip3 install requests opencv-python --break-system-packages
    # Note: On newer Pi OS, '--break-system-packages' prevents errors.
    ```

## 4. Get the Code 📥

You only need one file: `pi_client.py`.

**Option A: Clone from GitHub (Recommended)**
```bash
git clone https://github.com/sedhuraman7/smart-surveillance-v2.git
cd smart-surveillance-v2
```

**Option B: Copy Manually**
- Create a new file: `nano pi_client.py`
- Paste the code from `pi_client.py` (from your laptop).
- Save and exit (`Ctrl+X`, `Y`, `Enter`).

## 5. Configure the Server URL 🔗

**CRITICAL STEP:** You need to tell the Pi **where** to send the video.

1.  Open the file:
    ```bash
    nano pi_client.py
    ```

2.  Look for this line at the top:
    ```python
    SERVER_URL = "http://YOUR_LAB_URL_HERE:5000/upload_frame"
    ```

3.  Replace `YOUR_LAB_URL_HERE` with your **Selfmade Ninja Lab Domain**.
    - Go to your Lab Dashboard -> **Port Forwarding**.
    - Find the link for **Port 5000** (e.g., `https://surveillance-user.selfmade.ninja`).
    - Update the line:
      ```python
      # Example
      SERVER_URL = "https://surveillance-user.selfmade.ninja/upload_frame"
      ```

4.  Save and exit (`Ctrl+X`, `Y`, `Enter`).

## 6. Run the Camera! 🎬

Start the client:

```bash
python3 pi_client.py
```

### ✅ Expected Output:
- `Connecting to Server...`
- `....................` (Dots mean success!)

If you see `x x x`, it means the Pi cannot reach the Server. Check your URL and Internet.

## 7. View the Result 🌐
Go to your **Lab Dashboard URL** on your laptop/phone. You should see the live video from your Raspberry Pi with AI detection overlay! 🔥
