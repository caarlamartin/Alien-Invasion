import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """Una clase para dar informacion de la puntuación."""

    def __init__(self, ai_game):
        """Inicializa los atributos de la puntuación"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Configuración de fuente para la información de la puntuación
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepara la imagen de la puntuación inicial
        self.prep_score()
        self.prep_high_score()  # la imagen de la puntuación más alta va separada del marcador, asi que necestamos un nuevo método, prep_high_score()
        self.prep_level()   # Para mostrar el nive actual
        self.prep_ships()

    def prep_score(self):
        """Convierte la puntuación en una imagen renderizada"""
        rounded_score = round(self.stats.score, -1) # Redondea el valor de stats.score a la decena más cercana y lo guarda en rounded_score
        score_str = "{:,}".format(rounded_score)    # inserta comas en los números cuando convierta un valor númerico en cadena
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)   # Se la pasamos a render() y la convierte en una imagen

        # Muestra la puntuación en la parte superior derecha de la pantalla
        self.score_rect = self.score_image.get_rect()   # Creamos un rect llamado score_rect
        self.score_rect.right = self.screen_rect.right - 20 # Configuramos su borde derecho a 0 píxeles del borde derecho de la pantalla
        self.score_rect.top = 20    # ponemos el borde superior 20 píxeles por debajo del borde superior de la pantalla

    def show_score(self):   # El método dibuja la imagen de la puntuación en la pantalla, en la ubicación que especifica score_rects
        """Dibuja la puntuación, nivel y naves en la pantalla"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)   # dibuja la puntuación actual en la esquina superior derecha y la más alta en el centro superior de la pantalla
        self.screen.blit(self.level_image, self.level_rect) # dibuja la imagen del nivel en la pantalla
        self.ships.draw(self.screen)    # mostrar las naves en pantalla

    def prep_high_score(self):
        """"Convierte la puntuación más alta en una imagen renderizada"""
        high_score = round(self.stats.high_score, -1)   # redondeamos la puntuación más alta al 10 más cernado y le aplicamos formato con comas
        high_score_str = "{:,}".format(high_score)  # generamos una imagen de esa puntuación
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color) 

        # Centra la puntuación más alta en la parte superior de la pantalla
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx # centramos su rect horizontalmente
        self.high_score_rect.top = self.score_rect.top  # configuramos su atributo top para que coincida con el de la imagen del marcador

    def check_high_score(self):
        """"Comprueba si hay una nueva puntuación más alta"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Convierte el nivel en una imagen renderizada."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)   # prep_level() crea una imagen a partir del valor guardado en stats.level() 

        # Coloca el nivel debajo de la puntuación
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right   # configura el atributo right de la imagen para que coincida con el atributo right de la puntuación
        self.level_rect.top = self.score_rect.bottom + 10   # establece 10 píxeles por debajo del borde inferior de la imagen de la puntuación para dejar espacio entre el marcador y el nivel

    def prep_ships(self):
        """Muestra cuántas naves quedan."""
        self.ships = Group()    # crea un grupo vacío para acoger las instancias de la nave
        for ship_number in range(self.stats.ships_left):    # para rellenar el grupo cada vez por cada nave que le queda
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width    # establecer el valor de la coordenada x de cada nave para que aparezcan unas junto a otras con un marfen de 10 píxeles
            ship.rect.y = 10    # a 10 píxeles de la parte superior de la pantalla para que las naves aparezcan en la esquina superior izquierda
            self.ships.add(ship)    # añadimos naves de una en una al grupo
