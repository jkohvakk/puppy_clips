import time
import movementsensor
import picamera


class PuppyClips(object):

    def __init__(self):
        self._movementsensor = movementsensor.MovementSensor()
        self._camera = picamera.PiCamera()

    def run(self, round_count=None):
        for round in range(round_count):
            time.sleep(1)
            if self._movementsensor.is_movement():
                self.take_clip()

    def take_clip(self):
        self._camera.start_recording('TODO_FILENAME')
        time.sleep(60)
        self._camera.stop_recording()

