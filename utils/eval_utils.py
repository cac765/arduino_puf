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

def calculate_hamming_distance(hex_key: str, hex_auth: str) -> int:
    """Calculates the hamming distance between two hex strings."""
    int_key = int(hex_key, 16)
    int_auth = int(hex_auth, 16)
    int_ham = int_key ^ int_auth
    return bin(int_ham).count("1")

def convert_hex_to_binary(hex_str: str) -> str:
    """Converts a hex string to padded binary string."""
    return bin(int(hex_str, 16))[2:].zfill(8)

def XOR(bin_1: str, bin_2: str) -> str:
    """XOR two binary strings and return the result."""
    pass
