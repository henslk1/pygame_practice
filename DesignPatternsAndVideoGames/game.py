import os
import pygame
from pygame import Rect
from pygame.math import Vector2

os.environ['SDL_VIDEO_CENTERED'] = '1'


class GameState():
    """Handles the game state"""

    def __init__(self):
        """Initialize attributes"""

        self.world_size = Vector2(16,10)
        self.tank_pos = Vector2(0,0)


    def update(self, move_tank_command):
        """Update coords"""

        self.tank_pos += move_tank_command
        
        if self.tank_pos.x < 0:

            self.tank_pos.x = 0
        
        elif self.tank_pos.x >= self.world_size.x:

            self.tank_pos.x = self.world_size.x - 1

        if self.tank_pos.y < 0:

            self.tank_pos.y = 0

        elif self.tank_pos.y >= self.world_size.y:
            
            self.tank_pos.y = self.world_size.y - 1


class UserInterface():

    def __init__(self):
        """Initialize UserInterface attributes."""

        pygame.init()

        self.game_state = GameState()

        self.cell_size = Vector2(64, 64)
        self.units_texture = pygame.image.load("units.png")

        window_size = self.game_state.world_size.elementwise() * self.cell_size
        self.window = pygame.display.set_mode((int(window_size.x), int(window_size.y)))
        pygame.display.set_caption("Discover Python & Patterns")
        pygame.display.set_icon(pygame.image.load("icon.png"))

        self.move_tank_command = Vector2(0,0)

        self.clock = pygame.time.Clock()

        self.running = True


    def process_input(self):
        """Handles player input."""

        self.move_tank_command = Vector2(0,0)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False
                break

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.running = False
                    break

                elif event.key == pygame.K_RIGHT:

                    self.move_tank_command.x = 1

                elif event.key == pygame.K_LEFT:

                    self.move_tank_command.x = -1

                elif event.key == pygame.K_DOWN:

                    self.move_tank_command.y = 1

                elif event.key == pygame.K_UP:
                    
                    self.move_tank_command.y = -1
            

    def update(self):
        """Update game state"""
        
        self.game_state.update(self.move_tank_command)


    def render(self):
        """Displays current game state"""

        self.window.fill((0,0,0))

        #tank base
        sprite_point = self.game_state.tank_pos.elementwise() * self.cell_size
        texture_point = Vector2(1,0).elementwise() * self.cell_size
        texture_rect = Rect(int(texture_point.x), int(texture_point.y), 
                            int(self.cell_size.x),int(self.cell_size.y))
        self.window.blit(self.units_texture, sprite_point, texture_rect)

        pygame.display.update()


    def run(self):
        """Main game loop"""
        
        while self.running:

            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)

    
user_interface = UserInterface()
user_interface.run()

pygame.quit()
