import time
import movementsensor

class PuppyClips(object):

    def __init__(self):
        self._movementsensor = movementsensor.MovementSensor()

    def run(self, round_count=None):
        for round in range(round_count):
            time.sleep(1)
            self._movementsensor.is_movement()
