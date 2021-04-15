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

    def __init__(self):
        """Constructor method."""
        self.sram = None

    def load_sram(self):
        """Load contents of SRAM PUF."""
        pass