from serial import Serial
from time import sleep


class Roomba:

    COMMANDS = {
        "start": 128,
        "reset": 7,
        "stop": 173,
        "drive": 137,
        "drive_direct": 145,
        "song": 140,
        "play": 141
    }

    MODES = {"safe": 131, "full": 132}
    BAUD = 115200

    # maximum and minimum driving velocities in mm/s
    MAX_VEL = 500
    MIN_VEL = -500

    # maximum and minimum turn radii in mm
    MAX_RAD = 2000
    MIN_RAD = -2000

    def __init__(self, port: str, mode: str = "safe"):
        """Initialize Roomba instance
        port - The serial port to communicate with the roomba.
        mode - The mode to operate the roomba in. Defaults to safe mode.
        """

        self.port = port
        self.mode = mode

    def __enter__(self):
        """Context manager enter method"""

        self.setup()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Context manager exit method"""

        self.quit()

    def _write(self, data: list):
        """Write to serial
        data - List of data to write
        """

        self.serial.write(bytes(data))

    def _split_16_bits_to_2_bytes(self, bits: int) -> tuple:
        """Split 16 bts into two bytes, returns tutple with bytes split into
        high and low bytes respectively, ex: (high_byte, low_byte).

        bits: 16 bit integer to split into two bytes
        """

        # using bitwise AND operator to mask 8 bits with 255
        return ((bits >> 8) & 0xFF, bits & 0xFF)

    def _twos_compliment(self, val: int, bits: int) -> int:
        """calculate two's compliment using a specified number of bits and
        return as an integer

        val: the value to take the two's compliment
        bits: the number of bits appropriate for the value
        """

        # if the value is positive (or zero), there is no need
        # to apply twos compliment, we only need it for negative values

        comp = 0

        if val >= 0:
            comp = val

        else:
            # applying twos compiment by shiting 1 number of bits to the left
            # and adding the value to take the compliment
            comp = (1 << bits) + val

        return comp

    def setup(self):
        """Setup roomba interface by starting serial connection in the
        instance's specified mode.
        """

        self.serial = Serial(port=self.port, baudrate=self.BAUD)
        self._write([self.COMMANDS["start"], self.MODES[self.mode]])

        # sleep before sending other commands
        sleep(1)

    def quit(self):
        """Return roomba to safe mode to avoid battery draining and release
        serial resources
        """

        self._write([self.COMMANDS["stop"], self.MODES["safe"]])
        self.serial.close()

    def drive(self, vel: int, rad: int):
        """drive
        vel: the velocity to drive in mm/s
        rad: the turn radius in mm
        """

        vel_high_byte, vel_low_byte = self._split_16_bits_to_2_bytes(
            self._twos_compliment(vel, 16)
        )
        rad_high_byte, rad_low_byte = self._split_16_bits_to_2_bytes(
            self._twos_compliment(rad, 16)
        )

        self._write(
            [
                self.COMMANDS["drive"],
                vel_high_byte,
                vel_low_byte,
                rad_high_byte,
                rad_low_byte,
            ]
        )

    def drive_direct(self, vel: int):
        """Control ecah wheel independently
        vel: the velocity to drive in mm/s
        """

        r_vel_high_byte, r_vel_low_byte = self._split_16_bits_to_2_bytes(
            self._twos_compliment(vel, 16)
        )
        l_vel_high_byte, l_vel_low_byte = self._split_16_bits_to_2_bytes(
            self._twos_compliment(vel, 16)
        )

        self._write(
            [
                self.COMMANDS["drive_direct"],
                r_vel_high_byte,
                r_vel_low_byte,
                l_vel_high_byte,
                l_vel_low_byte,
            ]
        )

    def que_song(self, song_number:int, notes_list:list):
        song = [self.COMMANDS["song"], song_number, len(notes_list)] 

        for note, note_length in notes_list:
            song.append(note)
            song.append(note_length)

        self._write(song)

    def play_song(self, song_number:int):
        self._write([self.COMMANDS["play"], song_number])

    def play_waiting_sound(self):
        c_note = 60
        note_length = 32
        song_number = 0

        self.que_song(song_number, [(c_note, note_length)])
        self.play_song(song_number)

    def play_ready_sound(self):
        g_note = 67
        note_length = 64 
        song_number = 0

        self.que_song(song_number, [(g_note, note_length)])
        self.play_song(song_number)

