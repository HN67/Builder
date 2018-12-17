# Tile class file

# Import modules
import pygame
import Config as config

# Tile class
class Tile(pygame.sprite.Sprite):
    """Tile Sprite Class"""

    def __init__(self, size, image = "null"):
        """Creates an unlogiced tile (with image)"""

        # Call parent constructor
        super().__init__()

        # Define size
        self.size = size

        # Define type
        self.type = image

        # Grab image
        self.image = pygame.transform.scale(pygame.image.load(f"resources/{image}.png"),
                                      (self.size, self.size))

        # Set color key to white
        self.image.set_colorkey(config.color.white)
        
        # Reference image rect
        self.rect = self.image.get_rect()

    
    def variant(var, size):
        """Creates variant tile object"""

        # Subclass references
        refs = {0: FieldTile, "field": FieldTile,
                1: WaterTile, "water": WaterTile,
                2: MountainTile, "mountain": MountainTile,
                3: ForestTile, "forest": ForestTile}

        return refs[var](size)

    # Draws tile onto a surface
    def draw(self, surface):
        """Draw on to target surface"""
        
        surface.blit(self.image, self.rect)

class FieldTile(Tile):

    def __init__(self, size):

        # Call parent constructor
        super().__init__(size, "field")                

class WaterTile(Tile):

    def __init__(self, size):

        # Call parent constructor
        super().__init__(size, "water")


class MountainTile(Tile):

    def __init__(self, size):

        # Call parent constructor
        super().__init__(size, "mountain")


class ForestTile(Tile):

    def __init__(self, size):

        # Call parent constructor
        super().__init__(size, "forest")
