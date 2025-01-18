class Unit():
    """Handle units for the tank game"""

    def __init__(self, state, position, tile):
        """Initialize attributes."""

        self.state = state
        self.position = position
        self.tile = tile

    
    def move(self, move_vector):

        raise NotImplementedError()
    

class Tank(Unit):
    """Tank objects"""

    def move(self, move_vector):
        """Compute new tank position"""

        new_tank_pos = self.position + move_vector

        # Don't allow positions outside the world

        if new_tank_pos.x < 0 or new_tank_pos.x >= self.state.world_size.x \
        or new_tank_pos.y < 0 or new_tank_pos.y >= self.state.world_size.y:
            
            return
        
        # Don't allow collisions
        for unit in self.state.units:

            if new_tank_pos == unit.position:

                return
            
        self.position = new_tank_pos


class Tower(Unit):
    """Tower object"""

    def move(self, move_vector):

        pass
    