import os.path

def split_buffer(buffer, chunk_size=256):
    return [buffer[i:i + chunk_size] for i in range(0, len(buffer), chunk_size)]

def reconstruct_buffer(chunks):
    return b''.join(chunks)  # Use b''.join() for byte strings

class Chunks:

    filepath = ''
    cleanfilepath = ''

    def __init__(self, filepath, cleanpath) -> None:
        self.filepath = filepath
        self.cleanfilepath = cleanpath

    def readChunkFile(self, name, number):
        fname = name + '_' + str(number)
        path = self.filepath + '/' + fname

        with open(path, 'rb') as f:
            file_data = f.read()

        return file_data

    def writeChunkFile(self, name, number, file_data):
        fname = name + '_' + str(number)
        path = self.filepath + '/' + fname

        with open(path, 'wb+') as f:
            f.write(file_data)

    def readFullFile(self, name):
        index = 1
        file_data = ''

        while True:
            fname = name + '_' + str(index)
            path = self.filepath + '/' + fname
            isPath = os.path.isfile(fname)

            if isPath == False:
                return file_data
        
            with open(path, 'rb') as f:
                temp = file_data = f.read()

            file_data = file_data + temp

            index = index + 1

    def deconstructFile(self, name):
        fname = name
        path = self.cleanfilepath + '/' + fname

        with open(path, 'rb') as f:
            file_data = f.read()

        return split_buffer(file_data)
    
    def reconstrucFile(self, name, buffers):
        fname = name
        path = self.cleanfilepath + '/' + fname

        buffer = reconstruct_buffer(buffers)

        with open(path, 'wb+') as f:
            f.write(buffer)
