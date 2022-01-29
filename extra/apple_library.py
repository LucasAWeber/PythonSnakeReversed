# Apple class library

# Import
import pygame
import random


# Class
class Apple(pygame.sprite.Sprite):
    def __init__(self, segment_margin, segment_width, segment_height, colour):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(colour)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = 4 + random.randrange(1, 44) * (segment_width + segment_margin)
        self.rect.y = 4 + random.randrange(1, 29) * (segment_height + segment_margin)
