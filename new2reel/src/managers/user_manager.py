import json
import os
from datetime import datetime

DATA_FILE = os.path.join("data", "database.json")

class UserManager:
    def __init__(self):
        self._ensure_db()
        self.data = self._load_data()

    def _ensure_db(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(DATA_FILE):
            # Default schema for open source user
            default_data = {
                "videos_generated": 0,
                "history": [],
                "favorites": [],
                "settings": {"auto_save": True}
            }
            with open(DATA_FILE, "w") as f:
                json.dump(default_data, f)

    def _load_data(self):
        with open(DATA_FILE, "r") as f:
            return json.load(f)

    def _save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

    def add_video_to_history(self, title, path, duration="30s"):
        video_entry = {
            "title": title,
            "path": path,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "views": 0,
            "duration": duration,
            "id": len(self.data["history"]) + 1
        }
        self.data["history"].append(video_entry)
        self.data["videos_generated"] += 1
        self._save_data()
        return video_entry

    def delete_video(self, video_id):
        self.data["history"] = [v for v in self.data["history"] if v.get("id") != video_id]
        self._save_data()

    def get_history(self):
        # Return reversed to show newest first
        return self.data["history"][::-1]

    def get_stats(self):
        return {
            "generated": self.data["videos_generated"],
            "projects": len(self.data["history"])
        }
