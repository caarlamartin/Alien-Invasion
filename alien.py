import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Una clase para representar un solo alien en la flota."""

    def __init__(self, ai_game):
        """Inicializa el alien y establece su posición inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Carga la imagen del alien y configura su atributo rect
        self.image = pygame.image.load('PROYECTO_1_ALIEN_INVASION/images/alien.bmp')
        self.rect = self.image.get_rect()

        # Inicia un nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width   # añadimos un espacio a la izquierda equivalente de su anchura
        self.rect.y = self.rect.height  # añadimos un espacio encima igual a su altura

        # Guarda la posición horizontal exacta del alien
        self.x = float(self.rect.x)

    def check_edges(self):  #método para ver si el alien está en el borde derecho o izquierdo
        """Devuelve True si el alien está en el borde de la pantalla"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0: # está en el derecho si el atributo right de su rect es mayor o igual que el atributo right del rect de la pantalla. está en la izquierda, si su valor left es menor o igual que 0
            return True

    def update(self):
        """Mueve el alien a la derecha o a la izquierda"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction) # permitir el movimiento hacia la derecha y a la izquierda multiplicando la velocidad del alien por el valor de fleet_direction 
        self.rect.x = self.x    # usando el valor self.x para actualizar la posicion del rect del alien