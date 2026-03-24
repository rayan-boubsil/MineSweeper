import json
import os

class ScoreManager:
    """Gère l'enregistrement et le chargement des meilleurs scores en JSON."""
    def __init__(self, filename="scores.json"):
        self.filename = filename
        # On charge les scores dès l'initialisation
        self.scores = self.load_scores()

    def load_scores(self):
        """Charge les scores depuis le fichier ou renvoie des valeurs par défaut."""
        # 1. Si le fichier n'existe pas, on crée une liste de base
        if not os.path.exists(self.filename):
            return [
                {"name": "ALPHA", "time": "00:45"},
                {"name": "BETA",  "time": "01:10"},
                {"name": "GAMMA", "time": "02:00"}
            ]
        # 2. On essaie de lire le fichier JSON
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Si le fichier est illisible, on renvoie une liste vide
            return []

    def add_score(self, name, time_str):
        """Ajoute un score, trie la liste et garde le top 10."""
        new_entry = {
            "name": name.upper()[:10], # On limite à 10 caractères pour l'affichage
            "time": time_str
        }
        self.scores.append(new_entry)
        # Tri alphabétique du temps (ex: "00:30" avant "01:10")
        self.scores.sort(key=lambda x: x['time'])
        # On ne garde que les 10 meilleurs
        self.scores = self.scores[:10]
        # On sauvegarde immédiatement sur le disque
        self.save_all()

    def save_all(self):
        """Enregistre la liste actuelle dans le fichier JSON."""
        try:
            with open(self.filename, "w") as f:
                json.dump(self.scores, f, indent=4)
        except IOError as e:
            print(f"Erreur d'écriture du score : {e}")