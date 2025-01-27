import os
import shutil


def copy_temp_config():
    package_path = os.path.dirname(os.path.dirname(__file__))

    # Define the source file path
    source_file = os.path.join(package_path, 'languagetool.tmp.cfg')

    # Check if the file exists
    if not os.path.exists(source_file):
        raise FileNotFoundError(f"File 'languagetool.tmp.cfg' is missing and could not be copied.")

    # Define the destination file path (current directory)
    destination_file = os.path.join(os.getcwd(), 'languagetool.cfg')

    # Copy the file
    shutil.copy(source_file, destination_file)

    print(f"File 'languagetool.tmp.cfg' copied to {destination_file}")


if __name__ == '__main__':
    copy_temp_config()
