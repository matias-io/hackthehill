def break_cookie(file_path):
    chunk_size = 512  # Each "bite" or chunk is 512 bytes
    cookie_pieces = [] 

    with open(file_path, 'rb') as cookie_file:  
        chunk_number = 0
        while True:
            bite = cookie_file.read(chunk_size)  # Read 512 bytes at a time (a small piece)
            if not bite:  # If there’s no more to read, stop
                break
            
            piece_name = f'cookie_piece_{chunk_number}'  # Name each piece
            
            with open(piece_name, 'wb') as chunk:  # Write the chunk to a new file
                chunk.write(bite)  # Save the 512-byte chunk
                
            cookie_pieces.append(piece_name)  # Keep track of all the pieces
            chunk_number += 1  # Move to the next piece

    return cookie_pieces  # Return the list of broken pieces (chunks)

# Example usage:
cookie_path = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Breaking_the_file/test_file.txt'



cookie_pieces = break_cookie(cookie_path)
print(f'Cookie broken into pieces: {cookie_pieces}')
