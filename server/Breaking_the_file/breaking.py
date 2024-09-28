import os

def break_cookie(file_path, target_directory):
    chunk_size = 512  # Each "bite" or chunk is 512 bytes
    cookie_pieces = [] 

    # Ensure the target directory exists
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    with open(file_path, 'rb') as cookie_file:  
        chunk_number = 0
        while True:
            bite = cookie_file.read(chunk_size)  # Read 512 bytes at a time (a small piece)
            if not bite:  # If there’s no more to read, stop
                break
            
            piece_name = f'cookie_piece_{chunk_number}'  # Name each piece
            
            # Create the full path to save the chunk in the target directory
            piece_path = os.path.join(target_directory, piece_name)

            with open(piece_path, 'wb') as chunk:  # Write the chunk to a new file
                chunk.write(bite)  # Save the 512-byte chunk
                
            cookie_pieces.append(piece_path)  # Keep track of all the pieces (with full paths)
            chunk_number += 1  # Move to the next piece

    return cookie_pieces  # Return the list of broken pieces (chunks)

# Example usage:
cookie_path = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Breaking_the_file/test_file.txt'
target_directory = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Breaking_the_file/broken_pieces'

cookie_pieces = break_cookie(cookie_path, target_directory)

print(f'Cookie broken into pieces: {cookie_pieces}')
