from gamesetup import *


class Joystick:

    def __init__(self):
        GameSetup.setup_controller()

        self.active = False
        self.position = 0
        self.direction = 0

        # joysticks
        self.left_joystick = (0, 0)
        self.right_joystick = (0, 0)

        # buttons
        self.cross_button = False
        self.circle_button = False
        self.square_button = False
        self.triangle_button = False
        self.arrow_up = False
        self.arrow_down = False
        self.arrow_left = False
        self.arrow_right = False
        self.options_button = False


    def update(self):
        for joystick in GameSetup.joysticks:
            # control
            self.left_joystick = (joystick.get_axis(0), joystick.get_axis(1))
            self.right_joystick = (joystick.get_axis(2), joystick.get_axis(3))
            if abs(self.left_joystick[0]) >= 0.02:
                self.active = True

            self.cross_button = joystick.get_button(0)
            self.circle_button = joystick.get_button(1)
            self.options_button = joystick.get_button(6)
            self.arrow_up = joystick.get_button(11)
            self.arrow_down = joystick.get_button(12)
            self.arrow_left = joystick.get_button(13)
            self.arrow_right = joystick.get_button(14)

    def menu_control(self, buttons_num):
        if self.circle_button:
            return False
        if self.options_button:
            return 'settings'

        if self.left_joystick[1] > 0.2 or self.arrow_down:
            self.direction = 1
        if self.left_joystick[1] < -0.2 or self.arrow_up:
            self.direction = -1
        if -0.2 <= self.left_joystick[1] <= 0.2 and not self.arrow_up and not self.arrow_down:
            self.position += self.direction
            if self.position >= buttons_num:
                self.position = 0
            if self.position <= -1:
                self.position = buttons_num - 1

            self.direction = 0
        return True
