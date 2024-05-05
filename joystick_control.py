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
        self.L2 = 0
        self.R2 = 0

        # buttons
        self.cross_button = False
        self.cross_button_pressed = False
        self.circle_button = False
        self.circle_button_pressed = False
        self.square_button = False
        self.square_button_pressed = False
        self.triangle_button = False
        self.triangle_button_pressed = False
        self.arrow_up = False
        self.arrow_down = False
        self.arrow_left = False
        self.arrow_right = False
        self.options_button = False

    def update(self):
        for joystick in GameSetup.joysticks:
            # control
            # joysticks
            self.left_joystick = (joystick.get_axis(0), joystick.get_axis(1))
            self.right_joystick = (joystick.get_axis(2), joystick.get_axis(3))

            # L2/R2
            self.L2 = joystick.get_axis(4)
            self.R2 = joystick.get_axis(5)

            # buttons
            self.cross_button = joystick.get_button(0)
            self.circle_button = joystick.get_button(1)
            self.options_button = joystick.get_button(6)
            self.arrow_up = joystick.get_button(11)
            self.arrow_down = joystick.get_button(12)
            self.arrow_left = joystick.get_button(13)
            self.arrow_right = joystick.get_button(14)

            # active
            for i in range(16):
                if joystick.get_button(i):
                    self.active = True
                    break
            if (abs(self.left_joystick[0]) >= 0.1 or abs(self.left_joystick[1]) >= 0.1 or
                    abs(self.right_joystick[0]) >= 0.1 or abs(self.right_joystick[1]) >= 0.1 or self.L2 > -1 or self.R2 > -1):
                self.active = True

    def menu_control(self, buttons_num, axis='horizontal'):
        if self.circle_button:
            self.circle_button_pressed = True
        if not self.circle_button and self.circle_button_pressed:
            self.circle_button_pressed = False
            return 'exit'

        if self.cross_button:
            self.cross_button_pressed = True
        if not self.cross_button and self.cross_button_pressed:
            self.cross_button_pressed = False
            return 'enter'

        if self.options_button:
            return 'settings'

        # button movement
        if axis == 'horizontal':
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

        if axis == 'vertical':
            if self.left_joystick[0] > 0.2 or self.arrow_right:
                self.direction = 1
            if self.left_joystick[0] < -0.2 or self.arrow_left:
                self.direction = -1
            if -0.2 <= self.left_joystick[0] <= 0.2 and not self.arrow_left and not self.arrow_right:
                self.position += self.direction
                if self.position >= buttons_num:
                    self.position = 0
                if self.position <= -1:
                    self.position = buttons_num - 1

                self.direction = 0
        return True
