import pygame

import utilities
import cars
import menu

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("comicsans", 44)

# load images
GRASS = utilities.scale_image(pygame.image.load('images/grass.jpg'), factor=2.5)
TRACK = utilities.scale_image(pygame.image.load('images/track.png'), factor=0.9)
TRACK_BORDER = utilities.scale_image(pygame.image.load('images/track-border.png'), factor=0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = pygame.image.load('images/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)
RED_CAR = utilities.scale_image(pygame.image.load('images/red-car.png'), 0.55)
GREEN_CAR = utilities.scale_image(pygame.image.load('images/green-car.png'), 0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()

# colours
GAINSBORO = (220,220,220)
CORAL = (255,127,80)

# set the uniform FPS rate
FPS = 60

def draw(win, images, player_car, computer_car, game_info):
    """
    Draw objects and render text onto the canvas
    """
    # draw the backgrounds onto the canvas
    for img, pos in images:
        win.blit(img, pos)

    # render text onto the canvas
    level_txt = MAIN_FONT.render(f"Level {game_info.level}", 1, GAINSBORO)
    win.blit(level_txt, (10, HEIGHT - level_txt.get_height() - 70))
    time_txt = MAIN_FONT.render(f"Time: {game_info.get_level_time():.2f} s", 1, CORAL)
    win.blit(time_txt, (10, HEIGHT - time_txt.get_height() - 5))
    
    player_car.draw(win)
    computer_car.draw(win)
    pygame.display.update()

def move_player(player_car):

    # get the registered key (a list of keys)
    keys = pygame.key.get_pressed()

    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    elif keys[pygame.K_d]:
        player_car.rotate(right=True)
        
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    elif keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

def finish_line_ribbon(player_car, computer_car):
    player_finish_poi = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    computer_finish_poi = computer_car.collide(FINISH_MASK, *FINISH_POSITION)

    if computer_finish_poi != None:
        print("Computer wins!")
        player_car.reset()
        computer_car.reset()

    if player_finish_poi != None:

        # check from which direction does the car collide
        if player_finish_poi[1] == 0:
            player_car.bounce()
        # collide with the finish line after finishing the entire track
        else:
            print("Player wins!")
            player_car.reset()
            computer_car.reset()

def main():
    
    # set up the display
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")

    running = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (130, 250)), (TRACK_BORDER, (0, 0))]

    player_car = cars.PlayerCar(4, 3)
    computer_car = cars.ComputerCar(4, 4)
    game_info = menu.GameInfo()
    flagMenu = True

    while running:

        clock.tick(FPS) # the while loop runs at 60 FPS

        draw(WIN, images, player_car, computer_car, game_info)

        while not game_info.started and flagMenu:
            utilities.show_start_menu(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}...")
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    flagMenu = False
                    pygame.quit()
                    break
                # get the path for the computer car
                elif event.type == pygame.KEYDOWN:
                    game_info.start_level()
                    flagMenu = False

        if game_info.started:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    break
            # # get the path for the computer car
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()
            #     computer_car.path.append(pos)
        
            move_player(player_car)
            computer_car.move()

            # check if the car hit the boundry of the track
            if player_car.collide (TRACK_BORDER_MASK) != None:
                player_car.bounce()

            # detect which car enter the finish line first
            finish_line_ribbon(player_car, computer_car)
        
    # print(computer_car.path)
    pygame.quit()

if __name__ == "__main__":
    main()