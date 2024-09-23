#Crear la clase Ship
import pygame
from pygame.sprite import Sprite

class Ship(Sprite): # aseguramos que Ship hereda de Sprite
    """Una clase para gestionar la nave."""

    def __init__(self, ai_game):
        """Inicializa la nave y establece su posición inicial."""
        super().__init__()  # llamamos a super() al princio de __init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings    #crea un atributo settings para Ship para poder usarlo en update()
        self.screen_rect = ai_game.screen.get_rect()

        #Carga la imagen de la nave y obtiene su rect.
        self.image = pygame.image.load('PROYECTO_1_ALIEN_INVASION/images/ship.bmp')
        self.rect = self.image.get_rect()

        #Coloca inicialmente cada nave nueva en el centro de la parte inferior de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom

        # Guarda un valor decimal para la posición horizontal de la nave
        self.x = float(self.rect.x) #definimos un nuevo atributo self.x que pueda albergar valores decimales usando la función float()

        #Bandera de movimiento
        self.moving_right = False   # añadimos un atributo al método __init__() configurado como False
        self.moving_left = False

    def update(self):   #método que mueve la nave hacia la derecha si la bandera es True // no es un método auxiliar porque lo llamamos mediante una instancia de Ship
        """Actualiza la posición de la nave en función de la bandera de movimiento"""
        #Actualiza el valor de x de la nave, no el rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  #no ha llegado al borde derecho
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed  #no ha llegado al borde izquierdo
        
        # Actualiza el objeto rect de self.x
        self.rect.x = self.x

    def blitme(self):   #un método que dibuja la imagen en la pantalla en la posicion especifica por self.rect
        """Dibuja la nave en su ubicación actual."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):  # centramos la nave y restablecemos el atributo self.x, que nos permite determinar la posicion exacta de la nave
        """Centra la nave en la pantalla"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)