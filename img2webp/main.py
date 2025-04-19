import os
from PIL import Image
import glob


def convert_images_to_webp(source_folder, quality=80):
    """
    Convert all popular image formats in a folder to WebP format with optimization.

    Args:
        source_folder (str): Path to the folder containing images
        quality (int): WebP quality (0-100), lower means smaller file size
    """
    # Ensure the source folder exists
    if not os.path.exists(source_folder):
        print(f"Error: Source folder '{source_folder}' not found.")
        return

    # Create a 'webp_converted' subfolder if it doesn't exist
    output_folder = os.path.join(source_folder, "webp_converted")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # List of popular image extensions to convert
    extensions = [
        '*.jpg', '*.jpeg', '*.JPG', '*.JPEG',
        '*.png', '*.PNG',
        '*.bmp', '*.BMP',
        '*.gif', '*.GIF',
        '*.tiff', '*.tif', '*.TIFF', '*.TIF',
        '*.jfif', '*.JFIF',
        '*.heic', '*.HEIC',
        '*.webp', '*.WEBP'  # Including existing webp for re-optimization
    ]

    # Get all image files in the source folder
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(source_folder, ext)))

    # Remove duplicates (in case of case-insensitive file systems)
    image_files = list(set(image_files))

    if not image_files:
        print(f"No image files found in '{source_folder}'.")
        return

    print(f"Found {len(image_files)} images to convert.")

    # Convert each image to WebP
    for img_path in image_files:
        try:
            # Get the filename without extension
            filename = os.path.basename(img_path)
            name_without_ext = os.path.splitext(filename)[0]

            # Set the output path with WebP extension
            webp_path = os.path.join(output_folder, f"{name_without_ext}.webp")

            # Skip if it's a WebP file with the same path as destination
            if img_path.lower().endswith('.webp') and os.path.normpath(img_path) == os.path.normpath(webp_path):
                print(f"Skipping: {filename} (already WebP)")
                continue

            # Open and convert the image
            img = Image.open(img_path)

            # Handle animated GIFs
            if img_path.lower().endswith('.gif') and getattr(img, 'is_animated', False):
                print(f"Note: {filename} is an animated GIF. WebP conversion will maintain animation.")
                # For animated GIFs, we need different handling
                try:
                    img.save(webp_path, 'WEBP', quality=quality, method=6, save_all=True,
                             optimize=True, append_images=list(img.copy() for i in range(1, img.n_frames)),
                             duration=img.info.get('duration', 100), loop=0)
                except Exception as e:
                    print(f"  Error converting animated GIF {filename}: {e}")
                    continue
            else:
                # Convert to RGB if image has an alpha channel (except for PNG which should keep transparency)
                if img.mode == 'RGBA' and not img_path.lower().endswith('.png'):
                    img = img.convert('RGB')
                elif img.mode in ('LA', 'CMYK', 'P'):
                    if img.mode == 'P' and img_path.lower().endswith('.png') and img.info.get(
                            'transparency') is not None:
                        # Handle indexed PNGs with transparency
                        img = img.convert('RGBA')
                    else:
                        img = img.convert('RGB')

                # Save as WebP with specified quality
                img.save(webp_path, 'WEBP', quality=quality, method=6)

            # Get file sizes for comparison
            original_size = os.path.getsize(img_path) / 1024  # KB
            webp_size = os.path.getsize(webp_path) / 1024  # KB
            reduction = (1 - webp_size / original_size) * 100  # percentage

            print(f"Converted: {filename} → {name_without_ext}.webp")
            print(f"  Size reduction: {original_size:.1f}KB → {webp_size:.1f}KB ({reduction:.1f}% smaller)")

        except Exception as e:
            print(f"Error converting {img_path}: {e}")

    print("\nConversion complete!")
    print(f"WebP images saved to: {output_folder}")


if __name__ == "__main__":
    # Your specified folder path
    source_folder = r"-----------Need-to-get-folder-path--------------"

    # You can adjust the quality parameter (0-100) for different size/quality trade-offs
    # Lower values = smaller files but lower quality
    convert_images_to_webp(source_folder, quality=85)

    print("\nPress Enter to exit...")
    input()