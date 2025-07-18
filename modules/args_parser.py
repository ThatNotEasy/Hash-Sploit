import argparse

def get_args():
    parser = argparse.ArgumentParser(
        description="🔓 Smart Decoder & Hash Cracker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "-i", "--input", required=True,
        help="Input to process (hash or encoded string)"
    )
    
    parser.add_argument(
        "-w", "--wordlist",
        help="Path to wordlist file for hash cracking"
    )
    
    parser.add_argument(
        "-t", "--threads", type=int, default=4,
        help="Number of threads to use for cracking"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="File to save results"
    )
    
    return parser.parse_args()