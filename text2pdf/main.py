import os
import glob
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch


def convert_text_to_pdf(source_folder, font_name="Courier", font_size=12, margin=0.5):
    """
    Convert all text files in a folder to PDF format.

    Args:
        source_folder (str): Path to the folder containing text files
        font_name (str): Name of the font to use
        font_size (int): Font size in points
        margin (float): Margin in inches
    """
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' not found.")
        return

    # Create a 'pdf_converted' subfolder if it doesn't exist
    output_folder = os.path.join(source_folder, "pdf_converted")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # List of text file extensions to convert
    extensions = ['*.txt', '*.TXT', '*.text', '*.md', '*.MD', '*.markdown']

    # Get all text files in the source folder
    text_files = []
    for ext in extensions:
        text_files.extend(glob.glob(os.path.join(source_folder, ext)))

    # Remove duplicates (in case of case-insensitive file systems)
    text_files = list(set(text_files))

    if not text_files:
        print(f"No text files found in '{source_folder}'.")
        return

    print(f"Found {len(text_files)} text files to convert.")

    # Register fonts (optional, using system defaults if not available)
    try:
        pdfmetrics.registerFont(TTFont('Courier', 'Courier.ttf'))
    except:
        print("Default Courier font not registered, using system defaults.")

    # Convert each text file to PDF
    for text_path in text_files:
        try:
            # Get the filename without extension
            filename = os.path.basename(text_path)
            name_without_ext = os.path.splitext(filename)[0]

            # Set the output path with PDF extension
            pdf_path = os.path.join(output_folder, f"{name_without_ext}.pdf")

            # Read the text file
            with open(text_path, 'r', encoding='utf-8') as file:
                text_content = file.readlines()

            # Create a PDF file
            pdf = canvas.Canvas(pdf_path, pagesize=A4)
            pdf.setFont(font_name, font_size)

            # Get page dimensions
            width, height = A4
            margin_pixels = margin * inch
            x_position = margin_pixels
            y_position = height - margin_pixels
            line_height = font_size * 1.2  # 1.2 is a typical line spacing factor

            # Write text to PDF
            for line in text_content:
                # Check if we need a new page
                if y_position < margin_pixels + line_height:
                    pdf.showPage()
                    pdf.setFont(font_name, font_size)
                    y_position = height - margin_pixels

                # Write the line
                pdf.drawString(x_position, y_position, line.rstrip('\n'))
                y_position -= line_height

            # Save the PDF file
            pdf.save()

            # Get file sizes for comparison
            original_size = os.path.getsize(text_path) / 1024  # KB
            pdf_size = os.path.getsize(pdf_path) / 1024  # KB

            print(f"Converted: {filename} → {name_without_ext}.pdf")
            print(f"  Size: {original_size:.1f}KB → {pdf_size:.1f}KB")

        except Exception as e:
            print(f"Error converting {text_path}: {e}")

    print("\nConversion complete!")
    print(f"PDF files saved to: {output_folder}")


if __name__ == "__main__":
    # Your specified folder path
    source_folder = r"path/to/your/text/files"

    # Convert text files to PDF
    convert_text_to_pdf(source_folder)

    print("\nPress Enter to exit...")
    input()