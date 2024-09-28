import hashlib
import os

class FileHasher:
    def __init__(self):
        print("FileHasher initialized.")

    def hash_file(self, file_path):
        """Hash a single file and return the hash value."""
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)
            print(f"Hashing {file_name}...")

            sha256_hash = hashlib.sha256()  # Create a new SHA-256 hash object

            with open(file_path, "rb") as file:
                while chunk := file.read(4096):  # Read in 4KB chunks
                    sha256_hash.update(chunk)  # Update the hash with the current chunk

            # Return the hash value
            hash_value = sha256_hash.hexdigest()
            print(f"Hash for {file_name}: {hash_value}")
            return hash_value
        else:
            print(f"{file_path} is not a valid file.")
            return None

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

# Example usage:
if __name__ == "__main__":
    hasher = FileHasher()
    
    # Replace 'filename.ext' with the actual file you want to hash
    file_to_hash = "/path/to/your/filename.ext"
    
    # Hash the file and get the hash value
    hash_value = hasher.hash_file(file_to_hash)

    # Example verification
    if hash_value:
        verification_result = hasher.verify_hash(hash_value, file_to_hash)
        if verification_result:
            print("File verified successfully.")
        else:
            print("Verification failed.")
