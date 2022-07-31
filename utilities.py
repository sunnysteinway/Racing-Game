import pygame
import pickle

def scale_image(img, factor):
    """
    Scale the given image
    """
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def blit_rotate_center(win, image, top_left, angle):
    """
    Rotate the image
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    win.blit(rotated_image, new_rect.topleft)
    # self.rotated = pygame.transform.rotozoom(self.img, math.degrees(self.theta), scale=1)
    # self.rect = self.rotated.get_rect(center=(self.x, self.y))

def load_resources(filename, type):
    """
    Load resources
    """
    if type == 0:
        # unpickle
        with open(filename, "rb") as fp:
            return pickle.load(fp)