import unittest
import puppyclips
import mock_time


class SelfTrackingMock(object):

    instances = []

    @classmethod
    def get_instances(cls):
        return cls.instances

    @classmethod
    def reset(cls):
        cls.instances = []

    def __init__(self):
        self.__class__.instances.append(self)
        self._calls = []


class MockMovementSensor(SelfTrackingMock):

    def is_movement(self):
        self._calls.append('is_movement')
        return self._movement.pop()

    def get_calls(self):
        return self._calls

    def set_movement(self, movement):
        self._movement = movement


class MockPiCamera(SelfTrackingMock):

    def __init__(self):
        super(MockPiCamera, self).__init__()
        self.start_recording_calls = []
        self.stop_recording_calls = []

    def start_recording(self, *args):
        self.start_recording_calls.append(args)

    def stop_recording(self, *args):
        self.stop_recording_calls.append(args)


class MockSubprocess(object):

    call_calls = []

    @classmethod
    def call(cls, args):
        cls.call_calls.append(args)

    @classmethod
    def reset(cls):
        cls.call_calls = []


class MockOs(object):

    remove_calls = []

    @classmethod
    def remove(cls, filename):
        cls.remove_calls.append(filename)



class TestPuppyClips(unittest.TestCase):

    def setUp(self):
        MockMovementSensor.reset()
        MockPiCamera.reset()
        MockSubprocess.reset()
        puppyclips.movementsensor.MovementSensor = MockMovementSensor
        puppyclips.picamera.PiCamera = MockPiCamera
        puppyclips.time = mock_time
        mock_time.reset()
        self.pc = puppyclips.PuppyClips()

    def test_movement_sensor_is_polled_every_second(self):
        self.pc._movementsensor.set_movement([False, False, False])
        self.pc.run(3)
        self.assertEqual(mock_time.get_mock_sleep_calls(), 3)
        self.assertEqual(mock_time.get_mock_sleep_times(), [1, 1, 1])
        self.assertEqual(len(MockMovementSensor.get_instances()), 1)
        self.assertEqual(MockMovementSensor.get_instances()[0].get_calls(),
                         ['is_movement', 'is_movement', 'is_movement'])

    def test_if_movement_a_minute_clip_is_taken_with_name_based_on_current_datetime(self):
        self.pc._movementsensor.set_movement([False, True, False])
        self.pc.run(3)
        self.assertEqual(mock_time.get_mock_sleep_calls(), 4)
        self.assertEqual(mock_time.get_mock_sleep_times(), [1, 1, 60, 1])
        self.assertEqual(MockPiCamera.get_instances()[0].start_recording_calls[0],
                         ('2015.01.31-20:10.h264',))
        self.assertEqual(1, len(MockPiCamera.get_instances()[0].stop_recording_calls))

    def test_it_is_possible_to_set_max_clips(self):
        self.pc._movementsensor.set_movement([True, True, True])
        self.pc.run(3, max_clips=2)
        self.assertEqual(2, len(MockPiCamera.get_instances()[0].start_recording_calls))
        self.assertEqual(2, len(MockPiCamera.get_instances()[0].stop_recording_calls))
        self.assertEqual(mock_time.get_mock_sleep_calls(), 4)

    def test_clip_is_converted_from_h264_to_mp4(self):
        puppyclips.subprocess = MockSubprocess
        puppyclips.os = MockOs
        self.pc._movementsensor.set_movement([False, True, False])
        self.pc.run(3)
        self.assertEqual(MockSubprocess.call_calls[0], ['MP4Box', '-fps', '30', '-add',
                                                      '2015.01.31-20:10.h264', '2015.01.31-20:10.mp4'])
        self.assertEqual(MockOs.remove_calls[0], '2015.01.31-20:10.h264')

    def test_clip_is_uploaded_to_dropbox(self):
        puppyclips.subprocess = MockSubprocess
        self.pc._movementsensor.set_movement([False, True, False])
        self.pc.run(3)
        self.assertEqual(MockSubprocess.call_calls[1], ['/home/pi/Dropbox-Uploader/dropbox_uploader.sh', 'upload',
                                                        '2015.01.31-20:10.mp4', '2015.01.31-20:10.mp4'])



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()