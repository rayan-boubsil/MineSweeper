import os
import json

class ProfileManager:
    def __init__(self, manager ,profile_dir="profiles"):
        self.manager = manager
        self.profile_dir = profile_dir
        if not os.path.exists(self.profile_dir):
            os.makedirs(self.profile_dir)

    def create(self, name):
        """Crée un nouveau profil (fichier vide ou avec stats de base)."""
        file_path = os.path.join(self.profile_dir, f"{name}.json")
        if not os.path.exists(file_path):
            data = {"name": name, "games_played": 0, "total_wins": 0}
            with open(file_path, "w") as f:
                json.dump(data, f)
            print(f"Profil créé : {name}")
            return True
        return False

    def get_list(self):
        """Récupère la liste des noms de profils sans l'extension .json."""
        if not os.path.exists(self.profile_dir):
            return []
        return [f.replace(".json", "") for f in os.listdir(self.profile_dir) if f.endswith(".json")]

    def delete(self, name):
        """Supprime le profil et potentiellement sa sauvegarde associée."""
        profile_path = os.path.join(self.profile_dir, f"{name}.json")
        if os.path.exists(profile_path):
            os.remove(profile_path)
            return True
        return False