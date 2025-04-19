#!/usr/bin/env python3
import os
import sys
import argparse
import glob
import importlib.util
from pathlib import Path


def find_converters():
    """Find all available converters in the converters directory."""
    converters = []
    converters_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "converters")

    # Make sure the converters directory exists
    if not os.path.exists(converters_dir):
        print(f"Error: Converters directory not found: {converters_dir}")
        return []

    # Find all subdirectories with a main.py file
    for item in os.listdir(converters_dir):
        converter_dir = os.path.join(converters_dir, item)
        main_py = os.path.join(converter_dir, "main.py")

        if os.path.isdir(converter_dir) and os.path.exists(main_py):
            # Read the first function from main.py to get the description
            try:
                with open(main_py, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Look for the first docstring
                    if '"""' in content:
                        docstring = content.split('"""')[1].strip().split('\n')[0]
                    else:
                        docstring = f"Convert files with {item}"
            except Exception:
                docstring = f"Convert files with {item}"

            converters.append((item, docstring))

    return converters


def load_converter(converter_name):
    """Dynamically load a converter module."""
    converter_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "converters",
        converter_name,
        "main.py"
    )

    if not os.path.exists(converter_path):
        print(f"Error: Converter not found: {converter_name}")
        return None

    # Load the module dynamically
    spec = importlib.util.spec_from_file_location(converter_name, converter_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Get the main function from the module
    main_functions = [name for name in dir(module) if name.startswith('convert_')]

    if not main_functions:
        print(f"Error: No conversion function found in {converter_name}")
        return None

    # Return the first conversion function
    return getattr(module, main_functions[0])


def print_available_converters():
    """Print a list of all available converters with descriptions."""
    converters = find_converters()

    if not converters:
        print("No converters found!")
        return

    print("\nAvailable converters:")
    print("--------------------")
    for name, description in converters:
        print(f"  {name:<15} - {description}")
    print()


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='File Converter Collection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Examples:\n'
               '  python cli.py img2webp path/to/images\n'
               '  python cli.py csv2json path/to/csvfiles --pretty\n'
               '  python cli.py --list'
    )

    parser.add_argument(
        'converter',
        nargs='?',
        help='Converter to use (e.g., img2webp, text2pdf)'
    )

    parser.add_argument(
        'folder',
        nargs='?',
        help='Folder containing files to convert'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available converters'
    )

    parser.add_argument(
        '--quality',
        type=int,
        help='Quality setting for conversions that support it (0-100)'
    )

    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Enable pretty printing for formats that support it'
    )

    parser.add_argument(
        '--theme',
        help='Theme to use for conversions that support it'
    )

    return parser.parse_args()


def main():
    """Main entry point for the converter CLI."""
    args = parse_args()

    # List available converters
    if args.list or not args.converter:
        print_available_converters()
        return

    # Make sure a folder was specified
    if not args.folder:
        print("Error: Please specify a folder containing files to convert.")
        print(f"Usage: python cli.py {args.converter} /path/to/folder")
        return

    # Make sure the folder exists
    if not os.path.exists(args.folder):
        print(f"Error: Folder not found: {args.folder}")
        return

    # Load the specified converter
    converter_func = load_converter(args.converter)
    if not converter_func:
        return

    # Prepare converter arguments based on function signature
    import inspect
    sig = inspect.signature(converter_func)
    converter_args = {'source_folder': args.folder}

    # Add optional arguments if the converter supports them
    if 'quality' in sig.parameters and args.quality is not None:
        converter_args['quality'] = args.quality

    if 'pretty_print' in sig.parameters and args.pretty:
        converter_args['pretty_print'] = args.pretty

    if 'theme' in sig.parameters and args.theme:
        converter_args['theme'] = args.theme

    # Run the converter
    try:
        converter_func(**converter_args)
    except Exception as e:
        print(f"Error running {args.converter}: {e}")

    print("\nDone!")


if __name__ == "__main__":
    main()