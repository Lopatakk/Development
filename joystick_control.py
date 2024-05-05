from gamesetup import *


class Joystick:

    def __init__(self):
        GameSetup.setup_controller()

        self.active = False
        self.left_joystick = (0, 0)
        self.right_joystick = (0, 0)
        self.cross_button = False
        self.position = None

    def update(self):
        for joystick in GameSetup.joysticks:
            # control
            self.left_joystick = (joystick.get_axis(0), joystick.get_axis(1))
            self.right_joystick = (joystick.get_axis(2), joystick.get_axis(3))
            if abs(self.left_joystick[0]) >= 0.02:
                self.active = True

            self.cross_button = joystick.get_button(0)

    def switch_on(self, state):
        self.active = state
        if state:
            self.position = 0
        else:
            self.position = None
