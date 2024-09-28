from FileHasher import FileHasher

# Example usage:
file_hasher = FileHasher()

# Directories
source_folder = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Build&Rebuild_main_code/Breaking_the_file/broken_pieces'
hash_output_folder = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Checksum/hashes'


file_hasher.hash_files(source_folder, hash_output_folder)

# Verify the hashes
verification_status = file_hasher.verify_hashes(hash_output_folder, source_folder)

# Print final status
if verification_status:
    print("Final Status: All files verified successfully!")
else:
    print("Final Status: Some files failed verification.")