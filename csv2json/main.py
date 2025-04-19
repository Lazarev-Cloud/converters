import os
import csv
import json
import glob


def convert_csv_to_json(source_folder, pretty_print=True, encoding='utf-8'):
    """
    Convert all CSV files in a folder to JSON format.

    Args:
        source_folder (str): Path to the folder containing CSV files
        pretty_print (bool): Whether to format the JSON with indentation for readability
        encoding (str): Encoding to use when reading CSV files
    """
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' not found.")
        return

    # Create a 'json_converted' subfolder if it doesn't exist
    output_folder = os.path.join(source_folder, "json_converted")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # List of CSV file extensions to convert
    extensions = ['*.csv', '*.CSV']

    # Get all CSV files in the source folder
    csv_files = []
    for ext in extensions:
        csv_files.extend(glob.glob(os.path.join(source_folder, ext)))

    if not csv_files:
        print(f"No CSV files found in '{source_folder}'.")
        return

    print(f"Found {len(csv_files)} CSV files to convert.")

    # Convert each CSV file to JSON
    for csv_path in csv_files:
        try:
            # Get the filename without extension
            filename = os.path.basename(csv_path)
            name_without_ext = os.path.splitext(filename)[0]

            # Set the output path with JSON extension
            json_path = os.path.join(output_folder, f"{name_without_ext}.json")

            # Read the CSV file
            with open(csv_path, 'r', encoding=encoding, newline='') as csvfile:
                # Try to detect the dialect (comma, semicolon, etc.)
                try:
                    dialect = csv.Sniffer().sniff(csvfile.read(4096))
                    csvfile.seek(0)
                except:
                    print(f"Warning: Could not detect CSV dialect for {filename}, using comma as delimiter.")
                    dialect = 'excel'  # Default to comma-separated

                # Read CSV into a list of dictionaries
                reader = csv.DictReader(csvfile, dialect=dialect)
                data = []

                try:
                    for row in reader:
                        # Clean empty strings and convert numeric values
                        clean_row = {}
                        for key, value in row.items():
                            if key is None:  # Skip columns with no header
                                continue

                            # Clean the key (remove whitespace)
                            clean_key = key.strip()

                            # Try to convert to appropriate data type
                            if value == "":
                                clean_value = None
                            else:
                                try:
                                    # Try to convert to int or float
                                    if value.isdigit():
                                        clean_value = int(value)
                                    else:
                                        clean_value = float(value)
                                        # Convert to int if it's a whole number
                                        if clean_value.is_integer():
                                            clean_value = int(clean_value)
                                except (ValueError, AttributeError):
                                    # If conversion fails, keep as string
                                    clean_value = value

                            clean_row[clean_key] = clean_value

                        data.append(clean_row)
                except Exception as e:
                    print(f"Warning: Error processing rows in {filename}: {e}")
                    print(f"Attempting to continue with partial data...")

            # Write to JSON file
            with open(json_path, 'w', encoding=encoding) as jsonfile:
                indent = 2 if pretty_print else None
                json.dump(data, jsonfile, indent=indent, ensure_ascii=False)

            # Get file sizes for comparison
            original_size = os.path.getsize(csv_path) / 1024  # KB
            json_size = os.path.getsize(json_path) / 1024  # KB

            print(f"Converted: {filename} → {name_without_ext}.json")
            print(f"  Size: {original_size:.1f}KB → {json_size:.1f}KB")
            print(f"  Records: {len(data)}")

        except Exception as e:
            print(f"Error converting {csv_path}: {e}")

    print("\nConversion complete!")
    print(f"JSON files saved to: {output_folder}")


if __name__ == "__main__":
    # Your specified folder path
    source_folder = r"path/to/your/csv/files"

    # Convert CSV files to JSON (with pretty printing for readability)
    convert_csv_to_json(source_folder, pretty_print=True)

    print("\nPress Enter to exit...")
    input()