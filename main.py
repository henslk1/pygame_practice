import pygame, sys, random
from pygame.locals import *
from Modules.board import Board
from Modules.colors import Colors
from Modules.settings import Settings
from Modules.shapes import Shapes

class MatchingGame():
	"""Main game operations."""

	def __init__(self):
		"""Initiate attributes."""

		self.settings = Settings(self)
		self.board = Board(self)
		self.shapes = Shapes(self)
		self.colors = Colors(self)

		pygame.init()

		self.fps_clock = pygame.time.Clock()
		self.display_surf = pygame.display.set_mode((self.settings.window_width,
													self.settings.window_height))

		self.mousex = 0 #store x coord of mouse event
		self.mousey = 0 #store y coord of mouse event

		self.main_board = self.board.get_randomized_board()
		self.revealed_boxes = self._generate_revealed_boxes(False)

		self.first_selection = None #stores the (x,y) of first clicked box

		self.display_surf.fill(self.settings.bg_color)
		self._start_game_animation(self.main_board)

	def run_game(self):
		"""Start the main loop for the game."""
        
		while True:

			self.mouse_clicked = False
			self.display_surf.fill(self.settings.bg_color)

			self._draw_board(self.main_board, self.revealed_boxes)

			self._check_events()
			self._check_selection()

	def _check_events(self):
		"""Check for events"""

		for event in pygame.event.get(): #event handling loop
			if event.type == QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
				pygame.quit()
				sys.exit()
			
			elif event.type == MOUSEMOTION:
				self.mousex, self.mousey = event.pos

			elif event.type == MOUSEBUTTONUP:
				self.mousex, self.mousey = event.pos
				self.mouse_clicked = True

	def _check_selection(self):
		"""Respond to mouse hover and clicks."""

		self.boxx, self.boxy = self._get_box_at_pixel(self.mousex, self.mousey)

		if self.boxx != None and self.boxy != None:

			#The mouse is currently over a box
			if not self.revealed_boxes[self.boxx][self.boxy]:
				self._draw_highlight_box(self.boxx,self.boxy)

			if not self.revealed_boxes[self.boxx][self.boxy] and self.mouse_clicked:
				self._reveal_boxes_animation(self.main_board, [(self.boxx, self.boxy)])
				# Set the box as revealed
				self.revealed_boxes[self.boxx][self.boxy] = True

				if self.first_selection == None: # Current box is the first one clicked
					self.first_selection == (self.boxx, self.boxy)

				else: #the current box is the second box
					  #check if there was a match between the two icons
					self.icon1_shape, self.icon1_color = self.get_shape_and_color(
						self.main_board, self.first_selection[0], self.first_selection[1])
					
					self.icon2_shape, self.icon2_color = self.get_shape_and_color(
						self.main_board, self.boxx, self.boxy)
					
					if self.icon1_shape != self.icon2_shape or self.icon1_color != self.icon2_color:
						#Icons don't match
						pygame.time.wait(1000) #1 second
						self.cover_boxes_animation(self.main_board, [(
							self.first_selection[0], self.first_selection[1]), 
							(self.boxx, self.boxy)])
						
						self.revealed_boxes[self.first_selection[0]][self.first_selection[1]] = False
						self.revealed_boxes[self.boxx][self.boxy] = False
					
					#Check if all pairs found
					elif self._has_won(self.revealed_boxes):

						self._game_won_animation(self.main_board)
						pygame.time.wait(2000) #2 seconds

						#Reset the board
						self.main_board = self.board.get_randomized_board()
						self.revealed_boxes = self._generate_revealed_boxes_data(False)

						#Show the fully revealed board for a second.
						self._draw_board(self.main_board, self.revealed_boxes)
						pygame.display.update()
						pygame.time.wait(1000)

						#Replay the start animation
						self._start_game_animation(self.main_board)
					
					self.first_selection = None #reset first selection

		pygame.display.update()
		self.fps_clock.tick(self.settings.fps)


	

	
	def _generate_revealed_boxes(self, val):
		"""Generate revealed boxes"""

		self.revealed_boxes = []

		for i in range(self.settings.board_width):
			self.revealed_boxes.append([val] * self.settings.board_height)

		return self.revealed_boxes


	def _split_into_groups_of(self, group_size, the_list):
		"""splits a list into a list of lists"""
		result = []

		for i in range(0, len(the_list), group_size):
			result.append(the_list[i:i + group_size])
		
		return result


	def _left_top_coords_of_box(self, boxx, boxy):
		"""Convert board coords to pixel coords"""

		self.left = boxx * (self.settings.box_size + self.settings.gap_size) + self.board.x_margin
		self.top = boxy * (self.settings.box_size + self.settings.gap_size) + self.board.y_margin

		return (self.left, self.top)
	

	def _get_box_at_pixel(self, x, y):
		"""Return pixel coords"""

		for boxx in range(self.settings.board_width):
			for boxy in range(self.settings.board_height):
				self.left, self.top = self._left_top_coords_of_box(boxx, boxy)
				self.box_rect = pygame.Rect(self.left, self.top, 
								self.settings.box_size, self.settings.box_size)
				if self.box_rect.collidepoint(x, y):
					return(boxx, boxy)
		
		return (None, None)


	def _draw_icon(self, shape, color, boxx, boxy):
		"""Draw given icon."""

		self.quarter = int(self.settings.box_size * 0.25) #syntactic sugar
		self.half = int(self.settings.box_size * 0.5) #syntactic sugar

		#get pixel coords from boards coords
		self.left, self.top = self._left_top_coords_of_box(boxx, boxy)

		if shape == self.shapes.donut:
			#draw donut
			pygame.draw.circle(self.display_surf, color, (self.left + self.half, 
												self.top + self.half),self.half - 5)
		
			pygame.draw.circle(self.display_surf, self.settings.bg_color, 
					 (self.left + self.half, self.top + self.half),self.quarter - 5)
			
		elif shape == self.shapes.square:
			#draw square
			pygame.draw.rect(self.display_surf, color, (self.left + self.quarter, 
											   self.top + self.quarter, 
											   self.settngs.box_size - self.half, 
											   self.settngs.box_size - self.half))

		elif shape == self.shapes.diamond:
			pygame.draw.polygon(self.display_surf, color, 
				((self.left + self.half, self.top), 
				(self.left + self.settngs.box_size - 1, self.top + self.half), 
				(self.left + self.half, self.top + self.settngs.box_size - 1), 
				(self.left, self.top + self.half)))

		elif shape == self.shapes.lines:
			for i in range(0, self.settngs.box_size, 4):

				pygame.draw.line(self.display_surf, color, (self.left, self.top + i), 
					 (self.left + i, self.top))
				pygame.draw.line(self.display_surf, color, 
					 (self.left + i, self.top + self.settings.box_size - 1), 
					 (self.left + self.settings.box_size - 1, self.top + i))

		elif shape == self.shapes.oval:
			pygame.draw.ellipse(self.display_surf, color, 
						(self.left, self.top + self.quarter, 
	   					self.settings.box_size, self.half))
			
	
	def _get_shape_and_color(self, board, boxx, boxy):
		"""Get shape and color of the icons."""
		#shape value for x,y is board[x][y][0]
		#color value for x,y is board[x][y][1]
		return board[boxx][boxy][0], board[boxx][boxy][1]
	

	def _draw_box_covers(self, board, boxes, coverage):
		"""
		Draws boxes being covered/revealed. 'boxes' is a list
		of two-item lists, which have x,y coords of the box
		"""

		for box in boxes:
			left, top = self._left_top_coords_of_box(box[0], box[1])

			pygame.draw.rect(self.display_surf, self.settings.bg_color,
					(left, top, self.settings.box_size, self.settings.box_size))
			
			shape, color = self._get_shape_and_color(board, box[0], box[1])
			self._draw_icon(shape, color, box[0], box[1])

			if coverage > 0: #only draw the cover if there is an coverage
				pygame.rect(self.display_surf, self.settings.box_color,
				(left, top, coverage, self.settings.box_size))
			
		pygame.display.update()
		self.fps_clock.tick(self.settings.fps)

	
	def _reveal_boxes_animation(self, board, boxes_to_reveal):
		"""Box reveal animation"""

		for coverage in range(self.settings.box_size, (-self.settings.reveal_speed) - 1,
												 self.settings.reveal_speed):
			self._draw_box_covers(board, boxes_to_reveal, coverage)


	def _cover_boxes_animation(self, board, boxes_to_cover):
		"""Box cover animation"""

		for coverage in range(0, self.settings.box_size + self.settings.reveal_speed,
						self.settings.reveal_speed):
			self._draw_box_covers(board, boxes_to_cover, coverage)


	def _draw_board(self, board, revealed):
		"""Draws all the boxes or revealed state."""

		for boxx in range(self.settings.board_width):
			for boxy in range(self.settings.board_height):
				left, top = self._left_top_coords_of_box(boxx, boxy)

				if not revealed[boxx][boxy]:
					#draw covered box
					pygame.draw.rect(self.display_surf, self.settings.box_color,
					  (left, top, self.settings.box_size, self.settings.box_size))
					
				else:
					# Draw the revealed icon
					shape, color = self._get_shape_and_color(board, boxx, boxy)
					self._draw_icon(shape, color, boxx, boxy)


	def _draw_highlight_box(self, boxx, boxy):
		"""change color on hover"""
		left, top = self._left_top_coords_of_box(boxx, boxy)
		pygame.draw.rect(self.display_surf, self.settings.highlight_color,
				   (left - 5, top - 5, self.settings.box_size + 10,
					self.settings.box_size + 10), 4)
		

	def _start_game_animation(self, board):
		"""Randomly reveal boxes 8 at a time"""

		self.covered_boxes = self._generate_revealed_boxes(False)

		self.boxes = []

		for x in range(self.settings.board_width):
			for y in range(self.settings.board_height):
				self.boxes.append( (x, y) )

		random.shuffle(self.boxes)
		self.box_groups = self._split_into_groups_of(8, self.boxes)

		self._draw_board(board, self.covered_boxes)

		for box_group in self.box_groups:
			self._reveal_boxes_animation(board, box_group)
			self._cover_boxes_animation(board, box_group)


	def _games_won_animation(self, board):
		"""flash the background player when a player has won"""

		self.covered_boxes = self._generate_revealed_boxes(True)
		self.color1 = self.settings.light_bg_color
		self.color2 = self.settings.bg_color

		for i in range(13):
			self.color1, self.color2 = self.color2, self.color1
			self.display_surf.fill(self.color1)
			self._draw_board(board, self.covered_boxes)
			pygame.display.update()
			pygame.time.wait(300)


	def _has_won(self, revealed_boxes):
		"""Declare whether the player wins or not"""

		for i in revealed_boxes:
			if False in i:
				return False #return false if any boxes are covered
			
		return True
	

if __name__ == '__main__':
	mg = MatchingGame()
	mg.run_game()



