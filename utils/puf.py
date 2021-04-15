######## PUF Interface Utilities ########
#
# Author: Corey Cline
#
# Date: 04/15/21
#
# Description:
# A PUF Class to interface with the Arduino-based SRAM PUF. Includes
# basic utilities to read information from the PUF.
#
###############################################################################
import serial

"""PUF Class to interface and communicate with PUF."""


class PUF:

    def __init__(self, port="COM4", baudrate=9600, length=2048):
        """Constructor method."""
        self.device = serial.Serial(port=port, baudrate=baudrate)
        self.length = length
        self.sram = None

    def load_sram(self) -> bytes:
        """Load contents of SRAM PUF."""
        self.sram = self.device.read(self.length)
        return self.sram

    def format_sram_as_str(self) -> str:
        """Format the SRAM as a Hex string."""
        byte_str = ""
        for index in range(0, self.length):
            byte = self.sram[index]
            byte = hex(byte)[2:].upper()
            byte_str += byte
        return byte_str

        



