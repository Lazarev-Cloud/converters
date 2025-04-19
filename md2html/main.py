import os
import glob
import markdown
from bs4 import BeautifulSoup


def convert_markdown_to_html(source_folder, theme="default"):
    """
    Convert all markdown files in a folder to HTML format.

    Args:
        source_folder (str): Path to the folder containing markdown files
        theme (str): CSS theme to apply ('default', 'github', 'dark')
    """
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' not found.")
        return

    # Create a 'html_converted' subfolder if it doesn't exist
    output_folder = os.path.join(source_folder, "html_converted")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # List of markdown file extensions to convert
    extensions = ['*.md', '*.MD', '*.markdown', '*.MARKDOWN']

    # Get all markdown files in the source folder
    md_files = []
    for ext in extensions:
        md_files.extend(glob.glob(os.path.join(source_folder, ext)))

    # Remove duplicates (in case of case-insensitive file systems)
    md_files = list(set(md_files))

    if not md_files:
        print(f"No markdown files found in '{source_folder}'.")
        return

    print(f"Found {len(md_files)} markdown files to convert.")

    # CSS for different themes
    css_themes = {
        "default": """
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
                   line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #333; }
            h1, h2, h3, h4, h5, h6 { margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25; }
            h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
            h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
            code { padding: .2em .4em; margin: 0; font-size: 85%; background-color: rgba(27,31,35,.05); 
                   border-radius: 3px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }
            pre { padding: 16px; overflow: auto; line-height: 1.45; background-color: #f6f8fa; border-radius: 3px; }
            pre code { background-color: transparent; padding: 0; margin: 0; font-size: 100%; word-break: normal; 
                       white-space: pre; overflow: visible; line-height: inherit; word-wrap: normal; }
            blockquote { margin: 0; padding: 0 1em; color: #6a737d; border-left: .25em solid #dfe2e5; }
        """,
        "github": """
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
                   line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #24292e; }
            h1, h2, h3, h4, h5, h6 { margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25; }
            h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
            h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: .3em; }
            a { color: #0366d6; text-decoration: none; }
            a:hover { text-decoration: underline; }
            code { padding: .2em .4em; margin: 0; font-size: 85%; background-color: rgba(27,31,35,.05); 
                   border-radius: 3px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }
            pre { padding: 16px; overflow: auto; line-height: 1.45; background-color: #f6f8fa; border-radius: 3px; }
            pre code { background-color: transparent; padding: 0; margin: 0; font-size: 100%; word-break: normal; 
                       white-space: pre; overflow: visible; line-height: inherit; word-wrap: normal; }
            blockquote { margin: 0; padding: 0 1em; color: #6a737d; border-left: .25em solid #dfe2e5; }
            hr { height: .25em; padding: 0; margin: 24px 0; background-color: #e1e4e8; border: 0; }
            table { border-spacing: 0; border-collapse: collapse; margin-top: 0; margin-bottom: 16px; display: block; 
                    width: 100%; overflow: auto; }
            table th, table td { padding: 6px 13px; border: 1px solid #dfe2e5; }
            table tr { background-color: #fff; border-top: 1px solid #c6cbd1; }
            table tr:nth-child(2n) { background-color: #f6f8fa; }
        """,
        "dark": """
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; 
                   line-height: 1.6; padding: 20px; max-width: 800px; margin: 0 auto; color: #c9d1d9; 
                   background-color: #0d1117; }
            h1, h2, h3, h4, h5, h6 { margin-top: 24px; margin-bottom: 16px; font-weight: 600; line-height: 1.25; color: #e6edf3; }
            h1 { font-size: 2em; border-bottom: 1px solid #21262d; padding-bottom: .3em; }
            h2 { font-size: 1.5em; border-bottom: 1px solid #21262d; padding-bottom: .3em; }
            a { color: #58a6ff; text-decoration: none; }
            a:hover { text-decoration: underline; }
            code { padding: .2em .4em; margin: 0; font-size: 85%; background-color: rgba(110,118,129,0.4); 
                   border-radius: 3px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; color: #e6edf3; }
            pre { padding: 16px; overflow: auto; line-height: 1.45; background-color: #161b22; border-radius: 3px; }
            pre code { background-color: transparent; padding: 0; margin: 0; font-size: 100%; word-break: normal; 
                       white-space: pre; overflow: visible; line-height: inherit; word-wrap: normal; }
            blockquote { margin: 0; padding: 0 1em; color: #8b949e; border-left: .25em solid #30363d; }
            hr { height: .25em; padding: 0; margin: 24px 0; background-color: #30363d; border: 0; }
            table { border-spacing: 0; border-collapse: collapse; margin-top: 0; margin-bottom: 16px; display: block; 
                    width: 100%; overflow: auto; }
            table th, table td { padding: 6px 13px; border: 1px solid #30363d; }
            table tr { background-color: #0d1117; border-top: 1px solid #21262d; }
            table tr:nth-child(2n) { background-color: #161b22; }
        """
    }

    # Choose the CSS theme
    selected_css = css_themes.get(theme.lower(), css_themes["default"])

    # Configure Markdown extensions
    md_extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br',
        'markdown.extensions.sane_lists',
        'markdown.extensions.smart_strong'
    ]

    # Convert each markdown file to HTML
    for md_path in md_files:
        try:
            # Get the filename without extension
            filename = os.path.basename(md_path)
            name_without_ext = os.path.splitext(filename)[0]

            # Set the output path with HTML extension
            html_path = os.path.join(output_folder, f"{name_without_ext}.html")

            # Read the markdown file
            with open(md_path, 'r', encoding='utf-8') as file:
                md_content = file.read()

            # Convert Markdown to HTML
            html_content = markdown.markdown(md_content, extensions=md_extensions)

            # Create a complete HTML document
            html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name_without_ext}</title>
    <style>
        {selected_css}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

            # Beautify the HTML (optional, for better readability)
            try:
                soup = BeautifulSoup(html_doc, 'html.parser')
                html_doc = soup.prettify()
            except:
                print(f"Warning: BeautifulSoup not available for HTML prettifying, continuing without it.")

            # Write the HTML file
            with open(html_path, 'w', encoding='utf-8') as file:
                file.write(html_doc)

            # Get file sizes for comparison
            original_size = os.path.getsize(md_path) / 1024  # KB
            html_size = os.path.getsize(html_path) / 1024  # KB

            print(f"Converted: {filename} → {name_without_ext}.html")
            print(f"  Size: {original_size:.1f}KB → {html_size:.1f}KB")

        except Exception as e:
            print(f"Error converting {md_path}: {e}")

    print("\nConversion complete!")
    print(f"HTML files saved to: {output_folder}")


if __name__ == "__main__":
    # Your specified folder path
    source_folder = r"path/to/your/markdown/files"

    # Choose from 'default', 'github', or 'dark' themes
    convert_markdown_to_html(source_folder, theme="github")

    print("\nPress Enter to exit...")
    input()