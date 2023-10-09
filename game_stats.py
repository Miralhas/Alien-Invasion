class GameStats:
    '''Armazena estatísticas.'''

    def __init__(self, ai_game):
        '''Incializa as estatísticas.'''
        self.ai_settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        '''Incializa as estatísticas que podem ser mudadas durante o jogo.'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1