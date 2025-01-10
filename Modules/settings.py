#global settings
from colors import Colors
from pygame.locals import *


class Settings():
    """Settings for the matching game."""

    def __init__(self, matching_game, logger):
        """Settings attributes."""
        self.colors = Colors(self)

        # main settings
        self.fps = 30 #FPS rate
        self.window_width = 640
        self.window_height = 480

        #board settings
        self.reveal_speed = 8 #speed boxes' sliding reveals and covers
        self.box_size = 40 # height and width
        self.gap_size = 10 # gap between boxes
        self.board_width = 10 # columns
        self.board_height = 7 # rows
        
        #board colors
        self.bg_color = self.colors.navy_blue
        self.light_bg_color = self.colors.gray
        self.box_color = self.colors.white
        self.highlight_color = self.colors.blue
