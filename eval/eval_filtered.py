import logging
from eval import Eval

evaluate = Eval()
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)

# Get hex string data from SRAM Files
sram_key = Eval.load_data_from_file("sram_key.txt")[0]
sram_auth = Eval.load_data_from_file("sram_auth_new.txt")
if sram_key is None or sram_auth is None:
    exit(1)

# Load mismatch data from .csv
if evaluate.load_mismatch_from_csv("error_data.csv"):
    sram_key_filtered = evaluate.filter_hex_mismatch(sram_key, 1)
    sram_auth_filtered = []

    for auth in sram_auth:
        auth_filtered = evaluate.filter_hex_mismatch(auth, 1)
        sram_auth_filtered.append(auth_filtered)

    # Calculate new average Bit Error Rate
    new_avg_ber = evaluate.calculate_avg_ber(sram_key_filtered, 
                                             sram_auth_filtered,
                                             log=logging)

    # Track filtered mismatched bytes and occurrences
    evaluate.track_total_mismatch(sram_key_filtered, sram_auth_filtered)
    total_mismatch_filtered = evaluate.get_total_mismatch()
    logging.debug(f"Total bit errors: {len(total_mismatch_filtered)}")

    # Save filtered mismatches to CSV
    evaluate.export_to_csv("error_data_filtered.csv")
    logging.info(f"Error data saved to {'error_data_filtered.csv'}.")

logging.info("DONE")
