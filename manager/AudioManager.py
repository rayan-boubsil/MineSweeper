import pygame

class AudioManager:
    """Gère la musique et les sons du jeu."""
    def __init__(self):
        # Initialisation du moteur de son de Pygame
        pygame.mixer.init()
        # Dictionnaire pour stocker les sons chargés
        self.sfx = {}
        # Réglages par défaut du volume (0.0 à 1.0)
        self.music_volume = 0.4
        self.sfx_volume = 0.6
        # --- Chargement automatique des sons ---
        # Assure-toi que ces fichiers existent dans ton dossier 'assets'
        self.load_sfx("click", "assets/click.wav")
        self.load_sfx("win", "assets/win.wav")
        self.load_sfx("explosion", "assets/explosion.wav")

    def load_sfx(self, name, path):
        """Tente de charger un son. Si le fichier manque, le jeu ne crash pas."""
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sfx_volume)
            self.sfx[name] = sound
        except Exception:
            # Si le fichier n'est pas trouvé, on affiche un message simple
            print(f"⚠️ Son manquant : {path}")

    def play_sfx(self, name):
        """Joue un son court (ex: play_sfx('click'))."""
        if name in self.sfx:
            self.sfx[name].play()

    def start_music(self, path):
        """Lance une musique de fond en boucle infinie."""
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1) # -1 signifie 'en boucle'
        except Exception:
            print(f"⚠️ Musique manquante : {path}")

    def stop_music(self):
        """Arrête la musique proprement."""
        pygame.mixer.music.stop()