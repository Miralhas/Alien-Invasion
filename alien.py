import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Classe que representa um único alien na frota.'''

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Da load na imagem e gera o seu retângulo. 
        self.image = pygame.image.load('images/fireship.png')
        self.rect = self.image.get_rect()

        # Spawna cada alien novo perto da posição superior esquerda da tela.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.width

        # Armazena a posição horizontal exata do Alien.
        self.x = float(self.rect.x)

    def check_edges(self):
        '''Retorna True se o alien estiver na borda da tela.'''
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        '''Move o alien para a direita.'''
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

