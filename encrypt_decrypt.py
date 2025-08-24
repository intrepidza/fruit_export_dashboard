from cryptography.fernet import Fernet
import os


def generate_key(key_file='secret.key'):
    """Generate a key and save to file."""
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
    return key

def load_key(key_file='secret.key'):
    """Load key from file"""
    if not os.path.exists(key_file):
        raise FileNotFoundError(f"Key file {key_file} not found.")
    
    with open(key_file, 'rb') as f:
        return f.read()
    
def encrypt_file(input_file, output_file, key):
    fernet = Fernet(key)

    with open(input_file, "rb") as f:
        original_data = f.read()

    encrypted_data = fernet.encrypt(original_data)
    
    with open(output_file, "wb") as f:
        f.write(encrypted_data)

def decrypt_file(input_file, output_file, key):
    fernet = Fernet(key)

    with open(input_file, "rb") as f:
        decrypted_data = fernet.decrypt(f.read())

    # encrypted_data = fernet.encrypt(original_data)
    
    with open(output_file, "wb") as f:
        f.write(decrypted_data)
    

def main():
    enc_or_dec = input("(e)ncrypt or (d)ecrypt?: ")

    if enc_or_dec == 'e':
        input_file = input("Enter path of file to encrypt: ")
        output_file = input("Enter path for encrypted file: ")

    elif enc_or_dec == 'd':
        input_file = input("Enter path of file to decrypt: ")
        output_file = input("Enter path for decrypted file: ")
    
    else:
        print('Incorrect selection...')

    # Generate or load key:
    key_file = 'secret.key'
    if not os.path.exists(key_file):
    # if not key_file:
        key = generate_key(key_file)
    else:
        key = load_key(key_file)


    if enc_or_dec == 'e':

        # Encrypt file:
        try:
            encrypt_file(input_file, output_file, key)
            print("File encrypted")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")


    elif enc_or_dec == 'd':
        try:
            decrypt_file(input_file, output_file, key)
            print("File decrypted")
        except FileNotFoundError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error occurred: {e}")

    else:
        print("Incorrect selection...")

if __name__ == '__main__':
    main()
