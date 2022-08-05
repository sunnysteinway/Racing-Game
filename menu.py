import time
import pickle

LEVELS = 3

class GameInfo:

    def __init__(self) -> None:
        
        self.level = 1
        self.started = False
        self.start_time = 0

    def next_level(self):

        self.level += 1
        self.started = False

    def reset(self):

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

class Leaderboard:

    def __init__(self) -> None:
        self.q = []
        self.filename = "leaderboard"
        self.size = 5
        self.load_data()
        pass

    def load_data(self):

        with open(self.filename, 'rb') as f:
            self.q = pickle.load(f)

    def save_data(self):

        with open(self.filename, 'wb') as f:
            pickle.dump(self.q, f)

    def append(self, data):

        if len(self.q) < self.size:
            self.q.append(data)
            self.q.sort()
            return True
        else:
            last_item = self.q[-1]

            if data[0] > last_item[0]:
                return False
            else:
                self.q.append(data)
                self.q.sort()
                self.q.pop()
                self.save_data()
                return True
    
    def access(self):

        return self.q.copy()

    def reset_leaderboard(self):

        self.q = []
        self.q.append((100, "Unknown"))
        self.q.append((100, "Unknown"))
        self.q.append((100, "Unknown"))
        self.q.append((100, "Unknown"))
        self.q.append((100, "Unknown"))

        self.save_data()