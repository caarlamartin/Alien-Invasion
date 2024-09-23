import pygame
from pygame.sprite import Sprite

# cuando usamos sprite podemos agrupar los elementos relacionados del juego para actuar a la vez en todos ellos

class Bullet(Sprite):
    """Una clase para gestionar las balas disparadas desde la nave"""
    
    def __init__(self, ai_game):
        """Crea un objeto para la bala en la posición actual de la nave."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Crea un rectángulo para la bala en (0, 0) y luego establece la posición correcta 
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)  # creamos el atributo rect de la bala. la bala no se basa en una imagen, asi que creamos un rectangulo desde cero con la clase pygame.Rect()
        self.rect.midtop = ai_game.ship.rect.midtop # establecemos el atributo midtop para que coincida con el atributo midtop de la nave. así parece que la bala sale de la parte superior de la nave

        # Guarda la posición de la bala como valor decimal
        self.y = float(self.rect.y) # guardamos un valor decimal para la coordenada y de la bala para poder ajustar mejor su velocidad

    def update(self):   #este método administra la posición de la bala. cuando se dispara una se mueve hacia arriba por la pantalla (un valor decreciente en la coordenada y)
        """Mueve la bala hacia arriba por la pantalla"""
        # Actualiza la posición decimal de la bala
        self.y -= self.settings.bullet_speed    
        # Actualiza la posición del rectángulo
        self.rect.y = self.y

    def draw_bullet(self):  # método para dibujar la bala 
        """Dibuja la bala en la pantalla"""
        pygame.draw.rect(self.screen, self.color, self.rect)    # la función draw.rect() rellena la parte de la pantalla definida por el rect de la bala con el color almacenada en self.color
