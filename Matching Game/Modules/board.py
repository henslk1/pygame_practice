#board functions
from Modules.settings import Settings
from Modules.shapes import Shapes
from Modules.colors import Colors
import random


class Board():
    """Represents the board."""

    def __init__(self, mg):
        """Initiate attributes."""

        self.settings = Settings(self)
        self.colors = Colors(self)
        self.shapes = Shapes(self)

        self.define_board_margins()


    def define_board_margins(self):
        """Define x and y margin."""

        self.x_margin = int((self.settings.window_width - (self.settings.board_width
                             * (self.settings.box_size + self.settings.gap_size))) / 2)
        self.y_margin = int((self.settings.window_height - (self.settings.board_height
                             * (self.settings.box_size + self.settings.gap_size))) / 2)


    def get_randomized_board(self):
        
        self._generate_icons()

        return self._create_board_data_structure(self.icons)


    def _generate_icons(self):
        """Get a list of every posible shape and color."""

        self.icons = []

        for color in self.colors.all_colors:

            for shape in self.shapes.all_shapes:

                self.icons.append( (shape, color) )

        random.shuffle(self.icons) # randomize the order of the icons
        self.num_icons = int(self.settings.board_width * self.settings.board_height / 2)
        self.icons = self.icons[:self.num_icons] * 2 # makes 2 of each
        random.shuffle(self.icons)

        return self.icons


    def _create_board_data_structure(self, icons):
        """Create board structure with randomly placed icons."""

        self.new_board = []
        for x in range(self.settings.board_width):

            self.column = []
            
            for y in range(self.settings.board_height):

                self.column.append(icons[0])
                del icons[0] #remove icons as they're assigned
            
            self.new_board.append(self.column)
        
        return self.new_board
    