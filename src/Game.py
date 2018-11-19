# Ryan Allard PyGame general playtesting, Oct 18/18

## Setup debugging tools
# Set debug mode
DEBUG = True

# Define dprint function:
if DEBUG:
    def dprint(*value, sep = " ", end = "\n"):
        print(*value, sep = sep, end = end)
else:
    def dprint(*value, sep = " ", end = "\n"):
        pass

## Import modules
# Import pygame module for display
import pygame

# Import os module
import os

# Import Path
from pathlib import Path

# Raise up the cwd
mainDr = Path(__file__).resolve().parents[1]
os.chdir(mainDr)

dprint(os.getcwd())

# Import random module
import random

# Import config file
import Config as config

# Import Tile class from seperate file
from Tiles import Tile


# Pair class
class Pair:

    def __init__(self, x, y):

        self.x = x
        self.y = y


# Base class for game panels
class Panel:

    def __init__(self, rect):

        # Create image
        self.image = pygame.Surface((rect.width, rect.height))

        # Retrieve rect reference
        self.rect = self.image.get_rect()

        # Pass rect pos
        self.rect.x = rect.x
        self.rect.y = rect.y
        

    # Define how to redraw the panel (likely to be overridden)
    def update(self):
        """Update the graphical representation of the map"""

        # Fill black background
        self.image.fill(config.color.black)

    # Blits onto target surface
    def draw(self, surface, update = True):
        """Draw the map onto a surface"""

        # Update if specified
        if update:
            self.update()

        # Blit onto the target surface
        surface.blit(self.image, self.rect)

        

# Set class that holds a top-level sprite and keeps track of tiles
class Map(Panel):

    def __init__(self, pos, size, scale, rand = True):
        """Creates a map of tiles using"""

        # Call parent constructor
        super().__init__(pygame.Rect(pos, (size * scale, size * scale)))

        # Create tile group
        self.tileGroup = pygame.sprite.Group()
          
        # Create tile map
        for y in range(size):
            for x in range(size):

                # Generate random tile of the 4 variants
                if rand:
                    tile = Tile.variant(random.randrange(4), scale)
                # Dunno if this is useful
                else:
                    tile = Tile(scale)

                # Place the tile depeding on loop progress
                tile.rect.x = x*config.game.tileSize
                tile.rect.y = y*config.game.tileSize
                
                # Add tile to sprite groups
                self.tileGroup.add(tile)

    def update(self):
        """Update the graphical representation of the map"""

        # Fill black background
        self.image.fill(config.color.black)

        # Draw tiles
        self.tileGroup.draw(self.image)


    def pos_to_tile(self, x, y):
        """Takes mouse position and returns tile"""
        # Check every tile
        for tile in self.tileGroup:
            
            # If the tile's rect collides with the shifted position, return it
            # Shift position logic:
            #   The tiles 0,0 is map top-left
            #   By subtracting map position from mouse position
            #   We get relative position identical to tiles
            if tile.rect.collidepoint(x - self.rect.x, y - self.rect.y):
                return tile


## Define Game class
class Game:

    # Constructor
    def __init__(self, display):
        """Create a Game object"""

        # Create screen
        self.display = display

        # Set caption (window title)
        pygame.display.set_caption(config.game.caption)

        # Create clock object
        self.clock = pygame.time.Clock()

        # Set desired FPS
        self.maxFPS = config.game.fps

        ## Create sprite lists
        # Tile sprite group
        self.tileGroup = pygame.sprite.Group()

        # General sprite group
        self.allGroup = pygame.sprite.Group()

        # Create main surfaces
        #self.map = pygame.Surface((config.game.mapSize, config.game.height))
        self.map = None

        self.interface = pygame.Surface((config.game.interfaceWidth, config.game.height))
        
        # Do game-related less technical stuff
        self.reset()



    # Reset function
    def reset(self):
        """Restarts the game"""

        #Clear sprite groups
        #self.tileGroup.empty()
        self.allGroup.empty()

        self.map = Map((0,0),
                       config.game.mapSize // config.game.tileSize,
                       config.game.tileSize, rand = True)



    # Main loop
    def loop(self):
        """Start the main game loop, which continues until is interiorly stopped"""
        
        # Initalize loop variable
        done = False

        # Main game loop
        while not done:

            # Iterate through events in pygame queue
            for event in pygame.event.get():

                # Check for quit event
                if event.type == pygame.QUIT:
                    # Setup to exit loop
                    done = True

                # Check for keypresses
                elif event.type == pygame.KEYDOWN:
                    pass

                # Check for mouse press event
                elif event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        # Reference clicked tile
                        self.selectedTile = self.map.pos_to_tile(*event.pos)

                        # Make sure tile was found
                        if self.selectedTile is not None:
                            
                            # Output tile type
                            dprint(self.selectedTile.type)

                            # Test of changing tile image
                            self.selectedTile.image = pygame.transform.scale(
                                        pygame.image.load("resources/blank.png"),
                                              (30,30))
                    
                # Print out the event
                dprint(event)

            ## Test of moving the tile with the mouse
                """
            mousePos = pygame.mouse.get_pos()
            self.tile.rect.x = mousePos[0]
            self.tile.rect.y = mousePos[1]
            """


            # Redraw the graphics
            self.display.fill(config.color.black)

            #self.map.fill(config.color.black)
            #self.allGroup.draw(self.map)

            #self.map.update()

            self.interface.fill(config.color.grey)

            #self.display.blit(self.map, (0, 0))
            self.map.draw(self.display)
            self.display.blit(self.interface, (config.game.mapSize, 0))
            
            # Flip screen
            pygame.display.update()

            # Try and run at a certain FPS
            self.clock.tick(self.maxFPS)


## Define main function
def main():

    # Initalize pygame
    pygame.init()

    # Create a screen
    screen = pygame.display.set_mode((config.game.width, config.game.height))

    # Create game with the screen
    game = Game(screen)
    # Start game (blocks till game finishes)
    game.loop()

    # Shutdown pygame
    pygame.quit()

# Run program (if file run and not imported)
if __name__ == "__main__":
    main()
