# Smart Incident Detection and Auto Alert Surveillance System
## Project Documentation & Setup Guide

### 1. Hardware Requirements
- **Core**: Raspberry Pi 4 (4GB or 8GB RAM recommended for AI)
- **Vision**: Raspberry Pi Standard Camera Module (Type B) or High Quality USB Webcam
- **Location**: Neo-6M GPS Module (UART Interface)
- **Power**: 5V 3A USB-C Power Supply (Critical for AI loads)
- **Connectivity**: WiFi or Ethernet

### 2. Wiring Diagram (GPIO Header)

#### GPS Module (Neo-6M)
| GPS Pin | Raspberry Pi Pin | Description          |
|---------|------------------|----------------------|
| VCC     | Pin 1 (3.3V)     | Power (Prefer 3.3V)  |
| GND     | Pin 6 (GND)      | Ground               |
| TX      | Pin 10 (GPIO 15) | Receive Data (RXD)   |
| RX      | Pin 8 (GPIO 14)  | Transmit Data (TXD)  |

#### Camera
- Connect to the CSI port (ensure ribbon cable silver pins face the HDMI port).

### 3. Installation Commands
Run these commands on your Raspberry Pi Terminal:

```bash
# 1. Update System
sudo apt update && sudo apt upgrade -y

# 2. Enable Serial Port (raspi-config -> Interface -> Serial Port -> Login Shell:NO, HW:YES)
sudo raspi-config

# 3. Create Project Directory
mkdir -p ~/smart_surveillance
cd ~/smart_surveillance

# 4. Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 5. Install Dependencies (from requirements.txt)
pip install -r requirements.txt
```

### 4. How to Run
```bash
python main.py
```
