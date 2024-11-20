def set_key(num):
    """Calculate the key, ensuring it remains within the range 0-25."""
    return num % 26


def shift_character(char, shift, lower_bound, upper_bound):
    """Shift a character within specified bounds."""
    shifted = ord(char) + shift
    if shifted > upper_bound:
        shifted = lower_bound + (shifted - upper_bound - 1)
    elif shifted < lower_bound:
        shifted = upper_bound - (lower_bound - shifted - 1)
    return chr(shifted)


def encrypt(plaintext, key):
    """Encrypt the given plaintext using the Caesar cipher."""
    key = set_key(key)
    return ''.join(
        shift_character(c, key, 97, 122) if 'a' <= c <= 'z' else c
        for c in plaintext.lower()
    )


def decrypt(ciphertext, key):
    """Decrypt the given ciphertext using the Caesar cipher."""
    key = set_key(key)
    return ''.join(
        shift_character(c, -key, 97, 122) if 'a' <= c <= 'z' else c
        for c in ciphertext.lower()
    )


if __name__ == "__main__":
    key = int(input("Please enter the key: "))
    string = input("Please enter the string that you would like to encrypt: ")

    encrypted = encrypt(string, key)
    print(f"Encrypted: {encrypted}")

    dec = int(input("Would you like to decrypt (Enter 1 for yes or 2 for no)?: "))
    if dec == 1:
        decrypted = decrypt(encrypted, key)
        print(f"Decrypted: {decrypted}")
    else:
        print("Have a nice day.")
