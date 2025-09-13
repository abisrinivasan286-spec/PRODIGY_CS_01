#!/usr/bin/env python3
"""
Caesar Cipher: encrypt & decrypt text by shifting letters.
- Keeps case (A/a).
- Leaves spaces, punctuation, numbers unchanged.
- Works with positive or negative shifts.
- You can run interactively OR via command-line flags.

Examples (CLI):
  python caesar_cipher.py -m encrypt -s 3 -t "Hello, World!"
  python caesar_cipher.py -m decrypt -s 3 -t "Khoor, Zruog!"
"""
from __future__ import annotations
import argparse
from typing import List, Tuple

ALPHABET_SIZE = 26

def normalize_shift(shift: int) -> int:
    return shift % ALPHABET_SIZE

def shift_char(ch: str, shift: int) -> str:
    if ch.isalpha():
        base = ord('A') if ch.isupper() else ord('a')
        return chr((ord(ch) - base + shift) % ALPHABET_SIZE + base)
    return ch

def encrypt(text: str, shift: int) -> str:
    s = normalize_shift(shift)
    return ''.join(shift_char(c, s) for c in text)

def decrypt(text: str, shift: int) -> str:
    return encrypt(text, -shift)

def brute_force_candidates(text: str) -> List[Tuple[int, str]]:
    return [(s, decrypt(text, s)) for s in range(ALPHABET_SIZE)]

def run_cli(mode: str, shift: int, text: str) -> None:
    if mode == "encrypt":
        print(encrypt(text, shift))
    else:
        print(decrypt(text, shift))

def interactive() -> None:
    print("=" * 60)
    print("                CAESAR CIPHER (interactive)")
    print("=" * 60)
    print("Tips:")
    print("  • Enter 'E' to Encrypt, 'D' to Decrypt, or 'Q' to quit.")
    print("  • For Decrypt, if you don't know the shift, enter '?' to try all keys.")
    print()

    while True:
        mode = input("Mode [E/D/Q]: ").strip().lower()
        if not mode:
            continue
        if mode == 'q':
            print("Goodbye!")
            return
        if mode not in ('e', 'd'):
            print("Please enter E, D, or Q.")
            continue

        text = input("Enter your message: ")

        shift_str = input("Enter shift (integer). For Decrypt, '?' = try all: ").strip()
        if mode == 'd' and shift_str == '?':
            print("\nTrying all 26 keys... (shift : candidate)")
            for s, candidate in brute_force_candidates(text):
                print(f"{s:>2} : {candidate}")
            print()
            continue

        try:
            shift = int(shift_str)
        except ValueError:
            print("Shift must be an integer (e.g., 3, -2, 52). Try again.\n")
            continue

        if mode == 'e':
            result = encrypt(text, shift)
            print(f"\nEncrypted (shift {normalize_shift(shift)}): {result}\n")
        else:
            result = decrypt(text, shift)
            print(f"\nDecrypted (shift {normalize_shift(shift)}): {result}\n")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Caesar Cipher: encrypt/decrypt text by shifting letters.")
    p.add_argument("-m", "--mode", choices=["encrypt", "decrypt"], help="Operation to perform.")
    p.add_argument("-s", "--shift", type=int, help="Shift amount (integer).")
    p.add_argument("-t", "--text", type=str, help="Text to process.")
    return p

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.mode and args.shift is not None and args.text is not None:
        run_cli(args.mode, args.shift, args.text)
    else:
        interactive()

if __name__ == "__main__":
    main()
