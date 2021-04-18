######## Demo Script for SRAM PUF Key Generation ########
#
# Author: Corey Cline
#
# Date: 04/18/21
#
# Description:
# Demonstration Script that allows a user to access the SRAM PUF and filter the
# output to generate a cryptographic key of a variable length. Using filtered 
# key files is optional, and the program will output the generated key as well
# as the Hamming Distance when compared to the original or filtered key that
# would be encapsulated by the server. 
#
###############################################################################
import argparse
import logging
import random

from client.puf import PUF
from eval.eval import Eval

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log",
                        type=str,  
                        help="Specify logging level for main program.",
                        default="INFO")
    parser.add_argument("--error-file",
                        type=str,
                        help="filename of the mismatch .csv file.",
                        default="error_data.csv")
    parser.add_argument("--threshold",
                        type=int,
                        help="Mismatch threshold to filter from SRAM.",
                        default=2)
    parser.add_argument("--key-file",
                        type=str,
                        help="filename of the SRAM Key file.",
                        default="sram_key.txt")
    parser.add_argument("--port",
                        type=str,
                        help="USB communication port for the SRAM PUF.",
                        default="COM4")
    parser.add_argument("--baudrate", 
                        type=str,
                        help="Arduino Serial baud rate",
                        default="115200")
    parser.add_argument("--length",
                        type=int,
                        help="Length in Bytes of SRAM PUF.",
                        default=2048)
    return parser.parse_args()

def log_config(log_level: str):
    """Configures the logger."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid Log Level: {log_level}")
    logging.basicConfig(level=numeric_level, 
        format="%(levelname)s: %(message)s")

def main():
    # Parse args, set logger, create PUF and evaluator objects
    args = parse_args()
    log_config(args.log)
    evaluate = Eval()
    puf = PUF(port=args.port, baudrate=args.baudrate, length=args.length)

    sram_key = Eval.load_data_from_file(args.key_file)[0]
    puf.load_sram()
    sram_auth = puf.get_sram_str()

    if evaluate.load_mismatch_from_csv(args.error_file):
        sram_key_filtered = evaluate.filter_hex_mismatch(sram_key, 
            args.threshold)
        sram_auth_filtered = evaluate.filter_hex_mismatch(sram_auth,
            args.threshold)
        
        key_length = int(input("Enter length of cryptographic key in bytes: "))
        max_address = len(sram_key_filtered) - key_length - 1
        address = random.randint(0, max_address)

        sram_partial_key = sram_key_filtered[address : address + key_length]
        sram_partial_auth = sram_auth_filtered[address : address + key_length]
        logging.info(f"Cryptographic key generated: {sram_partial_auth}")

        if sram_partial_key == sram_partial_auth:
            logging.info("[SUCCESS]: Key Authenticted!")
        else:
            logging.info("[ERROR]: Key contained errors.")
            logging.info(f"Client Key: {sram_partial_auth}")
            logging.info(f"Server Key: {sram_partial_key}")
            ham_dist = Eval.calculate_hamming_distance(sram_partial_key,
                sram_partial_auth)
            logging.info(f"Hamming Distance: {ham_dist}")

        ber = Eval.calculate_avg_ber(sram_partial_key, 
            [sram_partial_auth],
            log=logging)     


if __name__ == "__main__":
    main()
    logging.info("DONE")
                          