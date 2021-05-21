# import RPi.GPIO as GPIO
import pigpio
from time import sleep


class FlameThrower:

    __WAIT = 0.5
    __CYCLES = {"cw": 2000, "center": 1500, "ccw": 1000}

    def __init__(self, fuel_pin: int, ignition_pin: int, assembly_pin: int):
        """Initiating FlameThrower class, the pins corespond to the raspberry pi's
        GPIO pins being used for the servo's logic line

        fuel_pin - logic input for fuel servo
        ignition_pin - logic input for ignition servo
        assembly_pin - logic input for lighter assembly servo
        """

        self.fuel_pin = fuel_pin
        self.ignition_pin = ignition_pin
        self.assembly_pin = assembly_pin

    def __enter__(self):
        """ Context manager enter method
        """

        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """ Context manager exit method
        """

        self.quit()

    def setup(self):
        """ Setup raspberry pi GPIO pins for servos and move servos to their
        off positions
        """

        self.pi = pigpio.pi()

        self.pi.set_mode(self.fuel_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.ignition_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.assembly_pin, pigpio.OUTPUT)

        # reset servos
        self.fuel_off()
        self.ignition_off()
        self.assembly_off()

    def fuel_on(self):
        """ Activate servo responsible for fuel spray
        """
        self.pi.set_servo_pulsewidth(self.fuel_pin, self.__CYCLES["ccw"])
        sleep(self.__WAIT)

    def fuel_off(self):
        """ Deactivate servo responsible for fuel spray
        """
        self.pi.set_servo_pulsewidth(self.fuel_pin, self.__CYCLES["cw"])
        sleep(self.__WAIT)

    def ignition_on(self):
        """ Activate servo responsible for ignition/lighter 
        """
        self.pi.set_servo_pulsewidth(self.ignition_pin, self.__CYCLES["cw"])
        sleep(self.__WAIT)

    def ignition_off(self):
        """ Deactivate servo responsible for ignition/lighter 
        """
        self.pi.set_servo_pulsewidth(self.ignition_pin, self.__CYCLES["center"])
        sleep(self.__WAIT)

    def assembly_on(self):
        """ Activate servo responsible for moving the lighter assembly infront
        of the fuel's path 
        """
        self.pi.set_servo_pulsewidth(self.assembly_pin, self.__CYCLES["ccw"])
        sleep(self.__WAIT)

    def assembly_off(self):
        """ Deactivate servo responsible for moving the lighter assembly infront
        of the fuel's path (move out of the fuel's path)
        """
        self.pi.set_servo_pulsewidth(self.assembly_pin, self.__CYCLES["center"])
        sleep(self.__WAIT)

    def quit(self):
        """ Reset servos back to starting position and release GPIO resources
        """

        self.fuel_off()
        self.ignition_off()
        self.assembly_off()

        self.pi.stop()
