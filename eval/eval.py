######## Client Main Script ########
#
# Author: Corey Cline
#
# Date: 04/16/21
#
# Description:
# Eval Class and utility functions to help the evaluation main script 
# calculate Hamming Distance and Bit Error Rate (BER) for SRAM PUF.
#
###############################################################################
import pandas as pd

"""Eval Class to hold evaluation data and utility functions."""

class Eval:

    def __init__(self):
        self.total_mismatch = {}

    @staticmethod
    def calculate_avg_ber(sram_key: str, sram_auth: list, log=None) -> float:
        """Calculates average bit error rate from key and list of auths."""
        total_ham_dist = 0
        for auth in sram_auth:
            ham_dist = Eval.calculate_hamming_distance(sram_key, auth)
            total_ham_dist += ham_dist
            if log is not None:
                log.debug(f"Hamming Distance: {ham_dist}")
        
        avg_ham_dist = total_ham_dist / len(sram_auth)
        avg_ber = avg_ham_dist / len(sram_key * 8) * 100
        
        if log is not None:
            log.debug(f"Average Hamming Distance: {avg_ham_dist}")
            log.info(f"Average Bit Error Rate (BER): %0.2f%%", avg_ber)
        return avg_ber

    @staticmethod
    def calculate_hamming_distance(hex_key: str, hex_auth: str) -> int:
        """Calculates the hamming distance between two hex strings."""
        int_key = int(hex_key, 16)
        int_auth = int(hex_auth, 16)
        int_ham = int_key ^ int_auth
        return bin(int_ham).count("1")

    @staticmethod
    def convert_hex_to_binary(hex_str: str) -> str:
        """Converts a hex string to padded binary string."""
        return bin(int(hex_str, 16))[2:].zfill(8)

    @staticmethod
    def load_data_from_file(filename: str) -> list:
        """Loads hex string lines from SRAM file."""
        try:
            with open(filename, "r") as file:
                return file.readlines()
        
        except FileNotFoundError as fnfe:
            logging.error(fnfe)
            print("Bad filename.")

        except Exception as err:
            logging.error(err)
            print("Error parsing keys.")

        return None

    @staticmethod
    def save_data_to_file(data: list, filename: str) -> bool:
        """Save SRAM data to a text file."""
        try:
            with open(filename, "w") as file:
                for line in data:
                    file.write(line)
            return True

        except Exception as err:
            print("Error parsing data.")
            return False

    def get_total_mismatch(self):
        """Get the total mismatch dictionary."""
        return self.total_mismatch

    def export_to_csv(self, filename: str):
        """Export the total mismatches to .csv file."""
        out_data = pd.DataFrame.from_dict(self.total_mismatch, 
            orient="index",
            columns=["frequency"])
        out_data.to_csv(filename)

    def filter_hex_mismatch(self, hex_str: str, threshold: int) -> str:
        """Remove the mismatch chars from hex string based on occurrences."""
        new_hex = hex_str
        for key in self.total_mismatch:
            if self.total_mismatch[key] >= threshold:
                new_hex = new_hex[:key] + "X" + new_hex[key+1:]
        new_hex = new_hex.translate({ord("X") : None})
        return new_hex

    def track_single_mismatch(self, hex_1: str, hex_2: str) -> list:
        """XOR two hex strings and track the locations of mismatched chars."""
        mismatches = []
        for index in range(0, len(hex_1)):
            if hex_1[index] != hex_2[index]:
                mismatches.append(index)
        return mismatches

    def track_total_mismatch(self, key: str, auth_list: list):
        """Track the total occurrences of mismatches from the key."""
        self.total_mismatch = {}
        for auth in auth_list:
            mismatches = self.track_single_mismatch(key, auth)
            # iterate through list of single mismatch case
            for mismatch in mismatches:
                # check if the index exists as a key in the dictionary
                if mismatch in self.total_mismatch:
                    # add one to the key's value
                    self.total_mismatch[mismatch] += 1
                # first occurrence, create a new key with the value 1
                else:
                    self.total_mismatch[mismatch] = 1
