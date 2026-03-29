import pickle
import os

class SaveManager:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        # Créer le dossier 'saves' s'il n'existe pas
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def get_save_path(self, player_name):
        """Génère un chemin de fichier propre : saves/NomDuJoueur.dat"""
        # On s'assure que le nom est valide pour un nom de fichier
        filename = f"{player_name.strip()}.dat"
        return os.path.join(self.save_dir, filename)

    def save_game(self, data, player_name):
        """Sauvegarde les données pour un joueur spécifique."""
        if not player_name: return
        
        path = self.get_save_path(player_name)
        try:
            with open(path, "wb") as f:
                pickle.dump(data, f)
            print(f"Jeu sauvegardé pour {player_name}")
        except Exception as e:
            print(f"Erreur de sauvegarde : {e}")

    def load_game(self, player_name):
        """Charge la sauvegarde d'un joueur s'il en a une."""
        path = self.get_save_path(player_name)
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Erreur de chargement : {e}")
        return None

    def delete_save(self, player_name):
        """Supprime la sauvegarde quand la partie est finie (victoire/défaite)."""
        path = self.get_save_path(player_name)
        if os.path.exists(path):
            os.remove(path)
            print(f"Sauvegarde supprimée pour {player_name}")

    def has_save(self, player_name):
        """Vérifie si le joueur a une partie en cours."""
        return os.path.exists(self.get_save_path(player_name))