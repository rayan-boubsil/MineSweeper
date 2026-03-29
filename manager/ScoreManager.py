import json
import os

class ScoreManager:
    def __init__(self, filename="scores.json"):
        self.filename = filename
        # On définit d'abord la structure par défaut
        self.scores = {
            "EASY": {"history": [], "best": None},
            "MEDIUM": {"history": [], "best": None},
            "HARD": {"history": [], "best": None}
        }
        # On charge les données par-dessus
        self.load_scores()

    def load_scores(self):
        """Charge les scores et fusionne avec la structure par défaut."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    data = json.load(f)
                    # Sécurité : on vérifie que le fichier a le bon format
                    if isinstance(data, dict) and "EASY" in data:
                        self.scores = data
            except Exception as e:
                print(f"Erreur de lecture du JSON : {e}")

    def save_scores(self):
        """Sauvegarde l'état actuel de self.scores."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except Exception as e:
            print(f"Erreur de sauvegarde : {e}")

    def add_score(self, difficulty, name, time_value):
        diff_key = difficulty.upper()
        if diff_key not in self.scores: 
            return

        # 1. HISTORIQUE (Les 5 derniers)
        new_entry = {"name": name.upper(), "time": time_value}
        self.scores[diff_key]["history"].append(new_entry)
        
        if len(self.scores[diff_key]["history"]) > 5:
            self.scores[diff_key]["history"] = self.scores[diff_key]["history"][-5:]

        # 2. RECORD (Best)
        if "(WIN)" in name.upper():
            current_best = self.scores[diff_key]["best"]
            if current_best is None or time_value < current_best["time"]:
                self.scores[diff_key]["best"] = {
                    "name": name.replace("(WIN)", "").strip().upper(), 
                    "time": time_value
                }

        self.save_scores()