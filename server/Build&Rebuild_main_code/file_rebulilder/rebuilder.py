import os

class CookieRebuilder:
    def __init__(self, pieces_directory, rebuilt_file_path):
        self.pieces_directory = pieces_directory
        self.rebuilt_file_path = rebuilt_file_path

    def rebuild(self):
        # Ensure the output directory exists
        if not os.path.exists(os.path.dirname(self.rebuilt_file_path)):
            os.makedirs(os.path.dirname(self.rebuilt_file_path))

        # Check if the directory is empty
        pieces = os.listdir(self.pieces_directory)
        if not pieces:
            print("No pieces to rebuild.")
            return

        # Filter out unwanted system files like .DS_Store and ensure only cookie pieces are processed
        pieces = [piece for piece in pieces if piece.startswith('cookie_piece_')]

        # Sort by the numerical part of the file name to ensure correct order
        pieces = sorted(pieces, key=lambda x: int(x.split('_')[2]))

        print("Sorted pieces:", pieces)  # Debugging line to show the correct order of pieces

        total_size = 0  # Track the total size of the rebuilt file

        # Open the rebuilt file in write-binary mode
        with open(self.rebuilt_file_path, 'wb') as rebuilt_file:
            for piece in pieces:
                piece_path = os.path.join(self.pieces_directory, piece)  # Get the full path to the piece
                
                with open(piece_path, 'rb') as piece_file:
                    piece_data = piece_file.read()
                    rebuilt_file.write(piece_data)  # Write the chunk to the rebuilt file

                    # Print the size of each piece being written
                    print(f"Writing chunk {piece} of size {len(piece_data)} bytes")
                    total_size += len(piece_data)

        print(f"Rebuilt file saved at: {self.rebuilt_file_path}")
        print(f"Total size of rebuilt file: {total_size} bytes")

# Example usage:
broken_pieces_dir = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/Build&Rebuild_main_code/Breaking_the_file/broken_pieces'
rebuilt_file = '/Users/adityabaindur/Desktop/HTH/hackthehill/server/rebuilt.txt'

rebuilder = CookieRebuilder(broken_pieces_dir, rebuilt_file)
rebuilder.rebuild()
