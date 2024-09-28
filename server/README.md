# Cookie Breaker and Rebuilder Documentation

## Overview
The **CookieBreaker** and **CookieRebuilder** classes facilitate the process of breaking a large file into smaller chunks (cookie pieces) and then reconstructing those pieces back into a single file. This is particularly useful for managing large files in scenarios where processing smaller segments is more efficient.

### Directory Structure
```
-- MAIN CODE
    -- Server
       -- Build&Rebuild...
            -- Breaking_the_file --> Code/logic to break down the initial test file
            -- File_Rebuilder    --> Rebuilds the text file
```

## Imports
Make sure to include the following imports at the beginning of your code:
```python
import os
```

## Classes

### 1. CookieBreaker

#### Description
The `CookieBreaker` class is responsible for dividing a large file into smaller chunks, called cookie pieces, based on a specified chunk size. 

#### Constructor
```python
CookieBreaker(chunk_size=512)
```
- **Parameters**:
  - `chunk_size`: (int) The size of each chunk in bytes. Default is `512`.

#### Methods
```python
List[str] break_cookie(String file_path, String target_directory)
```
- **Description**: Breaks the specified file into smaller pieces and saves them in the target directory.
- **Parameters**:
  - `file_path`: (String) The path of the file to be broken.
  - `target_directory`: (String) The directory where the cookie pieces will be stored.
- **Returns**: A list of paths to the created cookie pieces.
- **Exceptions**: Raises an exception if the target directory cannot be created or if there are issues reading the file.

### 2. CookieRebuilder

#### Description
The `CookieRebuilder` class is responsible for reconstructing a file from cookie pieces stored in a specified directory. It ensures the pieces are sorted correctly and writes them to a single output file.

#### Constructor
```python
CookieRebuilder(String piecesDirectory, String rebuiltFilePath)
```
- **Parameters**:
  - `piecesDirectory`: (String) The directory where the cookie pieces are stored.
  - `rebuiltFilePath`: (String) The file path where the rebuilt file will be saved.

#### Methods
```python
void rebuild()
```
- **Description**: Rebuilds the cookie file from the pieces in the specified directory.
- **Process**:
  - Checks if the output directory exists and creates it if not.
  - Reads the cookie pieces from the specified directory, filtering out any unwanted files.
  - Sorts the cookie pieces based on the numerical part of their filenames.
  - Writes the sorted pieces into the rebuilt file.
  - Outputs the total size of the rebuilt file and logs the writing process.
- **Exceptions**: Throws an exception if the directory is empty or if there are no valid cookie pieces to rebuild.

## Example Usage

### Main Code
```python
import os

if __name__ == "__main__":
    # User input for paths
    cookie_path = input("Enter the path to the cookie file to break: ")
    target_directory = '/path/to/save/chunks'  # Adjust as needed
    rebuilt_file = '/path/to/save/rebuilt_file.txt'  # Adjust as needed

    # Break the cookie file
    cookie_breaker = CookieBreaker()  # Create an instance of CookieBreaker
    cookie_pieces = cookie_breaker.break_cookie(cookie_path, target_directory)

    # Print each broken piece in a cleaner format
    print(f"Cookie broken into {len(cookie_pieces)} pieces:")
    for piece in cookie_pieces:
        print(f"- {piece}")

    # Rebuild the cookie file from pieces
    rebuilder = CookieRebuilder(target_directory, rebuilt_file)
    rebuilder.rebuild()
```

### Notes
- Ensure that the specified paths for the cookie file and target directories are valid and accessible.
- The rebuilt file will be saved in the specified location, and its total size will be logged in the console.
