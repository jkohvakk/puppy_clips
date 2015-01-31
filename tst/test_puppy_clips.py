import unittest
import puppyclips
import mock_time


class MockMovementSensor(object):

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

    def is_movement(self):
        self._calls.append('is_movement')
        return self._movement.pop()

    def get_calls(self):
        return self._calls

    def set_movement(self, movement):
        self._movement = movement


class MockPiCamera(object):

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

    def start_recording(self, *args):
        if hasattr(self, 'start_recording_args'):
            assert('Only support one call for now')
        self.start_recording_args = args

    def start_recording_called_once_with(self, *args):
        return self.start_recording_args == args

    def stop_recording(self, *args):
        if hasattr(self, 'stop_recording_args'):
            assert('Only support one call for now')
        self.stop_recording_args = args

    def stop_recording_called_once_with(self, *args):
        return self.stop_recording_args == args


class TestPuppyClips(unittest.TestCase):

    def setUp(self):
        MockMovementSensor.reset()
        MockPiCamera.reset()
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
        puppyclips.picamera.PiCamera = MockPiCamera
        self.pc._movementsensor.set_movement([False, True, False])
        self.pc.run(3)
        self.assertEqual(mock_time.get_mock_sleep_calls(), 4)
        self.assertEqual(mock_time.get_mock_sleep_times(), [1, 1, 60, 1])
        self.assertTrue(MockPiCamera.get_instances()[0].start_recording_called_once_with('TODO_FILENAME'))
        self.assertTrue(MockPiCamera.get_instances()[0].stop_recording_called_once_with())


    def test_clip_is_stored_with_end_timestamp(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()