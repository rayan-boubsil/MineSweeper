import json
import os

class ScoreManager:
    """Handles loading and saving high scores using JSON."""
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        """Read scores from file or return defaults if file doesn't exist."""
        if not os.path.exists(self.filename):
            return [
                {"mode": "CLASSIC", "name": "BOT_1", "time": "00:59"},
                {"mode": "FRENZY",  "name": "BOT_2", "time": "01:30"}
            ]
        
        # ADDED: Safety check for corrupted files
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Warning: scores.json is corrupted. Resetting scores.")
            return []

    def add_score(self, mode, name, time_str):
        """Add a new score and save it to the file."""
        # IMPROVED: Force upper case for consistent UI
        new_entry = {
            "mode": mode.upper(), 
            "name": name.upper(), 
            "time": time_str
        }
        self.scores.append(new_entry)
        # Sort by time (MM:SS string comparison works perfectly)
        self.scores.sort(key=lambda x: x['time'])
        # Keep only the top 10 (5 is a bit short for multiple modes!)
        self.scores = self.scores[:10]
        self.save_all()

    def save_all(self):
        """Write the current scores list to the JSON file."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError as e:
            print(f"FileSystem Error: {e}")