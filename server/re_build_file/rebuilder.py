import os


def check_basic():

    return 1 
    

def rebuild_cookie(pieces_directory, rebuilt_file_path):

    if(os.listdir(pieces_directory) == None):
        print("hello")

    # List all the pieces in the directory and sort them by name to ensure the correct order
    pieces = sorted(os.listdir(pieces_directory))

    # Open the rebuilt file in write-binary mode
    with open(rebuilt_file_path, 'wb') as rebuilt_file:
        for piece in pieces:
            piece_path = os.path.join(pieces_directory, piece)  # Get the full path to the piece
            
            with open(piece_path, 'rb') as piece_file:
                # Read each chunk and append it to the rebuilt file
                rebuilt_file.write(piece_file.read())

    print(f"Rebuilt file saved at: {rebuilt_file_path}")

# Example usage:
broken_pieces_dir = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Breaking_the_file/broken_pieces'
rebuilt_file = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/re_build_file'

rebuild_cookie(broken_pieces_dir, rebuilt_file)
