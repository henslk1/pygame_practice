from pygame.math import Vector2


class GameState():
    """Handles the game state"""

    def __init__(self):
        """Initialize attributes"""

        self.world_size = Vector2(16,10)
        self.tank_pos = Vector2(5,4)
        self.towers_pos = [
            Vector2(10,3),
            Vector2(10,5)
            ]


    def update(self, move_tank_command):
        """Update coords"""

        new_tank_pos = self.tank_pos + move_tank_command
        
        if new_tank_pos.x < 0 or new_tank_pos.x >= self.world_size.x \
        or new_tank_pos.y < 0 or new_tank_pos.y >= self.world_size.y:
            
            return
        
        for position in self.towers_pos:

            if new_tank_pos == position:

                return
            
        self.tank_pos = new_tank_pos
