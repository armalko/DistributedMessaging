from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys():
    """Generate RSA public and private keys."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    # Serialize keys to store or share
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_key_pem, public_key_pem

def save_keys_to_files(private_key_pem, public_key_pem,
                       private_key_file="private_key.pem", public_key_file="public_key.pem"):
    """Save private and public keys to PEM files."""
    with open(private_key_file, "wb") as priv_file:
        priv_file.write(private_key_pem)
    with open(public_key_file, "wb") as pub_file:
        pub_file.write(public_key_pem)

def load_private_key_from_file(private_key_file="private_key.pem"):
    """Load a private key from a PEM file."""
    with open(private_key_file, "rb") as priv_file:
        private_key_pem = priv_file.read()
    return private_key_pem

def load_public_key_from_file(public_key_file="public_key.pem"):
    """Load a public key from a PEM file."""
    with open(public_key_file, "rb") as pub_file:
        public_key_pem = pub_file.read()
    return public_key_pem

def encode_text(public_key_pem, plaintext):
    """Encrypt text using a public key."""
    public_key = serialization.load_pem_public_key(public_key_pem)
    ciphertext = public_key.encrypt(
        plaintext.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decode_text(private_key_pem, ciphertext):
    """Decrypt text using a private key."""
    private_key = serialization.load_pem_private_key(private_key_pem, password=None)
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode('utf-8')

# Example usage
if __name__ == "__main__":
    # Generate keys
    private_key_pem, public_key_pem = generate_keys()

    # Save keys to files
    save_keys_to_files(private_key_pem, public_key_pem)

    # Load keys from files
    loaded_private_key_pem = load_private_key_from_file()
    loaded_public_key_pem = load_public_key_from_file()

    # Original message
    message = "This is a secret message."
    print("\nOriginal Message:", message)

    # Encrypt the message
    encrypted_message = encode_text(loaded_public_key_pem, message)
    print("\nEncrypted Message:", encrypted_message)

    # Decrypt the message
    decrypted_message = decode_text(loaded_private_key_pem, encrypted_message)
    print("\nDecrypted Message:", decrypted_message)
