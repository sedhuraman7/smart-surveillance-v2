from datetime import datetime
try:
    from pymongo import MongoClient
except ImportError:
    print("[WARN] PyMongo not found. Install via 'pip install pymongo'")
    MongoClient = None

import os

# Configuration
# Usually in Selfmade Labs, these are env vars:
# MONGO_HOST = os.getenv('MONGO_HOST', 'mongodb.selfmade.ninja')
# MONGO_PORT = int(os.getenv('MONGO_PORT', 27017))
# MONGO_USER = os.getenv('MONGO_USER', 'ninja')
# MONGO_PASS = os.getenv('MONGO_PASS', 'ninja')

# Hardcoded for now based on typical Lab setup (You might need to update credentials)
# Password '@' is encoded as '%40'
MONGO_URI = "mongodb://Sedhuraman:sedhuraman%407777@mongodb.selfmade.ninja:27017/?authSource=Sedhuraman"
DB_NAME = "Sedhuraman"
COLLECTION_NAME = "incidents"

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.enabled = False
        
        if MongoClient:
            try:
                # Attempt Connection
                # Note: This might need specific credentials from your Lab Dashboard -> MongoDB -> Manage
                self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
                # Check connection
                self.client.server_info() 
                
                self.db = self.client[DB_NAME]
                self.collection = self.db[COLLECTION_NAME]
                self.enabled = True
                print("[DB] Connected to MongoDB Successfully! 🚀")
            except Exception as e:
                print(f"[DB] Connection Failed: {e}")
                self.enabled = False
        else:
            print("[DB] PyMongo library missing. Database disabled.")

    def log_incident(self, incident_type, image_path, video_path=None, location=None):
        if not self.enabled: return
        
        record = {
            "timestamp": datetime.now(),
            "type": incident_type,
            "image": image_path,
            "video": video_path,
            "location": location or "Unknown",
            "status": "Unreviewed"
        }
        
        try:
            self.collection.insert_one(record)
            print("[DB] Incident Logged to Database.")
        except Exception as e:
            print(f"[DB] Insert Failed: {e}")

    def get_recent_incidents(self, limit=20):
        if not self.enabled: return []
        
        try:
            return list(self.collection.find().sort("timestamp", -1).limit(limit))
        except Exception as e:
            print(f"[DB] Fetch Failed: {e}")
            return []

# Singleton Instance
db = DatabaseService()
