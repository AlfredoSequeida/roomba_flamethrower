from Controller import Controller
from FlameThrower import FlameThrower
from Roomba import Roomba

from time import sleep


def get_controller(roomba) -> Controller:
    """Wait for controller to connect and return a Controller instance once the
    controller has been connected
    """

    controller = None

    while not controller:
        try:
            controller = Controller()
            roomba.play_ready_sound()
            print("ready")
        except:
            print("Waiting for controller . . .")
            roomba.play_waiting_sound()
            sleep(3)

    return controller


def get_trig_val(abs_val: int, max_unit: int, abs_limit: int) -> int:
    """Get the corresponding trigger value to a specific limit. This evenly
    devides the value so that the more you press the trigger, the higher the
    output value.

    abs_val - The current trigger value
    max_unit - The maximum value to remap the trigger value
    abs_limit - The maximum range of the trigger
    """

    inc = abs_limit / max_unit
    return int(abs_val / inc)


def get_unsigned_js_val(abs_val: int, max_unit: int, abs_limit: int) -> int:
    """Get unsigned remaped joystick value in reverse range
    (For example if the limit is 2000, and the input valueis also 2000,
    the value returned will be 1. And with the same limit, if the input value
    is 1, the output value wwill be 2000. The same applies to the values in
    between). This evenly devides the value so that the maximum js range is
    remapped to a value in the range of the
    specified limit.

    abs_val - The current joystick value
    max_unit - The maximum value to remap the joystick value
    abs_limit - The maximum range of the joystick
    """

    inc = abs_limit / max_unit

    # ignoring signs to keep results positive
    if abs_val > 0:
        abs_val *= -1

    val = int((abs_val / inc) + max_unit)

    # if the value is zero, return 1 (maximum range)
    if val == 0:
        val = 1

    return val


def main():

    fuel_pin = 17
    ignition_pin = 27
    assembly_pin = 22

    roomba_serial = "/dev/ttyUSB0"

    with Roomba(roomba_serial) as roomba, FlameThrower(
        fuel_pin, ignition_pin, assembly_pin
    ) as flame_thrower:
        controller = get_controller(roomba)

        # turning radius in mm
        rad = 0
        # driving direction, negative = backwards, positive = forwards
        rot = 0
        # driving velocity in mm/s
        vel = 0

        for button, val in controller.get_input():

            update = False

            # use right trigger to drive forward
            if button == "RT":
                vel = get_trig_val(val, Roomba.MAX_VEL, controller.TRIG_MAX_RANGE)
                rot = 1
                update = True

            # use left trigger to drive backward (reverse)
            if button == "LT":
                vel = get_trig_val(val, Roomba.MAX_VEL, controller.TRIG_MAX_RANGE)
                rot = -1
                update = True

            # use the left joystick to turn
            if button == "LSX":
                rad = get_unsigned_js_val(val, Roomba.MAX_RAD, controller.JS_CENTER)

                if val > 0:
                    rad *= -1

                update = True

            # send new command to romba
            if update:
                roomba.drive(vel * rot, rad)

            # use left bumper to spray fuel.
            # Pressed = spay, Stop pressing = stop spraying
            if button == "LB":
                if val == 1:
                    flame_thrower.fuel_on()
                else:
                    flame_thrower.fuel_off()

            # use x button to move ignition source in the fuel's path and
            # turn on the ignition source.
            # Press to enable, let go to disable
            if button == "X":
                if val == 1:
                    flame_thrower.assembly_on()
                    flame_thrower.ignition_on()
                else:
                    flame_thrower.assembly_off()
                    flame_thrower.ignition_off()


if __name__ == "__main__":
    main()
