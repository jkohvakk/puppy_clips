import time
import movementsensor
import picamera
import sys
import subprocess


class PuppyClips(object):

    def __init__(self):
        self._movementsensor = movementsensor.MovementSensor()
        self._camera = picamera.PiCamera()

    def run(self, round_count='infinite', max_clips=60):
        loop_count = round_count if round_count != 'infinite' else 1
        self._clips = 0
        while loop_count > 0 and self._clips < max_clips:
            time.sleep(1)
            if self._movementsensor.is_movement():
                self.take_clip()
            if round_count != 'infinite':
                loop_count -= 1

    def take_clip(self):
        name = '{}'.format(time.strftime('%Y.%m.%d-%H:%M'))
        self._camera.start_recording('{}.h264'.format(name))
        time.sleep(60)
        self._camera.stop_recording()
        subprocess.call(['MP4Box', '-fps', '30', '-add',
                         '{}.h264'.format(name),
                         '{}.mp4'.format(name)])
        self._clips += 1


if __name__ == '__main__':
    pc = PuppyClips()
    pc.run(round_count='infinite', max_clips=sys.argv[1])
