import os

def search_files(search_string, directory='.'):
    """
    Search for a string in all files within the given directory.
    
    Args:
        search_string (str): The string to search for
        directory (str): The directory to search in (defaults to current directory)
    """
    for root, dirs, files in os.walk(directory):
        # Skip the __pycache__ directory
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
            
        for file in files:
            # Skip binary files and common non-text files
            if file.endswith(('.pyc', '.git', '.png', '.jpg')):
                continue
                
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if search_string in line:
                            print(f"\n{file_path}:{line_num}")
                            print(f"    {line.strip()}")
            except (UnicodeDecodeError, IOError):
                # Skip files that can't be read as text
                continue

if __name__ == "__main__":
    search_term = input("Enter the string to search for: ")
    search_files(search_term, "Extract2JSON") 