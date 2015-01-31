import RPi


class MovementSensor(object):

    def __init__(self):
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(2, RPi.GPIO.IN, RPi.GPIO.PUD_DOWN)

    def is_movement(self):
        return RPi.GPIO.input(2)

