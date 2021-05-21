from evdev import InputDevice, list_devices, ecodes


class Controller:

    # xbox one controller joystick max range (negative + positive range)
    JS_MAX_RANGE = 65534

    # xbox one controller joystick center range 
    JS_CENTER = JS_MAX_RANGE / 2

    # xbox one controller trigger max range (pressed in all of the way)
    TRIG_MAX_RANGE = 1023

    # button mappings for xbox one controller
    BUTTONS = {
        0: "LSX",
        1: "LSY",
        2: "RSV",
        4: "SCAN",
        5: "RSH",
        9: "RT",
        10: "LT",
        16: "DPADHOR",
        17: "DPADVERT",
        158: "OPTION",
        172: "HOME",
        304: "A",
        305: "B",
        308: "Y",
        307: "X",
        310: "LB",
        311: "UNK",
        315: "START",
        317: "LSB",
        318: "RSB",
    }

    def __init__(self):
        self.controller = InputDevice(list_devices()[0])

    def get_input(self) -> list:
        """
        Get contoller input from linux input devices.
        """
        for e in self.controller.read_loop():

            key_code = e.code
            button = self.BUTTONS[key_code]

            if e.type == ecodes.EV_KEY:
                val = e.value
                yield (button, val)

            # for abs values (joystick, triggers)
            if e.type == ecodes.EV_ABS:
                val = e.value
                button = self.BUTTONS[key_code]

                # getting left joystick x-axis values (used for turning)
                if button == "LSX":
                    # Splitting maximum joystick range into postive and negative
                    # values. Negative = left, Positive = right
                    val = val - self.JS_CENTER

                yield (button, val)
