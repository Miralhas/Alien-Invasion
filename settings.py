class Settings:
    '''Classe para armazenar todas as Settings do Jogo'''

    def __init__(self):
        '''Inicializa as settings estáticas do jogo'''
        # Screen Settings.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (16, 27, 55) #(85, 85, 85)

        # Ship Settings
        self.ship_limit = 2

        # Bullet Settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (46, 147, 56)
        self.bullets_allowed = 3

        # Alien Settings
        self.fleet_drop_speed = 10

        # O quão rapidamente o jogo se acelera.
        self.speedup_scale = 1.1

        # O quão rapidamente o valor de cada alien aumenta.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Inicializa as settings que vão mudando conforme o jogo avança.'''
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction = 1 repesenta direita; -1 representa esquerda.
        self.fleet_direction = 1

        # Scoring Settings
        self.alien_points = 50
    
    def increase_speed(self):
        '''Aumenta as settings de velocidade e pontuação.'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)



