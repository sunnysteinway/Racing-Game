import pygame

import utilities
import cars
import menu

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("comicsans", 40)
MEDIUM_FONT = pygame.font.SysFont("georgia", 30)
SMALL_FONT = pygame.font.SysFont("georgia", 24)

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
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SLATE = (119,136,153)
GAINSBORO = (220,220,220)
CORAL = (255,127,80)
RED = (255,0,0)
MAROON = (128,0,0)
LIME = (0,255,0)
LAWN = (124,252,0)
OLIVE = (107,142,35)
INDIGO = (75,0,130)
VIOLET = (138,43,226)
GOLD = (255,215,0)
ORANGE = (255,140,0)
AZURE = (240,255,255)

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

def finish_line_ribbon(win, player_car, computer_car, game_info):
    """
    Detect which car cross the finish line first
    """
    player_finish_poi = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    computer_finish_poi = computer_car.collide(FINISH_MASK, *FINISH_POSITION)

    if computer_finish_poi != None:
        utilities.show_msg(win, MAIN_FONT, f"You lost!")
        pygame.display.update()
        pygame.time.wait(100)
        game_info.reset()
        player_car.reset()
        computer_car.reset()
        game_info.start_level()
        return -1

    if player_finish_poi != None:

        # check from which direction does the car collide
        if player_finish_poi[1] == 0:
            player_car.bounce()
            return -1
        # collide with the finish line after finishing the entire track
        else:
            ret = round(game_info.get_level_time(), 3)
            game_info.next_level()  # go to the next level
            player_car.reset()
            computer_car.level_up(game_info.level)  # update the difficulty of the next level
            game_info.start_level()
            return ret
    
    return -1

def game_intro(win):
    '''
    The game intro page
    '''
    intro = True
    player_name = "Enter Your Name..."

    while intro:

        win.blit(GRASS, (0, 0))
        win.blit(TRACK, (0,0))
        pygame.draw.rect(win, SLATE, (0, 200, WIDTH, HEIGHT-400))

        welcome_txt = MAIN_FONT.render("Welcome to the racing game", 1, GAINSBORO, SLATE)
        win.blit(welcome_txt, welcome_txt.get_rect(center=(WIDTH/2, HEIGHT/2-100)))
        welcome_txt = MAIN_FONT.render(player_name, 1, (255,69,0))
        win.blit(welcome_txt, welcome_txt.get_rect(center=(WIDTH/2, HEIGHT/2)))
        welcome_txt = MAIN_FONT.render("Press ENTER to begin or press ESC to exit", 1, GAINSBORO, SLATE)
        pos = welcome_txt.get_rect(center=(WIDTH/2, HEIGHT/2))
        pos[1] += welcome_txt.get_height()
        win.blit(welcome_txt, pos)

        # some constants
        quitX = 150
        quitY = 500
        startX = WIDTH-250
        startY = 500
        leaderboardX = 0.5*(quitX+startX)
        leaderboardY = 500
        buttonWidth = 150
        buttonHeight = 50

        mouse = pygame.mouse.get_pos() # get the position of the mouse
        click = pygame.mouse.get_pressed()  # get the buttons of the mouse

        # determine whether the mouse is within the buttons
        pygame.draw.rect(win, MAROON, (quitX, quitY, buttonWidth, buttonHeight))
        pygame.draw.rect(win, OLIVE, (startX, startY, buttonWidth, buttonHeight))
        pygame.draw.rect(win, INDIGO, (leaderboardX, leaderboardY, buttonWidth, buttonHeight))

        if utilities.detect_mouse(mouse, quitX, quitY, buttonWidth, buttonHeight):
            pygame.draw.rect(win, RED, (quitX, quitY, buttonWidth, buttonHeight))
            if click[0]:
                return -1, player_name
        if utilities.detect_mouse(mouse, startX, startY, buttonWidth, buttonHeight):
            pygame.draw.rect(win, LIME, (startX, startY, buttonWidth, buttonHeight))
            if click[0]:
                return 2, player_name
        if utilities.detect_mouse(mouse, leaderboardX, leaderboardY, buttonWidth, buttonHeight):
            pygame.draw.rect(win, VIOLET, (leaderboardX, leaderboardY, buttonWidth, buttonHeight))
            if click[0]:
                return 1, player_name

        # put text on the buttons
        menu_txt = MEDIUM_FONT.render("Quit", 1, BLACK)
        win.blit(menu_txt, menu_txt.get_rect(center=(quitX+0.5*buttonWidth, quitY+0.5*buttonHeight)))
        menu_txt = MEDIUM_FONT.render("Start", 1, BLACK)
        win.blit(menu_txt, menu_txt.get_rect(center=(startX+0.5*buttonWidth, startY+0.5*buttonHeight)))
        menu_txt = SMALL_FONT.render("Leaderboard", 1, WHITE)
        win.blit(menu_txt, menu_txt.get_rect(center=(leaderboardX+0.5*buttonWidth, leaderboardY+0.5*buttonHeight)))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return -1, player_name
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return 2, player_name
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
    return 0, player_name

def game_leaderboard(win, board):
    
    leader = True
    ranking = board.access()
    while leader:

        # the background of the leaderboard
        win.fill((176,196,222))

        # the title of the leaderboard
        title_txt = MEDIUM_FONT.render("Leaderboard", 1, BLACK)
        win.blit(title_txt, title_txt.get_rect(center=(0.5*WIDTH, 80)))
        pygame.draw.line(win, BLACK, start_pos=(50, 100), end_pos=(WIDTH - 50, 100))

        # the content of the leaderboard
        curY = 200
        i = 1
        
        for idx in range(0, 5):
            item = ranking[idx]
            title_txt = MEDIUM_FONT.render(f"# {i} {item[1]}: {item[0]} s", 1, BLACK)
            win.blit(title_txt, title_txt.get_rect(center=(0.5*WIDTH, curY)))
            i += 1
            curY += 60

        # the buttons
        buttonWidth = 150
        buttonHeight = 50
        backX = 0.5*(WIDTH-buttonWidth)
        backY = 700
        
        mouse = pygame.mouse.get_pos() # get the position of the mouse
        click = pygame.mouse.get_pressed()  # get the buttons of the mouse

        # determine whether the mouse is within the buttons
        pygame.draw.rect(win, ORANGE, (backX, backY, buttonWidth, buttonHeight))

        if utilities.detect_mouse(mouse, backX, backY, buttonWidth, buttonHeight):
            pygame.draw.rect(win, GOLD, (backX, backY, buttonWidth, buttonHeight))
            if click[0]:
                return 2

        # put text on the buttons
        menu_txt = MEDIUM_FONT.render("Back", 1, BLACK)
        win.blit(menu_txt, menu_txt.get_rect(center=(backX+0.5*buttonWidth, backY+0.5*buttonHeight)))

        pygame.display.update()

        # detect quit action
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return -1

    return 0

def main():
    
    # set up the display
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racing Game")

    running = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (130, 250)), (TRACK_BORDER, (0, 0))]

    player_car = cars.PlayerCar(10, 3)
    computer_car = cars.ComputerCar(1, 4)
    game_info = menu.GameInfo()
    flagMenu = True
    board = menu.Leaderboard()

    selectWin = 0

    while running:

        clock.tick(FPS) # the while loop runs at 60 FPS

        # determine which window the player if in
        if selectWin == 0:
            ret = game_intro(WIN)
            selectWin = ret[0]
            player_car.player_name = ret[1]
            if selectWin < 0:
                break
        elif selectWin == 1:
            selectWin = game_leaderboard(WIN, board)
            if selectWin < 0:
                break
        else:

            draw(WIN, images, player_car, computer_car, game_info)

            while not game_info.started and flagMenu:
                utilities.show_msg(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}...")
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                        flagMenu = False
                        break
                    # get the path for the computer car
                    elif event.type == pygame.KEYDOWN:
                        game_info.start_level()
                        flagMenu = False

            if not flagMenu:
                computer_car.move()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        running = False
                        break
                    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_i):
                        player_car.x = 150
                        player_car.y = 330
                    elif (event.type == pygame.KEYDOWN and event.key == pygame.K_o):
                        computer_car.x, computer_car.y = computer_car.path[-2]
                    
                move_player(player_car)

                # check if the car hit the boundry of the track
                if player_car.collide (TRACK_BORDER_MASK) != None:
                    player_car.bounce()

                # detect which car enter the finish line first
                player_time = finish_line_ribbon(WIN, player_car, computer_car, game_info)

                # check if the player makes in to the leaderboard
                if player_time > 0:
                    board.append((player_time, player_car.player_name))
                
                if game_info.game_finished():
                    utilities.show_msg(WIN, MAIN_FONT, "You won the game!")
                    pygame.time.wait(2500)
                    running = False
                    break
            
    pygame.quit()   # NOTE: it does not exit the program

if __name__ == "__main__":
    main()