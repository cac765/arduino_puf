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
import time

from utils.puf import PUF

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", 
                        type=str,
                        help="Communication port for PUF",
                        default="COM4")
    parser.add_argument("--baudrate", 
                        type=str,
                        help="Arduino Serial baud rate",
                        default="9600")
    parser.add_argument("--log",
                        type=str,  
                        help="Specify logging level for main program.",
                        default="INFO")
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
    puf = PUF(port=args.port, baudrate=args.baudrate)
    sram = puf.load_sram()
    logging.info(f"SRAM Loaded: \n{sram}")
    byte_str = puf.format_sram_as_str()
    logging.info(f"SRAM Byte Str: \n{byte_str}")

def test():
    pass

if __name__ == "__main__":
    main()
    #test()
    logging.info("DONE")
