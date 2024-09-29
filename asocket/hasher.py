import hashlib
import os


def hash(file_path):
        
    file_name = os.path.basename(file_path)
    print(f"Hashing {file_name}...")

    sha256_hash = hashlib.sha256()  # Create a new SHA-256 hash object

    with open(file_path, "rb") as file:
        while chunk := file.read(512):  # Read in 512 bytes chunks
            sha256_hash.update(chunk)  # Update the hash with the current chunk



    # Return the hash value
    hash_value = sha256_hash.hexdigest()
    print(f"Hash for {file_name}: {hash_value}")
    return hash_value
    

    



def verify_hash(self, hash_value, file_path):
    """Verify the hash of the given file against the provided hash value."""
    if os.path.isfile(file_path):
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha256_hash.update(chunk)

        calculated_hash = sha256_hash.hexdigest()

        if calculated_hash == hash_value:
            print(f"{os.path.basename(file_path)} is verified. Hash matches.")
            return True
        else:
            print(f"{os.path.basename(file_path)} hash mismatch! Integrity compromised.")
            return False
    else:
        print(f"{file_path} does not exist.")
        return False

