''' 
No jogo Alien Invasion, o player controla uma nave que aparece no centro inferior da tela. 
O player pode mover a nave para esquerda e direita utilizando as setas (<>) e atirar misseis apertando a barra de espaço.
Quando o jogo começa, uma frota de aliens preenche o céu e se move através e abaixo da tela.
O player atira e destrói os aliens. Caso o player destrua todos os aliens, a fase acaba, e uma nova frota mais rápida que a anterior aparecerá.
Caso algum alien atinja o player, ou chegue até o fim da tela, o jogador perde uma nave. Caso o player perca três naves, o jogo acaba.
'''
import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''Classe geral para administrar os assets e comportamentos do game.'''

    def __init__(self):
        '''Inicializa o game e cria os recursos do própio.'''
        pygame.init()
        self.settings = Settings()

        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))

        # Definir o título da janela do pygame.
        pygame.display.set_caption("Alien Invasion")

        # Cria uma instância para armazenar estatísticas do jogo.
        #   e cria uma scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Cria uma instância da nave.
        self.ship = Ship(self)

        # Cria uma instância do disparo e armazena ela no (Group). 
        self.bullets = pygame.sprite.Group()

        # Cria uma instância do Alien e armazena ela no (Group).
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Inicia o jogo em um estado inativo.
        self.game_active = False

        # Faz o botão de Play.
        self.play_button = Button(self, 'Play')

    def run_game(self):
        '''Método que inicia o loop principal do jogo'''
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            
            # Quadros por Segundo (FPS)
            self.clock.tick(144)
            
    def _check_events(self):
        '''Obter todos os eventos de entrada.(Ações do usuário Mouse/Teclado)'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Quando o Usuário estiver segurando uma tecla < >
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)    

            # Quando o Usuário soltar a tecla que estava segurando.
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            # Quando o usuário clicar no botão de Play.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        '''Responde a apertos do teclado'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True   
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._check_play_button(self.screen.get_rect().center)
        elif event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_play_button(self, mouse_pos):
        '''Inicia um novo jogo quando o usuário clica Play.'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self._start_game()
    
    def _start_game(self):
        '''Faz os ajustes necessários quando um novo jogo é iniciado.'''
        # Reseta as estatísticas e inicia o Jogo.
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()
        self.settings.initialize_dynamic_settings()
        self.game_active = True

        # Deleta qualquer disparo e alien restante.
        self.bullets.empty()
        self.aliens.empty()

        # Cria uma nova frota de aliens e centraliza a nave.
        self._create_fleet()
        self.ship.center_ship()

        # Esconde o cursor do mouse.
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        '''Cria um novo disparo e adiciona para o grupo de disparos'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        '''Atualiza a posição e deleta os disparos que já sairam da tela.'''

        # Atualiza a posição do disparo.
        self.bullets.update()
        
        # Deleta os disparos que já saíram da tela.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            # print(len(self.bullets))
        
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''Responde a colisões entre disparos e aliens.'''

        # Remove qualquer disparo e alien que tenham colidido.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.prep_high_score()

        if not self.aliens:
            # Destroi os disparos existentes e cria uma nova nave.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
    
    def _check_aliens_bottom(self):
        '''Checa se algum alien alcançou a parte inferior da tela.'''
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Trata-se igual como se a nave fosse atingida.
                self._ship_hit()
    
    def _ship_hit(self):
        '''Responde à nave sendo atingida por um alien.'''
        if self.stats.ships_left > 0:
            # Diminui o número de naves restantes.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Deleta qualquer disparo ou alienígena restante.
            self.bullets.empty()
            self.aliens.empty()

            # Cria uma nova frota de alienígenas e centraliza a nave.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        '''Verifica se a nave está na borda e dps atualiza as posições.'''
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Procura por aliens atingindo a parte inferior da tela.
        self._check_aliens_bottom()

    def _update_screen(self):
        '''Atualiza as Imagens e flipa para a nova tela.'''
        self.screen.fill(self.settings.bg_color) # Background da tela.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme() # Chama a nave para a posição midbottom.

        self.aliens.draw(self.screen) # Faz o Alien aparecer na tela.

        self.sb.show_score() # Desenha o Score.
        
        if not self.game_active:
            self.play_button.draw_button() # Chama o Botão para a tela.

        pygame.display.flip() # atualiza a tela com as mudanças feitas acima.
    
    def _create_alien(self, x_position, y_position):
        '''Cria um Alien e adiciona na fila'''
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    
    def _check_fleet_edges(self): 
        '''Responde se algum alien ter alcançado a borda da tela'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        '''abaixa a nave do alien e muda sua posição'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        '''Cria a frota de Aliens'''
        # Faz um Alien e continua a adicionar mais até não ter mais espaço.
        # O espaço entre aliens é a largura de um alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 4 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            current_x = alien_width
            current_y += 2 * alien_height

if __name__ == "__main__":
    # Cria uma instância e roda o jogo.
    ai = AlienInvasion()
    ai.run_game()