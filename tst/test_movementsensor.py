import unittest
import movementsensor
import RPi


class MockGPIO(object):

    BCM = 'BCM'
    IN = 'IN'
    PUD_DOWN = 'PUD_DOWN'

    @classmethod
    def setmode(cls, *args):
        cls.setmode_args = args

    @classmethod
    def setmode_called_once_with(cls, *args):
        return cls.setmode_args == args

    @classmethod
    def setup(cls, *args):
        cls.setup_args = args

    @classmethod
    def setup_called_once_with(cls, *args):
        return cls.setup_args == args

    @classmethod
    def set_input_state(cls, state):
        cls.input_state = state

    @classmethod
    def input(cls, pin):
        return cls.input_state

class TestMovementSensor(unittest.TestCase):

    def setUp(self):
        movementsensor.RPi.GPIO = MockGPIO
        self.ms = movementsensor.MovementSensor()

    def test_constructor_initializes_GPIO(self):
        self.assertTrue(MockGPIO.setmode_called_once_with(RPi.GPIO.BCM))
        self.assertTrue(MockGPIO.setup_called_once_with(2, RPi.GPIO.IN, RPi.GPIO.PUD_DOWN))

    def test_is_movement_no_movement(self):
        MockGPIO.set_input_state(0)
        self.assertFalse(self.ms.is_movement())

    def test_is_movement_movement(self):
        MockGPIO.set_input_state(1)
        self.assertTrue(self.ms.is_movement())


if __name__ == "__main__":
    unittest.main()