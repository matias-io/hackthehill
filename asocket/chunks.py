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

    def writeFullFile(self, name, data):
        fname = name
        path = self.cleanfilepath + '/' + fname

        with open(path, 'wb+') as f:
            f.write(data)

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

