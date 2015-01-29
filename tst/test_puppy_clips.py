import unittest
import puppyclips


mock_sleep_calls = 0
mock_sleep_times = []


class MockMovementSensor(object):

    instances = []

    @classmethod
    def get_instances(cls):
        return cls.instances

    def __init__(self):
        self.__class__.instances.append(self)
        self._calls = []

    def is_movement(self):
        self._calls.append('is_movement')

    def get_calls(self):
        return self._calls


def get_mock_sleep_calls():
    return mock_sleep_calls


def get_mock_sleep_times():
    return mock_sleep_times


def mock_sleep(time):
    global mock_sleep_calls
    mock_sleep_calls += 1
    mock_sleep_times.append(time)


class TestPuppyClips(unittest.TestCase):


    def test_movement_sensor_is_polled_every_second(self):
        puppyclips.movementsensor.MovementSensor = MockMovementSensor
        puppyclips.time.sleep = mock_sleep
        pc = puppyclips.PuppyClips()
        pc.run(3)
        self.assertEqual(get_mock_sleep_calls(), 3)
        self.assertEqual(get_mock_sleep_times(), [1, 1, 1])
        self.assertEqual(MockMovementSensor.get_instances()[0].get_calls(),
                         ['is_movement', 'is_movement', 'is_movement'])

    def test_if_movement_under_5_secs_1_min_clip_is_taken(self):
        pass

    def test_clip_is_stored_with_end_timestamp(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()