import time
import movementsensor
import picamera


class PuppyClips(object):

    def __init__(self):
        self._movementsensor = movementsensor.MovementSensor()
        self._camera = picamera.PiCamera()

    def run(self, round_count='infinite'):
        loop_count = round_count if round_count != 'infinite' else 1
        while loop_count > 0:
            time.sleep(1)
            if self._movementsensor.is_movement():
                self.take_clip()
            if round_count != 'infinite':
                loop_count -= 1

    def take_clip(self):
        self._camera.start_recording('{}.h264'.format(time.strftime('%Y.%m.%d-%H:%M')))
        time.sleep(60)
        self._camera.stop_recording()


if __name__ == '__main__':
    pc = PuppyClips()
    pc.run('infinite')
