"""Sample script that copies a file from source to destination."""
import argparse
import shutil


def copy_file(src, dest):
    """
    Function to copy a file from source to destination.

    :param src: Source file path
    :type src: str
    :param dest: Destination file path
    :type dest: str
    """
    shutil.copy2(src, dest)


def main():
    """
    Main function to parse command line arguments and execute file copy.
    """
    parser = get_argument_parser()

    args = parser.parse_args()

    if args.verbose:
        print(f"Copying file from {args.source} to {args.destination}")

    copy_file(args.source, args.destination)

    if args.verbose:
        print("File copied successfully")


def get_argument_parser():
    parser = argparse.ArgumentParser(description="A simple file copy script.")
    parser.add_argument(
        "-s",
        "--source",
        type=str,
        required=True,
        help="Source file path. Example: -s '/path/to/source'",
    )
    parser.add_argument(
        "-d", "--destination", type=str, required=True, help="Destination file path"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose mode"
    )
    
    return parser


if __name__ == "__main__":
    main()
