import re
from typing import Dict, List

class HashDetector:
    @staticmethod
    def _is_hex(s: str) -> bool:
        s = s.lower().replace('0x', '')
        return re.fullmatch(r'^[a-f0-9]+$', s) is not None

    def detect_hash_algorithm(self, hash_str: str) -> Dict[str, str]:
        hash_str = hash_str.strip()
        result = {
            'algorithm': 'Unknown',
            'length': len(hash_str),
            'variants': []
        }

        # Check for common hash formats by length (hex encoded)
        if self._is_hex(hash_str):
            length = len(hash_str)
            if length == 32:
                result['algorithm'] = 'MD5'
                result['variants'] = ['MD5', 'MD4', 'MD2']
            elif length == 40:
                result['algorithm'] = 'SHA-1'
                result['variants'] = ['SHA-1']
            elif length == 56:
                result['algorithm'] = 'SHA-224'
            elif length == 64:
                result['algorithm'] = 'SHA-256'
                result['variants'] = ['SHA-256', 'SHA3-256']
            elif length == 96:
                result['algorithm'] = 'SHA-384'
            elif length == 128:
                result['algorithm'] = 'SHA-512'
                result['variants'] = ['SHA-512', 'SHA3-512']

        # Check for special hash formats (password hashes)
        if hash_str.startswith("$2a$") or hash_str.startswith("$2b$"):
            result['algorithm'] = 'bcrypt'
        elif hash_str.startswith("$1$"):
            result['algorithm'] = 'MD5-crypt'
        elif hash_str.startswith("$5$"):
            result['algorithm'] = 'SHA-256-crypt'
        elif hash_str.startswith("$6$"):
            result['algorithm'] = 'SHA-512-crypt'
        elif hash_str.startswith("$argon2"):
            result['algorithm'] = 'Argon2'
        elif hash_str.startswith("{SSHA}"):
            result['algorithm'] = 'Salted SHA-1'
        elif hash_str.startswith("{SHA}"):
            result['algorithm'] = 'SHA-1'
        elif hash_str.startswith("$pbkdf2"):
            result['algorithm'] = 'PBKDF2'

        return result