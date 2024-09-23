import pygame.font  # permite mostrar texto en la pantalla

class Button:

    def __init__(self, ai_game, msg):   # msg contiene el texto del boton
        """Inicializa los atributos del botón"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Configura las dimensiones y propiedades del boton
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)   # preparamos un atributo font para mostrat texto. None indica a Pygame que use la fuente predeterminada, 48 es el tamaño del texto

        # Crea el objeto rect del boton y lo centra
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Solo hay que preparar el mensaje del boton una vez
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Convierte msg en una imagen redenrizada y centra el texto en el boton"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)    # font.render() convierte el texto almacenado en msg en una imagen, y lo almacena en self.msg_image
        self.msg_image_rect = self.msg_image.get_rect() #centra la imagen del texto en el boton creando un rect desde la imagen y configurando su atributo center 
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):  # para mostrar el boton en pantalla
        # Dibuja un boton en blanco y luego el mensaje
        self.screen.fill(self.button_color, self.rect)  #dibuja la parte rectangular del boton
        self.screen.blit(self.msg_image, self.msg_image_rect)   # dibuja la imagen del texto en la pantalla