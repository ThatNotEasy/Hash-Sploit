from modules.detection import HashDetector
from modules.crack import HashCracker
from modules.args_parser import get_args
from modules.logger import get_logger
from modules.banners import banners
import time
import sys
import os

logger = get_logger()

def load_wordlist(path: str) -> list:
    """Load and validate wordlist file."""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Wordlist not found at {path}")
        if os.path.getsize(path) == 0:
            raise ValueError("Wordlist file is empty")
            
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f if line.strip()]
            if not wordlist:
                raise ValueError("No valid passwords found in wordlist")
            return wordlist
            
    except Exception as e:
        logger.error(f"Wordlist error: {str(e)}")
        print(f"[!] Error: {str(e)}")
        return None

def print_progress(attempts: int, current_password: str, total: int):
    """Display progress of cracking attempt."""
    progress = (attempts / total) * 100
    sys.stdout.write(
        f"\r[⏳] Progress: {progress:.1f}% | "
        f"Attempts: {attempts:,}/{total:,} | "
        f"Current: {current_password[:20]}{'...' if len(current_password) > 20 else ''}"
    )
    sys.stdout.flush()

def display_hash_info(hash_str: str, hash_info: dict):
    """Display detailed information about the detected hash."""
    print(f"[🔍] Hash Analysis:\n")
    print(f" - Input: {hash_str}")
    print(f" - Algorithm: {hash_info.get('algorithm', 'Unknown')}")
    print(f" - Length: {hash_info.get('length', 'N/A')}")
    
    if variants := hash_info.get('variants'):
        print(f" - Possible Variants: {', '.join(variants)}")
    
    if hash_info['algorithm'] == 'bcrypt':
        print(" - Note: Bcrypt cracking will be significantly slower")

def main():
    try:
        # Initial setup
        banners()
        args = get_args()
        
        if not args.input:
            print("[!] Error: No hash input provided")
            return
            
        detector = HashDetector()
        cracker = HashCracker()
        start_time = time.time()

        # Step 1: Hash detection and analysis
        hash_info = detector.detect_hash_algorithm(args.input)
        display_hash_info(args.input, hash_info)

        # Step 2: Hash cracking
        if hash_info.get('algorithm') == 'Unknown':
            print("\n[❌] No known hash algorithm detected")
            return

        if not args.wordlist:
            print("\n[ℹ️] Wordlist not provided. Skipping cracking.")
            return

        wordlist = load_wordlist(args.wordlist)
        if not wordlist:
            return

        algorithm = hash_info.get('algorithm')
        if not cracker.set_algorithm(algorithm):
            print(f"\n[❌] Unsupported algorithm: {algorithm}")
            return

        print(f"\n[⚡] Starting cracking process:")
        print(f" - Algorithm: {algorithm}")
        print(f" - Wordlist: {args.wordlist} ({len(wordlist):,} passwords)")
        print(f" - Threads: {args.threads}\n")

        result = cracker.crack(
            hash_target=args.input,
            wordlist=wordlist,
            threads=args.threads,
            progress_callback=lambda a, p: print_progress(a, p, len(wordlist))
        )

        # Display results
        if result:
            print(f"\n[✅] SUCCESS: Password found - {result}")
            if args.output:
                try:
                    with open(args.output, 'a') as f:
                        f.write(f"{args.input}:{result}\n")
                    print(f"[📁] Results saved to: {args.output}")
                except IOError as e:
                    print(f"[!] Error saving results: {str(e)}")
        else:
            print("[❌] Password not found in wordlist")

    except KeyboardInterrupt:
        print("\n[⚠️] Process interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        print(f"[!] An error occurred: {str(e)}")
    finally:
        print(f"\n[⏱️] Total processing time: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()