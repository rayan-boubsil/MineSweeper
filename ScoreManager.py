import json
import os

class ScoreManager:
    """Handles high scores for a single game mode."""
    def __init__(self, filename="scores.json"):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        if not os.path.exists(self.filename):
            # Valeurs par défaut simplifiées (plus de clé "mode")
            return [
                {"name": "ALPHA", "time": "00:45"},
                {"name": "BETA",  "time": "01:10"}
            ]
        
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def add_score(self, name, time_str):
        """Add a new score (mode is implicit now)."""
        new_entry = {
            "name": name.upper(),
            "time": time_str
        }
        self.scores.append(new_entry)
        
        # Tri toujours basé sur le temps
        self.scores.sort(key=lambda x: x['time'])
        
        # On garde le Top 10
        self.scores = self.scores[:10]
        self.save_all()

    def save_all(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError as e:
            print(f"Error saving scores: {e}")