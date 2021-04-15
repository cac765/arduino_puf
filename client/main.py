######## Client Main Script ########
#
# Author: Corey Cline
#
# Date: 04/15/21
#
# Description:
# Main server script for client interaction with an Arduino-based SRAM PUF.
#
###############################################################################
import argparse
import logging

from utils.puf import PUF

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", type=str, default="INFO", 
        help="Specify logging level for main program.")
    return parser.parse_args()

def log_config(log_level):
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid Log Level: {log_level}")
    logging.basicConfig(level=numeric_level, 
        format="%(levelname)s: %(message)s")

def main():
    args = parse_args()
    log_config(args.log)
    print("Hello world")
    pass

if __name__ == "__main__":
    main()
