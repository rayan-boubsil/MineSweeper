import pygame

class AudioManager:
    """Gestionnaire central de l'audio."""
    def __init__(self):
        pygame.mixer.init()
        self.sfx = {}
        self.music_volume = 0.4
        self.sfx_volume = 0.6

        # --- CHARGEMENT DES BRUITAGES (SFX) ---
        # Remplace les noms de fichiers par les tiens
        self.load_sfx("click", "assets/click.wav")
        self.load_sfx("win", "assets/win.wav")
        self.load_sfx("explosion", "assets/explosion.wav")

    def load_sfx(self, name, path):
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self.sfx_volume)
            self.sfx[name] = sound
        except:
            print(f"Erreur : Impossible de charger le son {path}")

    def play_sfx(self, name):
        """Joue un bruitage court (clic, mine, victoire)."""
        if name in self.sfx:
            self.sfx[name].play()

    def start_music(self, path):
        """Lance une musique en boucle."""
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1) # -1 pour la boucle infinie
        except:
            print(f"Erreur : Impossible de charger la musique {path}")

    def stop_music(self):
        pygame.mixer.music.stop()