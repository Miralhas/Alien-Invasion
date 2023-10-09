import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Classe para gerenciar a nave.'''

    def __init__(self, ai_game):
        '''Inicializa a nave e define sua posição inicial.'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Carrega a imagem da nave e seu retângulo
        self.image = pygame.image.load('images/niceship.png')
        self.rect = self.image.get_rect()

        # Inicia cada nova Nave no centro inferior da tela.
        self.rect.midbottom = self.screen_rect.midbottom

        # Armazenar um float para a posição exata horizontal da nave.
        self.x = float(self.rect.x)

        # Flag de Movimento; Começa com uma nave que não está se movendo.
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Atualiza a posição da nave baseado na Flag de Movimento'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x
    
    def blitme(self):
        '''Desenha a Nave na localização atual.'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Centraliza a nave na tela.'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)