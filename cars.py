from numpy import diff
import pygame
import time
import math

import utilities

RED_CAR = utilities.scale_image(pygame.image.load('images/red-car.png'), 0.55)
GREEN_CAR = utilities.scale_image(pygame.image.load('images/green-car.png'), 0.55)

PATH = [(176, 164), (173, 112), (133, 72), (75, 94), (72, 466), (286, 701), (386, 714), (404, 648), (413, 551), (465, 488), (561, 502), (593, 555), (611, 643), (614, 711), (719, 732), (745, 408), (688, 366), (424, 350), (418, 266), (722, 245), (729, 95), (294, 89), (285, 366), (223, 413), (182, 378), (175, 250)]

class AbstractCar:

    def __init__(self, max_vel, rotation_vel):

        self.img = self.IMG
        self.max_vel = max_vel
        self.rotation_vel = rotation_vel
        self.acceleration = 0.1

        # initialize the starting status and the position
        self.vel = 0
        self.angle = 0
        self.x, self.y = self.START_POS

    def rotate(self, left=False, right=False):

        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def move_forward(self):

        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):

        self.vel = max(self.vel - 0.8 * self.acceleration, -0.5 * self.max_vel)
        self.move()

    def move(self):

        rad = math.radians(self.angle)

        self.x -= math.sin(rad) * self.vel
        self.y -= math.cos(rad) * self.vel

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))

        # calculate the point of interest if there is one
        poi = mask.overlap(car_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = self.vel = 0

    def draw(self, win):
        utilities.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

class PlayerCar(AbstractCar):
    '''
    The class for the player's car
    (inherits from the AbstractCar class)
    '''
    IMG = RED_CAR
    START_POS = (180, 200)

    def reduce_speed(self):

        self.vel = max(self.vel - 0.45 * self.acceleration, 0)
        self.move()

    def bounce(self):
        """
        If the car hit the boundery of the track,
        it will bounce back to the track
        """
        self.vel *= -0.8
        self.move()

class ComputerCar(AbstractCar):
    
    IMG = GREEN_CAR
    START_POS = (150, 200)

    def __init__(self, max_vel, rotation_vel, path=[]):

        # use the init method from the abstract class
        super().__init__(max_vel, rotation_vel)

        self.path = PATH

        # keep track of the current point
        self.cur_point = 0

        self.vel = self.max_vel

    def draw_point(self, win):
        
        for p in self.path:

            pygame.draw.circle(win, color=(255, 0,0), center=p, radius=5)

    def draw(self, win):
        
        super().draw(win)
        self.draw_point(win)

    def calculate_angle(self):
        '''
        Calculate the angle of the target point
        '''
        # grab the position of the target point
        targetX, targetY = self.path[self.cur_point]

        # calculate the distance between the target point and the current position
        diffX = targetX - self.x
        diffY = targetY - self.y

        if diffY == 0:
            desired_angle = math.pi / 2
        else:
            desired_angle = math.atan(diffX / diffY)
        
        if targetY > self.y:
            desired_angle += math.pi

        difference_angle = self.angle - math.degrees(desired_angle)

        if difference_angle >= 180:
            difference_angle -= 360
        
        if difference_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_angle)) # we want to avoid the car jittering
        else:
            self.angle += min(self.rotation_vel, abs(difference_angle))

    def update_path_point(self):
        '''
        Check if the car has reached the point or not
        '''
        target = self.path[self.cur_point]
        ego = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())

        # if we have collide the target point, then we can move forward to the next target
        if ego.collidepoint(*target):
            self.cur_point += 1

    def move(self):
        """
        The computer car needs to follow along the predefined path
        """
        # we want to make sure that it does not try to access an index point that does not exist
        if self.cur_point >= len(self.path):
            return
        
        self.calculate_angle()

        self.update_path_point()

        super().move()