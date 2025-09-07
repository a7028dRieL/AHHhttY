# 代码生成时间: 2025-09-07 12:11:19
import tarfile
def extract_tar_gz(file_path, extract_path):
    """Extract a tar.gz file.

    Args:
        file_path (str): The path to the tar.gz file.
        extract_path (str): The path to extract the contents to.

    Returns:
        None
    """
    try:
        with tarfile.open(file_path, 'r:gz') as file:
            file.extractall(extract_path)
            print(f"File {file_path} extracted successfully to {extract_path}")
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
    except tarfile.TarError:
        print(f"Error: The file {file_path} is not a valid tar.gz file.")
def main():
    # Example usage of the extract_tar_gz function
    if __name__ == '__main__':
        import sys
        if len(sys.argv) != 3:
            print("Usage: python uncompress_tool.py <tar_gz_file_path> <extract_path>")
            return

        file_path = sys.argv[1]
        extract_path = sys.argv[2]
        extract_tar_gz(file_path, extract_path)
"""Entry point for the uncompression tool."""
if __name__ == '__main__':
    main()