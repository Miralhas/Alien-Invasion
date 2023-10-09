import pygame

from pygame.sprite import Sprite

class Bullet(Sprite):
    '''Classe para administrar disparos feito pela nave.'''

    def __init__(self, ai_game):
        '''Cria o objeto disparado pela nave em sua posição atual.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Cria o retângulo do disparo em (0, 0) e dps seta para posição correta.
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = ai_game.ship.rect.midtop

        # Armazena a posição do disparo como float
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet up the screen.'''
        # Atualiza a posição exata do retângulo disparado.
        self.y -= self.settings.bullet_speed
        # Atualiza da posição do retângulo disparado
        self.rect.y = self.y

    def draw_bullet(self):
        '''Desenha o disparo na tela.'''
        pygame.draw.rect(self.screen, self.color, self.rect)