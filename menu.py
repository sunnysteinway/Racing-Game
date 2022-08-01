import time

LEVELS = 10

class GameInfo:

    def __init__(self) -> None:
        
        self.level = 1
        self.started = False
        self.start_time = 0

    def next_level(self):

        self.level += 1
        self.started = False

    def level_reset(self):

        self.__init__()

    def game_finished(self):

        return self.level > LEVELS

    def start_level(self):

        self.started = True
        self.start_time = time.time()

    def get_level_time(self):

        if not self.started:
            return 0
        else:
            return time.time() - self.start_time