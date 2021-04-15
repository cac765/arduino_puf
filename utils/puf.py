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
        self.sram_str = ""

    def challenge(self, addr: int) -> bytes:
        """Send challenge to PUF and get response byte."""
        try:
            return self.sram[addr]
        except IndexError:
            print(f"[ERROR]: Address {addr} out of range for challenge.")
            return None

    def format_sram_as_str(self):
        """Format the SRAM as a Hex string and store it."""
        byte_str = ""
        for index in range(0, self.length):
            byte = self.sram[index]
            byte = hex(byte)[2:].upper()
            byte_str += byte
        self.sram_str = byte_str

    def get_sram_bytes(self) -> bytes:
        """Get the raw SRAM as bytes."""
        return self.sram

    def get_sram_str(self) -> str:
        """Get the SRAM as a Hex string."""
        return self.sram_str

    def load_sram(self):
        """Load contents of SRAM PUF."""
        self.sram = self.device.read(self.length)
        self.format_sram_as_str()

    def save_sram(self, filename: str) -> bool:
        """Save the current SRAM state to file."""
        try:
            with open(filename, 'a') as file:
                file.write(self.sram_str + "\n")
            return True
        except:
            print("[ERROR]: Error writing SRAM to file.")
            return False
