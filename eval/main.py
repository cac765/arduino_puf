######## Main Evaluation Script ########
#
# Author: Corey Cline
#
# Date: 04/16/21
#
# Description:
# Main driver class for evaluation of the SRAM PUF. Accepts arguments that
# point to a filename for a single iteration of stored SRAM data to be used as
# the reference, as well as a filename for the several iterations of SRAM data 
# to be checked against the reference. The hamming distance will be calculated
# and the overall Bit Error Rate (BER) will be found for the SRAM PUF. 
#
###############################################################################
import argparse
import logging

from utils.eval_utils import calculate_hamming_distance

def parse_args():
    """Parses program optional arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log",
                        type=str,  
                        help="Specify logging level for main program.",
                        default="INFO")
    parser.add_argument("--key-file",
                        type=str,
                        help="Name of the key file for SRAM authentication.",
                        default="sram_key.txt")
    parser.add_argument("--auth-file",
                        type=str,
                        help="Name of the SRAM data file to authenticate.",
                        default="sram_auth.txt")
    return parser.parse_args()

def log_config(log_level: str):
    """Configures the logger."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid Log Level: {log_level}")
    logging.basicConfig(level=numeric_level, 
        format="%(levelname)s: %(message)s")

def main():
    args = parse_args()
    log_config(args.log)
    try:
        with open(args.key_file, "r") as file:
            sram_key = file.readlines()[0]
        with open(args.auth_file, "r") as file:
            sram_auth = file.readlines()
    
    except FileNotFoundError as fnfe:
        logging.error(fnfe)
        logging.info(f"Bad filename. Exiting...")
        exit(1)

    except Exception as err:
        logging.error(err)
        logging.info(f"Error parsing keys. Exiting...")
        exit(1)

    if len(sram_auth) > 0:
        total_ham_dist = 0
        for auth in sram_auth:
            ham_dist = calculate_hamming_distance(sram_key, auth)
            total_ham_dist += ham_dist
            logging.debug(f"Hamming Distance: {ham_dist}")
        
        avg_ham_dist = total_ham_dist / len(sram_auth)
        logging.debug(f"Average Hamming Distance: {avg_ham_dist}")

        avg_ber = avg_ham_dist / len(sram_key * 8) * 100
        logging.debug(f"Average Bit Error Rate (BER): %0.2f%%", avg_ber)

def test():
    print(calculate_hamming_distance("1A", "1B"))


if __name__ == "__main__":
    main()
    #test()
    logging.info("DONE")