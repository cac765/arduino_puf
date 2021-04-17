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
    parser.add_argument("--port", 
                        type=str,
                        help="Communication port for PUF",
                        default="COM4")
    parser.add_argument("--baudrate", 
                        type=str,
                        help="Arduino Serial baud rate",
                        default="9600")
    parser.add_argument("--length",
                        type=int,
                        help="Length in Bytes of SRAM PUF.",
                        default=2048)
    parser.add_argument("--log",
                        type=str,  
                        help="Specify logging level for main program.",
                        default="INFO")
    parser.add_argument("--save",
                        type=str,
                        help="Filename to save SRAM output to.",
                        default=None)
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
    puf = PUF(port=args.port, baudrate=args.baudrate, length=args.length)
    puf.load_sram()
    logging.debug(f"SRAM Loaded: \n{puf.sram}")
    logging.debug(f"SRAM Byte Str: \n{puf.sram_str}")

    if args.save is not None:
        if puf.save_sram(args.save):
            logging.debug(f"SRAM appended to file {args.save}.")
        else:
            logging.debug(f"Failed to save SRAM to file {args.save}.")


def test():
    pass

if __name__ == "__main__":
    main()
    #test()
    logging.info("DONE")
