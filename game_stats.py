class GameStats:    # Clase para hacer el seguimiento de las estadísticas
    """Sigue las estadísticas de Alien Invasion"""

    def __init__(self, ai_game):
        """Inicializa las estadísticas"""
        self.settings = ai_game.settings
        self.reset_stats()  # llamamo al método reset_stats() desde __init__() para que las estadísticas se configuren correctamente cuando se cree la instancia de GameStats. También se podrá llamar a reset_stats() cada vez que el jugador empiece una partida
        # Inicia Alien Invasion en estado inactivo
        self.game_active = False

        # La puntuación más alta no debería de restablecerse nunca
        self.high_score = 0


    def reset_stats(self):
        """Inicializa las estadísiticas que pueden cambiar durante el juego"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        
