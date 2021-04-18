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

from eval.eval_utils import Eval

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
    parser.add_argument("--output",
                        type=str,
                        help="Name of output file for mismatch errors.",
                        default="error_data.csv")
    parser.add_argument("--threshold",
                        type=int,
                        help="Mismatch threshold to filter from SRAM.",
                        default=3)
    return parser.parse_args()

def log_config(log_level: str):
    """Configures the logger."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid Log Level: {log_level}")
    logging.basicConfig(level=numeric_level, 
        format="%(levelname)s: %(message)s")

def main():
    # Parse args, get log, create evaluator
    args = parse_args()
    log_config(args.log)
    evaluate = Eval()

    # Get hex string data from SRAM Files
    sram_key = Eval.load_data_from_file(args.key_file)[0]
    sram_auth = Eval.load_data_from_file(args.auth_file)
    if sram_key is None or sram_auth is None:
        exit(1)
    
    # Evaluate hamming distances and average bit error rate
    if len(sram_auth) > 0:
        avg_ber = Eval.calculate_avg_ber(sram_key, sram_auth, log=logging)

    # Track mismatched bytes and occurrences
    evaluate.track_total_mismatch(sram_key, sram_auth)
    total_mismatch = evaluate.get_total_mismatch()
    logging.debug(f"Total bit errors: {len(total_mismatch)}")

    # Save mismatches to CSV
    evaluate.export_to_csv(args.output)
    logging.info(f"Error data saved to {args.output}.")

    # Filter mismatched bytes from sram data
    logging.info(f"Filtering byte errors with threshold {args.threshold}...")
    sram_key_filtered = evaluate.filter_hex_mismatch(sram_key, args.threshold)
    logging.debug(f"Length of filtered key: {len(sram_key_filtered)}")
    sram_auth_filtered = []
    for auth in sram_auth:
        auth_filtered = evaluate.filter_hex_mismatch(auth, args.threshold)
        sram_auth_filtered.append(auth_filtered)

    # Calculate new average Bit Error Rate
    new_avg_ber = evaluate.calculate_avg_ber(sram_key_filtered, 
                                             sram_auth_filtered,
                                             log=logging)

    # Save filtered SRAM data to file
    Eval.save_data_to_file([sram_key_filtered], 
                            "sram_key_filtered.txt")
    Eval.save_data_to_file(sram_auth_filtered, 
                            "sram_auth_filtered.txt")


if __name__ == "__main__":
    main()
    logging.info("DONE")