from gamesetup import *


class Joystick:

    def __init__(self):
        GameSetup.setup_controller()

        self.active = False
        self.position = (0, 0)
        self.vertical_direction = 0
        self.horizontal_direction = 0
        self.sliding = False
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
        self.options_button = False
        self.options_button_pressed = False
        self.arrow_up = False
        self.arrow_down = False
        self.arrow_left = False
        self.arrow_right = False

    def set_position(self, horizontal, vertical):
        self.position = (horizontal, vertical)

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

    def menu_control(self, max_horizontals, max_verticals):
        if not self.sliding:

            horizontal_position = self.position[0]
            vertical_position = self.position[1]

            #   button movement
            # vertical
            if self.left_joystick[1] > 0.5 or self.arrow_down:
                self.vertical_direction = 1
            if self.left_joystick[1] < -0.5 or self.arrow_up:
                self.vertical_direction = -1
            if -0.5 <= self.left_joystick[1] <= 0.5 and not self.arrow_up and not self.arrow_down:
                vertical_position += self.vertical_direction
                if vertical_position >= max_verticals:
                    vertical_position = 0
                if vertical_position <= -1:
                    vertical_position = max_verticals - 1

                self.vertical_direction = 0

            # horizontal
            if self.left_joystick[0] > 0.5 or self.arrow_right:
                self.horizontal_direction = 1
            if self.left_joystick[0] < -0.5 or self.arrow_left:
                self.horizontal_direction = -1
            if -0.5 <= self.left_joystick[0] <= 0.5 and not self.arrow_left and not self.arrow_right:
                horizontal_position += self.horizontal_direction
                if horizontal_position >= max_horizontals:
                    horizontal_position = 0
                if horizontal_position <= -1:
                    horizontal_position = max_horizontals - 1

                self.horizontal_direction = 0
            self.position = (horizontal_position, vertical_position)

            return self.control_buttons()
        return True

    def control_buttons(self):
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
            self.options_button_pressed = True
        if not self.options_button and self.options_button_pressed:
            self.options_button_pressed = False
            return 'settings'
