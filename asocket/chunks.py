import os.path

def split_buffer(buffer, chunk_size=256):
    return [buffer[i:i + chunk_size] for i in range(0, len(buffer), chunk_size)]

def reconstruct_buffer(chunks):
    return b''.join(chunks)  # Use b''.join() for byte strings

class Chunks:

    filepath = '' # Chunks
    cleanfilepath = '' # Actual files

    def __init__(self, filepath, cleanpath) -> None:
        self.filepath = filepath
        self.cleanfilepath = cleanpath

    # Read a specific chunk file
    # Return the buffer
    def readChunkFile(self, name, number):
        fname = name + '_' + str(number)
        path = self.filepath + '/' + fname

        with open(path, 'rb') as f:
            file_data = f.read()

        return file_data

    # Write a specific chunk file
    def writeChunkFile(self, name, number, file_data):
        fname = name + '_' + str(number)
        path = self.filepath + '/' + fname

        with open(path, 'wb+') as f:
            f.write(file_data)

    # Read all chunk files
    # Return a dict of buffers
    def readAllChunks(self, name):
        index = 0
        n = self.numberOfChunks(name)
        print("Number of chunks to send: " + str(n))
        found = 0
        chunks = {}

        while found < n:
            fname = name + '_' + str(index)
            path = self.filepath + '/' + fname
            print("Trying path " + path)
        
            try: 
                with open(path, 'rb') as f:
                    temp = f.read()
                    chunks[index] = temp
                    found = found + 1
            except:
                print("Path not found: " + path)
                continue

            index = index + 1

        return chunks


    # Read all chunks files and assemble them
    # This assumes all the chunks are available
    # Returns the buffer
    def readFullFile(self, name):
        index = 0

        file_data = []

        while True:
            fname = name + '_' + str(index)
            path = self.filepath + '/' + fname
            print(path)
        
            try: 
                with open(path, 'rb') as f:
                    temp = f.read()
            except:
                print(file_data)
                return reconstruct_buffer(file_data)

            print("Reading " + fname)
            file_data.append(temp)

            index = index + 1

    # Write a complete file into clean path using buffer
    def writeFullFile(self, name, data):
        fname = name
        path = self.cleanfilepath + '/' + fname

        with open(path, 'wb+') as f:
            f.write(data)

    # Read a full file and return list of deconstructed chunks
    def deconstructFile(self, name):
        fname = name
        path = self.cleanfilepath + '/' + fname

        with open(path, 'rb') as f:
            file_data = f.read()

        return split_buffer(file_data)
    
    # Take a list of deconstructed chunks and wirte the full file
    def reconstrucFile(self, name, buffers):
        fname = name
        path = self.cleanfilepath + '/' + fname

        buffer = reconstruct_buffer(buffers)

        with open(path, 'wb+') as f:
            f.write(buffer)

    # List all unique files in the chunks
    def listFiles(self):
        l = []
        for path in os.listdir(self.filepath):
            l.append(path.split('_')[0])

        l = list(dict.fromkeys(l))
        return l
    
    # Number of available chunks for a file name
    def numberOfChunks(self, filename):
        l = []
        for path in os.listdir(self.filepath):
            if path.startswith(filename):
                l.append(path)
        return len(l)

