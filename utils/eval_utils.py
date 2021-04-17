######## Client Main Script ########
#
# Author: Corey Cline
#
# Date: 04/16/21
#
# Description:
# Utility functions to help the evaluation main script calculate Hamming 
# Distance and Bit Error Rate (BER) for SRAM PUF.
#
###############################################################################


class Eval:

    def __init__(self):
        self.total_mismatch = {}

    def calculate_hamming_distance(hex_key: str, hex_auth: str) -> int:
        """Calculates the hamming distance between two hex strings."""
        int_key = int(hex_key, 16)
        int_auth = int(hex_auth, 16)
        int_ham = int_key ^ int_auth
        return bin(int_ham).count("1")

    def convert_hex_to_binary(hex_str: str) -> str:
        """Converts a hex string to padded binary string."""
        return bin(int(hex_str, 16))[2:].zfill(8)

    def track_single_mismatch(hex_1: str, hex_2: str) -> list:
        """XOR two hex strings and track the locations of mismatched chars."""
        # iterate through length of strings

            # if chars are not equal

                # add index to a list

        # return list of indices of mismatched chars
        pass

    def track_total_mismatch(mismatches: list):
        """Track the total occurrences of mismatches from the key."""
        # iterate through list of single mismatch case

            # check if the index exists as a key in the dictionary

                # add one to the key's value

            # first occurrence, create a new key with the value 1
        pass
