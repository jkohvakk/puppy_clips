import unittest
import puppyclips
import mock_time
from mock import patch, Mock, call


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


class MockOs(object):

    remove_calls = []

    @classmethod
    def remove(cls, filename):
        cls.remove_calls.append(filename)


class TestPuppyClips(unittest.TestCase):

    def setUp(self):
        puppyclips.movementsensor.RPi = Mock()
        puppyclips.time = mock_time
        mock_time.reset()
        self.picamera_class_mock = Mock()
        puppyclips.picamera.PiCamera = self.picamera_class_mock
        self.pc = puppyclips.PuppyClips()
        self.picamera_class_mock.assert_called_with(framerate=20)
        self.picamera = self.picamera_class_mock.return_value

    @patch('puppyclips.movementsensor.MovementSensor.is_movement')
    def test_movement_sensor_is_polled_every_second(self, is_movement):
        is_movement.return_value = False
        self.pc.run(3)
        self.assertEqual(mock_time.get_mock_sleep_calls(), 3)
        self.assertEqual(mock_time.get_mock_sleep_times(), [1, 1, 1])
        is_movement.assert_called_with()
        self.assertEqual(3, is_movement.call_count)

    def get_movements(self):
        return self.movements.pop()

    def set_mock_movements(self, movements, mock_is_movement):
        self.movements = movements
        mock_is_movement.side_effect = self.get_movements

    @patch('puppyclips.subprocess')
    @patch('puppyclips.movementsensor.MovementSensor.is_movement')
    def test_if_movement_a_minute_clip_is_taken_with_name_based_on_current_datetime(self,
                                                                                    is_movement,
                                                                                    subprocess):
        puppyclips.os = MockOs
        self.set_mock_movements([False, True, False], is_movement)
        self.pc.run(3)
        self.assertEqual(mock_time.get_mock_sleep_calls(), 4)
        self.assertEqual(mock_time.get_mock_sleep_times(), [1, 1, 60, 1])
        self.picamera.start_recording.assert_called_once_with('2015.01.31-20:10.h264')
        self.picamera.stop_recording.assert_called_once_with()

    @patch('puppyclips.subprocess')
    @patch('puppyclips.movementsensor.MovementSensor.is_movement')
    def test_it_is_possible_to_set_max_clips(self, is_movement, subprocess):
        self.set_mock_movements([True, True, True], is_movement)
        self.pc.run(3, max_clips=2)
        expected_picamera_mock_calls = [call.start_recording('2015.01.31-20:10.h264'),
                                        call.stop_recording(),
                                        call.start_recording('2015.01.31-20:10.h264'),
                                        call.stop_recording()]
        self.assertEqual(expected_picamera_mock_calls, self.picamera.mock_calls)
        self.assertEqual(mock_time.get_mock_sleep_calls(), 4)

    @patch('puppyclips.subprocess')
    @patch('puppyclips.movementsensor.MovementSensor.is_movement')
    def test_clip_is_converted_from_h264_to_mp4(self, is_movement, subprocess):
        puppyclips.os = MockOs
        self.set_mock_movements([False, True, False], is_movement)
        self.pc.run(3)
        self.assertEqual(call(['MP4Box',
                               '-fps', '20',
                               '-add', '2015.01.31-20:10.h264',
                               '2015.01.31-20:10.mp4']), subprocess.call.mock_calls[0])
        self.assertEqual(MockOs.remove_calls[0], '2015.01.31-20:10.h264')

    @patch('puppyclips.subprocess')
    @patch('puppyclips.movementsensor.MovementSensor.is_movement')
    def test_clip_is_uploaded_to_dropbox(self, is_movement, subprocess):
        puppyclips.os = MockOs
        self.set_mock_movements([False, True, False], is_movement)
        self.pc.run(3)
        self.assertEqual(call(['/home/pi/Dropbox-Uploader/dropbox_uploader.sh',
                               'upload',
                               '2015.01.31-20:10.mp4',
                               '2015.01.31-20:10.mp4']),
                         subprocess.call.mock_calls[1])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()