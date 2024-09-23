import sys  #herramientas para salir del juego cuando el jugador quiera
from time import sleep  # para poder poner el juego en pausa un momento cuando la nave es alcanzada

import pygame   #contiene la funcionalidad que necesitamos para hacer un juego

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:    #crear una clase llamada AlienInvasion
    """Clase general para gestionar los recursos y el comportamiento del juego."""

    def __init__(self):
        """Inicializa el juego y crea recursos."""
        pygame.init()   #inicializa la configuración de fondo que necesita Pygame para funcionar bien
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # esto dice que use un tamaño de ventana que rellene toda la pantalla // asignamos esta ventana al atributo self.screen para que esté disponible en todos los métodos de la clase
        # como no sabemos el alto y el ancho de la pantalla de antemano, actualizamos estas configuraciones después de crear la pantalla 
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasión")

        # Crea una instancia para guardar estadísticas del juego y crea un marcador.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)  #instancia despúes de crear la pantalla
        self.bullets = pygame.sprite.Group()    # creamos el grupo
        self.aliens = pygame.sprite.Group()     # creamos un grupo para la alojar la flota de aliens 

        self._create_fleet()

        # Hace el boton Play
        self.play_button = Button(self, "Play") # instancia de Button con la etiqueta Play, pero no dibuja el boton

    def run_game(self): #método run_game() controla el juego
        """Inicia el bucle principal para el juego."""
        while True: #bucle while: contine un bucle de eventos y código para administrar las actualizaciones de la pantalla. un "evento" es una acción que realiza el usuario mientras juega
            # a continuación llamamos a los métodos
            self._check_events()    #ponemos el "." para llamar a un método desde dentro de una clase

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()

    def _update_screen(self):
            """Actualiza las imágenes en la pantalla y cambia a la pantalla nueva"""
            #Redibuja la pantalla en cada paso por el bucle
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():   # el método bullets.sprites() devuelve una lista de todos los sprites del grupo bullets. Para dibujar todas las balas disparadas en la pantalla, pasamos en bucle por los sprites de bullets  y llamamos a draw_bullet() en cada uno
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            # Dibuja la información de la puntuación
            self.sb.show_score()

            #Dibuja el boton para jugar si el juego esta inactivo
            if not self.stats.game_active:
                 self.play_button.draw_button()

            # Hace visibilidad la última pantalla dibujada.
            pygame.display.flip()   #actualiza constantemente la pantalla para mostrar las nuevas posiciones de esos elementos y ocultar las viejas, creando un ailusión de movimiento suave.
    
    def _update_bullets(self):
         """Actualiza la posicion de las balas y deshace las viejas"""
         #Actualiza las posiciones de las balas
         self.bullets.update()   # así el grupo llama automáticamente a update() para cada uno de sus sprites // llama a bullet.update() para cada bala colocda en el grupo bullets
            
        # se deshace de las balas que han desaparecido 
         for bullet in self.bullets.copy():  # usamos el método sopy() para configurar el bucle for, lo que permite modificar las balas dentro del bucle
             if bullet.rect.bottom <= 0:    # comprobamos cada bala para ver si ha desaparecido por encima de la pantalla
                  self.bullets.remove(bullet)   # la quitamos de bullets  
         
         self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):     
         """Responde a las colisiones bala-alien"""
         # Si chocan, se deshace de la bala y del alien
         collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)   

         if collisions:  # actualizamos la puntuación cada vez que se abata un alien
               for aliens in collisions.values(): 
                    self.stats.score += self.settings.alien_points * len(aliens)     # nos aseguramos de que puntuamos todos los aciertos
               self.sb.prep_score()
               self.sb.check_high_score()

         if not self.aliens:    # comprobamos si el grupo de aliens está vacío, evaluado como False si es así
              # Destruye las balas existentes y crea una flota nueva
              self.bullets.empty()  # deshaciendonos de cualquier bala existente con empty(), que elimina todos los sprites que quedan en un grupo
              self._create_fleet()  # vuelve a llenar la pantalla de marcianitos
              self.settings.increase_speed()

              # Aumenta el nivel
              self.stats.level += 1     # si se destruye una flota, incrementamos el valor de stats.level 
              self.sb.prep_level() # llamamos a prep_level para asegurarnos de que el nuevo nivel se muestra correctamente

    def _ship_hit(self):
         """Responde al impacto de un alien en la nave"""
         if self.stats.ships_left > 0:  # el jugador tiene al menos una nave
            #Disminuye ships_left y actualiza el marcador
            self.stats.ships_left = -1 # el número de naves que se quedan se reducen en 1
            self.sb.prep_ships()   # se llama a prep_ships() tras reducir el valor de ships_left para que se muestra el número correcto de naves cada vez que se destruya una

            #Se deshace de los aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa
            sleep(0.5)
         else:
              self.stats.game_active = False
              pygame.mouse.set_visible(True)    # el cursor reaparece

    def _check_aliens_bottom(self):     #pausar el juego cuando un alien llegue a la parte inferior de la pantalla
         """Comprueba si algún alien ha llegado al fondo de la pantalla"""
         screen_rect = self.screen.get_rect()
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                   # Trata esto como si la nave hubiese sido alcanzada
                   self._ship_hit()
                   break

    def _update_aliens(self):
         """
         Comprueba si la flota está en un borde,
         después actualiza las posiciones de todos los aliens de la flota
         """
         self._check_fleet_edges()
         self.aliens.update()

         # Busca colisiones alien-nave
         if pygame.sprite.spritecollideany(self.ship, self.aliens): #si no hay colisiones, spritecollideany() devuelve None y no se ejecuta el bloque
              self._ship_hit()

         # Busca aliens llegando al fondo de la pantalla
         self._check_aliens_bottom()

    def _check_events(self):    #método donde está el código que comprueba que el jugador ha hecho clic para cerrar la ventana
            """Responde a pulsaciones de teclas y eventos de ratón"""    
            #Busca eventos de teclado y ratón.
            for event in pygame.event.get():    #bucle de eventos
                if event.type == pygame.QUIT:   #para acceder a los eventos detectados por Pygame. devuelve una lista de los eventos que se han producido desde la última vez que se llamó 
                    sys.exit()  #cuando se haga clic para cerrar la ventana, se detecta un evento pygame.QUIT y llamamos a sys.exit() para salir
                elif event.type == pygame.KEYDOWN:  #para detectar a los eventos del tipo KEYDOWN
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:    # bloque que responde a eventos KEYUP // cuando el jugador suelte la tecla (K_RIGHT), configuramos moving_right en False
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:  # se detecta un evento de MOUSEBUTTONDOWN cuando se hace clic en alguna parte de la pantalla, para se quiere restringir en el boton Play
                     mouse_pos = pygame.mouse.get_pos() # devuelve una tupla que contiene las coordenadas x e y del cursor cuando hace clic
                     self._check_play_button(mouse_pos) # estos valores se envian al método _check_play_button()

    def _check_play_button(self, mouse_pos):
         """Inicia un juego nuevo cuando el jugador hace clic en Play"""
         button_clicked = self.play_button.rect.collidepoint(mouse_pos) # button_clicked tiene el valor de True o False // collidepoint() comprueba si el punto dl clic del raton se solapa con la region del boton Play
         if button_clicked and not self.stats.game_active:  # se reinicia solo si se hace clic en Play y el juego está inactivo actualmente
              
              # Restablece las configuraciones del juego
              self.settings.initialize_dynamic_settings()
              
              # Restablece las estadísticas del juego
              self.stats.reset_stats() 
              self.stats.game_active = True
              self.sb.prep_score() # esto prepara el marcador a 0 cada vez que se empiece una partida nueva
              self.sb.prep_level() # asegurarnos que la imagen del nivel se actualiza bien al principio de una partida nueva
              self.sb.prep_ships() # cuando se da a una nave para actualizar la muestra de las imágenes cuando el jugador pierde una vida

              # Se deshace de los aliens y las balas que quedan
              self.aliens.empty()
              self.bullets.empty()

              # Crea una flota nueva y centra la nave
              self._create_fleet()
              self.ship.center_ship()

              # Ocultar el cursor del ratón
              pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event): # método auxiliar
            """Responde a pulsaciones de teclas"""
            if event.key == pygame.K_RIGHT:    # comprobar que la tecla que se ha pulsado es la tecla derecha (pygame.K_RIGHT)
                self.ship.moving_right = True   # en lugar de cambiar directamente la posición de la nave, establecemos moving_right True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = True
            elif event.key == pygame.K_q:   # al pulsar Q, termina el juego
                 sys.exit()
            elif event.key == pygame.K_SPACE:
                 self._fire_bullet()    # llamamos a _fire_bullet() cuando se pulsa la barra espaciadora

    def _check_keyup_events(self, event):   # método auxiliar
            """Responde a liberaciones de teclas"""
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False
                    
    def _fire_bullet(self):
        """Crea una bala nueva y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:   # para comprobar cuantas balas hay antes de crear una nueva
            new_bullet = Bullet(self)  # hacemos un instancia de Bullet y la llamamos new_bullet
            self.bullets.add(new_bullet)   # la añadimos al grupo bullets con la función add()         
                     
    def _create_fleet(self):
         """Crea la flota de aliens."""
         # Crea un alien y halla el número de aliens en una fila
         # El espacio entre aliens es igual a la anchura de un alien
         alien = Alien(self)
         alien_width, alien_height = alien.rect.size # usamos el atributo size, que contiene una tupla con la anchura y la altura de un objeto rect
         available_space_x = self.settings.screen_width - (2 * alien_width)    # obtenemos la anchura del alien de su atributo rect y guardamos el valor alien_width
         number_aliens_x = available_space_x // (2 * alien_width)   # calculamos el espacio horizontal disponible para los aliens y el número de marcianitos que cabe en este espacio
         
         # Determina el número de filas de aliens que caben en la pantalla
         ship_height = self.ship.rect.height
         available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)   #calculo de filas que caben 
         number_rows = available_space_y // (2 * alien_height)

         # Crea la flota de aliens
         for row_number in range(number_rows):  # usamos un bucle exterior, que cuenta desde 0 hasta el número de filas que queramos, y otro interior, que crea los aliens de una fila
            for alien_number in range(number_aliens_x):    # bucle que cuente desde 0 hasta el número de aliens que tenemos que hacer
              self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
              """Crea un alien y lo coloca en la fila"""
              alien = Alien(self)
              alien_width, alien_height = alien.rect.size
              alien_width = alien.rect.width
              alien.x = alien_width + 2 * alien_width * alien_number
              alien.rect.x = alien.x
              alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number # cambiamos el valor de la coordenada y cuando no está en la primera fila 
              self.aliens.add(alien)    #creamos un nuevo alien y establecemos el valor de su coordenada x para colocarlo en la fila

    def _check_fleet_edges(self):
         """Responde adecuadamente si algún alien ha llegado a un borde"""
         for alien in self.aliens.sprites():    # llamamos a _check_edges() en cada alien
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
              
    def _change_fleet_direction(self):
         """Baja toda la flota y cambia su dirección"""
         for alien in self.aliens.sprites():
              alien.rect.y += self.settings.fleet_drop_speed    #pasamos en bucle por todos los aliens y los bajamos con la configuracion fleet_drop_speed
         self.settings.fleet_direction *= -1

if __name__ == '__main__':
    #Hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game()



