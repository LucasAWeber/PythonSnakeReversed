# Segment class library

# Import
import pygame


# Class
class Segment(pygame.sprite.Sprite):

    # -- Methods
    # Constructor function
    def __init__(self, x, y, snake_direction):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.image.load("extra/SnakeHead.png").convert()

        # Determines the rotation of snake head based on the direction it is going
        if snake_direction == "right":
            rotation = -90
        elif snake_direction == "left":
            rotation = 90
        elif snake_direction == "down":
            rotation = 180
        else:
            rotation = 0

        # Rotates image
        self.image = pygame.transform.rotate(self.image, rotation)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Function that turns heads into the body as we are moving
    def head_swap(self, screen):
        self.image = pygame.image.load("extra/SnakeBody.png").convert()
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # Function that turns body into tail as we are moving
    def body_swap(self, screen, rotation):
        self.image = pygame.image.load("extra/SnakeTail.png").convert()
        self.image = pygame.transform.rotate(self.image, rotation)
        screen.blit(self.image, (self.rect.x, self.rect.y))