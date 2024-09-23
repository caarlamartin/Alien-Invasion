#CREAR UNA CLASE SETTINGS
#para modificar el juego solo tendremos que cambiar algunos valores en settings.py en vez de buscar distintas configuraciones por todo el proyecto

class Settings:
    """Una clase para guardar toda la configuración de Alien Invasion"""

    def __init__(self):
        """Inicializa la configuracion estática del juego."""

        #Configuracion de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #Configuración de la nave
        self.ship_speed = 1.5 #píxeles
        self.ship_limit = 3 # estadísticas

        # Configuración de las balas
        self.bullet_speed = 1.5 # velocidad de las balas
        self.bullet_width = 3   # anchura de 3 píxeles
        self.bullet_height = 15 # altura de 15 píxeles
        self.bullet_color = (60, 60, 60) # color gris
        self.bullets_allowed = 3    # esto limita al jugador a tres balas cada vez

        # Configuraciones del alien
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        #Rapidez con la que se acelere el juego
        self.speedup_scale = 1.1    # el valor 2 duplica la velocidad cada vez que el jugador pase de nivel

        # Lo rápido que aumenta el valor en puntos de los aliens
        self.score_scale = 1.5

        self.initialize_dynamic_settings()  # inicializar los valores para los atributos que tengan que cambiar durante el juego

    def initialize_dynamic_settings(self):
        """Inicializa las configuraciones que cambian durante el juego."""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction de 1 representa derecha; -1 representa izquierda
        self.fleet_direction = 1

        # Puntuación
        self.alien_points = 50  # puntos que se consiguen tras disparar a un alien

    def increase_speed(self):
        """Incrementa las configuraciones de velocidad y los valores en puntos de los aliens"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)   # el nuevo valor debe aparecer en el terminal cada vez que pase de nivel
