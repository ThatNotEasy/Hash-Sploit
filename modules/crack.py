import hashlib
import threading
from typing import List, Optional, Callable
import bcrypt

class HashCracker:
    def __init__(self):
        self.found = False
        self.result = None
        self.lock = threading.Lock()
        self.attempts = 0
        self.hash_func = None

    def set_algorithm(self, algorithm: str) -> bool:
        algo_map = {
            'MD5': lambda x: hashlib.md5(x.encode()).hexdigest(),
            'SHA-1': lambda x: hashlib.sha1(x.encode()).hexdigest(),
            'SHA-256': lambda x: hashlib.sha256(x.encode()).hexdigest(),
            'SHA-512': lambda x: hashlib.sha512(x.encode()).hexdigest(),
            'bcrypt': lambda x, target: bcrypt.checkpw(x.encode(), target.encode()),
            'MD5-crypt': None  # Still not implemented
        }
        
        # Normalize algorithm name
        algorithm = algorithm.upper().replace('_', '-').split(' ')[0]
        self.hash_func = algo_map.get(algorithm)
        
        if self.hash_func is None:
            print(f"[⚠️] Note: {algorithm} requires special handling not implemented in this version")
        
        return self.hash_func is not None

    def worker(self, hash_target: str, chunk: List[str], progress_callback: Callable = None):
        if not self.hash_func:
            return

        for password in chunk:
            if self.found:
                return

            password = password.strip()
            with self.lock:
                self.attempts += 1
                if progress_callback:
                    progress_callback(self.attempts, password)

            try:
                if self.hash_func(password, hash_target) if self.hash_func.__code__.co_argcount > 1 else self.hash_func(password) == hash_target:
                    with self.lock:
                        self.found = True
                        self.result = password
                    return
            except:
                continue

    def crack(self, hash_target: str, wordlist: List[str], threads: int = 4, 
              progress_callback: Callable = None) -> Optional[str]:
        if not self.hash_func:
            return None

        chunk_size = len(wordlist) // threads
        chunks = [wordlist[i:i + chunk_size] for i in range(0, len(wordlist), chunk_size)]
        threads = []

        for chunk in chunks:
            t = threading.Thread(
                target=self.worker,
                args=(hash_target, chunk, progress_callback)
            )
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return self.result