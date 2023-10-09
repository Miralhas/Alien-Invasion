import pygame.font

class Button:
    '''Classe para construir botões.'''

    def __init__(self, ai_game, msg):
        '''Inicializa os atributos do botão.'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Seta as dimensões e propriedades do botão.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Constroi o retângulo do botão e centraliza ele.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # A mensagem do botão precisa ser preparada apenas uma vez.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        # Transforma a msg em uma img renderizada e centraliza o txt no botão.
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        '''Desenha o botão e depois desenha a mensagem.'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)