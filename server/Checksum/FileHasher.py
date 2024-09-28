import hashlib
import os

class FileHasher:
    def __init__(self):
        print("FileHasher initialized.")

    def hash_files(self, input_dir, output_dir):
        """Hash all files in the input directory and store the hashes in the output directory."""
        os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file_name)
            
            if os.path.isfile(file_path):
                print(f"Hashing {file_name}...")

                sha256_hash = hashlib.sha256()  # Create a new SHA-256 hash object

                with open(file_path, "rb") as file:
                    while chunk := file.read(4096):  # Read in 4KB chunks
                        sha256_hash.update(chunk)  # Update the hash with the current chunk

                # Save the hash to a file
                hash_value = sha256_hash.hexdigest()
                hash_filename = os.path.join(output_dir, f"{file_name}.hash")
                with open(hash_filename, "w") as hash_file:
                    hash_file.write(hash_value)

                print(f"Hash for {file_name}: {hash_value}")

        print(f"Hashing completed. Hash files are in {output_dir}")


    def verify_hashes(self, hash_dir, original_files_dir):
        """Verify the hashes of the files in the given directory."""
        all_verified = True  # Start assuming all files are verified

        # List all hash files for debugging
        hash_files = [f for f in os.listdir(hash_dir) if f.endswith(".hash")]
        print(f"Hash files to verify: {hash_files}")

        for hash_file in hash_files:
            base_name = hash_file[:-5]  # Remove the '.hash' extension
            hash_file_path = os.path.join(hash_dir, hash_file)

            # Read the stored hash from the hash file
            with open(hash_file_path, "r") as file:
                stored_hash = file.read().strip()

            original_file_path = os.path.join(original_files_dir, base_name)

            # Verify if the original file exists
            if os.path.isfile(original_file_path):
                sha256_hash = hashlib.sha256()
                
                with open(original_file_path, "rb") as file:
                    while chunk := file.read(4096):
                        sha256_hash.update(chunk)

                calculated_hash = sha256_hash.hexdigest()

                if calculated_hash == stored_hash:
                    print(f"{base_name} is verified. Hash matches.")
                else:
                    print(f"{base_name} hash mismatch! Integrity compromised.")
                    all_verified = False  # Set to False if any file fails verification
            else:
                print(f"{original_file_path} does not exist.")
                all_verified = False  # Set to False if any file does not exist

        return all_verified  # Return the overall verification status



