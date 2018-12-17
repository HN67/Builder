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
        """Update the graphical representation of the panel"""

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

        

# Class for an Icon widget
class Icon(Panel):

    def __init__(self, rect, image, border = 0, bc = (0,0,0),  outer = False):
        """Image would be a pygame.Surface
           Border is border width in pixels
           If outer is True, the border is drawn around the image,
           expanding the rect, otherwise it is drawn atop the image"""

        # Check if border is in or out
        if outer:
            rect.width += border
            rect.height += border
        
        # Call parent constructor
        super().__init__(rect)

        # Save border for use in update method
        self.border = border

        # Save image (as pic to not conflict with top surface image)
        self.pic = image

        # Save outer bool for use in update method, but privately
        # since it cannot be hot changed
        self._outer = outer

        # Save border color
        self.bc = bc

    # Update method
    def update(self):

        # Clear image
        self.image.fill(config.color.black)

        # Check if border is outside to determine whether to shift pic or not
        if self._outer:

            self.image.blit(self.pic, (self.border, self.border))

        else:

            self.image.blit(self.pic, (0, 0))

        # Draw border
        pygame.draw.rect(self.image, self.bc,
                         self.rect, self.border)
        

# Set class that holds a top-level sprite and keeps track of tiles
class Map(Panel):

    def __init__(self, origin, size, scale, rand = True):
        """Creates a map of tiles using"""

        # Call parent constructor
        super().__init__(pygame.Rect(origin, (size * scale, size * scale)))

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


# Class for a control interface
# (either dynamic or designed for this project, havent decided)
# Probably specifically designed for interfacing with tiles
class Interface(Panel):

    def __init__(self, origin, width, height):
        
        # Call parent constructor
        super().__init__(pygame.Rect(origin, (width, height)))

        # Create config object
        self.cfg = config.interface()
        
        # Create blank tile
        self.tile = Tile(config.game.tileSize)

        # Create tile icon
        # Create starting rect with tile size
        iconRect = pygame.Rect((0, 0),
                               (self.tile.rect.width, self.tile.rect.height))
        
        # Create tileIcon using rect
        self.tileIcon = Icon(iconRect, self.tile.image, border = self.cfg.imgBorder,
                             bc = config.color.brown, outer = True)

        # Center tileIcon rect
        self.tileIcon.rect.center = (self.rect.width*self.cfg.imgXRatio,
                                     self.rect.height*self.cfg.imgYRatio)



    def update(self):
        """Update the graphics of the interface to prepare for drawing"""

        # Fill grey background
        self.image.fill(config.color.lightGrey)

        # Draw border
        pygame.draw.rect(self.image, config.color.black,
                         pygame.Rect(0, 0, self.rect.width, self.rect.height),
                         10)

        # Draw tile icon
        # Pass self tile image to tileIcon so it updates
        self.tileIcon.image = self.tile.image
        # Draw tileIcon onto self image (Main panel)
        self.tileIcon.draw(self.image)

    

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

        self.interface = None
        
        # Do game-related less technical stuff
        self.reset()



    # Reset function
    def reset(self):
        """Restarts the game"""

        # Clear sprite groups
        self.allGroup.empty()

        # Create map based on config
        self.map = Map((0,0),
                       config.game.mapSize // config.game.tileSize,
                       config.game.tileSize, rand = True)
        
        # Create interface
        self.interface = Interface((config.game.mapSize, 0),
                                   config.game.interfaceWidth, config.game.mapSize)

        # Create tile selector
        self.selectedTile = Tile(config.game.tileSize)
        

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

                            # Give the selected tile to the Interface
                            self.interface.tile = self.selectedTile
                            
                    
                # Print out the event
                dprint(event)


            # Redraw the graphics
            # Root background color
            self.display.fill(config.color.black)

            # Draw the map and interface
            self.map.draw(self.display)
            self.interface.draw(self.display)
            
            # Flip the display
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
