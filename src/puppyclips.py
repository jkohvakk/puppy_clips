import time
import movementsensor
import picamera
import sys
import subprocess
import os


class PuppyClips(object):

    def __init__(self):
        self._movementsensor = movementsensor.MovementSensor()
        self._camera = picamera.PiCamera()
        self._camera.exposure_compensation = 25

    def run(self, round_count='infinite', max_clips=60):
        loop_count = round_count if round_count != 'infinite' else 1
        clips = 0
        while loop_count > 0 and clips < max_clips:
            time.sleep(1)
            if self._movementsensor.is_movement():
                self.take_clip()
                clips += 1
            if round_count != 'infinite':
                loop_count -= 1

    def take_clip(self):
        basename = '{}'.format(time.strftime('%Y.%m.%d-%H:%M'))
        h264_name = '{}.h264'.format(basename)
        mp4_name = '{}.mp4'.format(basename)

        self._camera.start_recording(h264_name)
        time.sleep(60)
        self._camera.stop_recording()

        self._convert_h264_to_mp4(h264_name, mp4_name)
        self._upload_to_dropbox(mp4_name)

    def _convert_h264_to_mp4(self, h264_name, mp4_name):
        subprocess.call(['MP4Box', '-fps', '30', '-add',
                         h264_name,
                         mp4_name])
        os.remove(h264_name)

    def _upload_to_dropbox(self, mp4_name):
        subprocess.call(['/home/pi/Dropbox-Uploader/dropbox_uploader.sh', 'upload',
                         mp4_name, mp4_name])


if __name__ == '__main__':
    pc = PuppyClips()
    pc.run(round_count='infinite', max_clips=sys.argv[1])
