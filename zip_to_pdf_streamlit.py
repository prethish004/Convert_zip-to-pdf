# import streamlit as st
# from io import BytesIO
# import zipfile
# import os
# import re
# from PIL import Image

# # Helper function to extract numeric parts from filenames
# def extract_number(filename):
#     """Extract the numerical part of the filename."""
#     match = re.search(r'(\d+)', filename)
#     return int(match.group(1)) if match else float('inf')

# # Helper function to process and resize an image
# def process_and_resize_image(image_path, resize_factor=0.7):
#     """Open, resize, and process an image to fit within 70% of its original size."""
#     with Image.open(image_path) as img:
#         # Ensure image is in RGB format
#         img = img.convert("RGB")
        
#         # Resize the image to 70% of its original dimensions
#         original_width, original_height = img.size
#         new_width = int(original_width * resize_factor)
#         new_height = int(original_height * resize_factor)
#         img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
#         return img

# # Helper function to convert images to PDF
# def convert_images_to_pdf(image_files, zip_name, resize_factor=0.7):
#     """Convert a list of images to a single PDF."""
#     pdf_images = []

#     # Process and resize images
#     for image_path in image_files:
#         img = process_and_resize_image(image_path, resize_factor)
#         pdf_images.append(img)

#     # Save the images to a single PDF (in memory)
#     pdf_buffer = BytesIO()
#     pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
#     pdf_buffer.seek(0)

#     # Use ZIP filename for the PDF filename
#     pdf_filename = f"{zip_name}.pdf"

#     return pdf_buffer, pdf_filename

# # Streamlit app
# def main():
#     st.title("ZIP to PDF Converter")
#     st.write("Upload a ZIP file containing images, and we'll convert it into a single PDF.")

#     # File upload
#     uploaded_file = st.file_uploader("Upload ZIP file", type=["zip"])
    
#     if uploaded_file:
#         temp_dir = "temp_images"
#         os.makedirs(temp_dir, exist_ok=True)

#         try:
#             # Extract the ZIP file
#             with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
#                 zip_name = uploaded_file.name.rsplit('.', 1)[0]  # Extract ZIP name for the PDF file
#                 zip_ref.extractall(temp_dir)

#             # Collect valid image files
#             image_files = []
#             for f in os.listdir(temp_dir):
#                 file_path = os.path.join(temp_dir, f)
#                 if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')) and 'final' not in f.lower():
#                     image_files.append(file_path)

#             # Sort files numerically based on filenames
#             image_files = sorted(image_files, key=lambda x: extract_number(os.path.basename(x)))

#             if not image_files:
#                 st.error("No valid images found in the ZIP file.")
#                 return

#             # Convert images to PDF
#             pdf_buffer, pdf_filename = convert_images_to_pdf(image_files, zip_name, resize_factor=0.7)

#             # Cleanup temporary files
#             for f in os.listdir(temp_dir):
#                 os.remove(os.path.join(temp_dir, f))
#             os.rmdir(temp_dir)

#             # Download button for the generated PDF
#             st.success(f"PDF successfully created: {pdf_filename}")
#             st.download_button(
#                 label="Download PDF",
#                 data=pdf_buffer,
#                 file_name=pdf_filename,
#                 mime="application/pdf"
#             )

#         except zipfile.BadZipFile:
#             st.error("Invalid ZIP file format. Please upload a valid ZIP file.")
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()

import streamlit as st
from io import BytesIO
import zipfile
import os
import re
from PIL import Image

# Helper function to extract numeric parts from filenames
def extract_number(filename):
    """Extract the numerical part of the filename."""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

# Helper function to process and resize an image to a common size
def process_and_resize_image(image_path, max_width, max_height):
    """Open, resize, and process an image to fit within the max_width and max_height."""
    with Image.open(image_path) as img:
        # Ensure image is in RGB format
        img = img.convert("RGB")
        
        # Resize the image while maintaining aspect ratio
        img.thumbnail((max_width, max_height))
        
        return img

# Helper function to convert images to PDF
def convert_images_to_pdf(image_files, zip_name, resize_factor=0.7):
    """Convert a list of images to a single PDF."""
    pdf_images = []

    # Find maximum width and height across all images for consistent resizing
    max_width = 0
    max_height = 0
    for image_path in image_files:
        with Image.open(image_path) as img:
            max_width = max(max_width, img.width)
            max_height = max(max_height, img.height)

    # Process and resize images
    for image_path in image_files:
        img = process_and_resize_image(image_path, max_width, max_height)
        pdf_images.append(img)

    # Save the images to a single PDF (in memory)
    pdf_buffer = BytesIO()
    pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
    pdf_buffer.seek(0)

    # Use the first ZIP file name for the PDF filename
    pdf_filename = f"{zip_name}.pdf"

    return pdf_buffer, pdf_filename

# Streamlit app
def main():
    st.title("ZIP to PDF Converter")
    st.write("Upload 2 to 5 ZIP files containing images, and we'll convert them into a single PDF. The arrangement is based on your selection.")

    # File upload (accept multiple ZIP files)
    uploaded_files = st.file_uploader("Upload ZIP files", type=["zip"], accept_multiple_files=True)
    
    if uploaded_files:
        if len(uploaded_files) < 1 or len(uploaded_files) > 5:
            st.error("Please upload between 1 and 5 ZIP files.")
            return

        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # List to store image files
            all_image_files = []
            zip_name = uploaded_files[0].name.rsplit('.', 1)[0]  # Use the first ZIP file's name

            # Extract all ZIP files
            for uploaded_file in uploaded_files:
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Collect valid image files from the current ZIP
                for f in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, f)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')) and 'final' not in f.lower():
                        all_image_files.append(file_path)

            # Sort files numerically based on filenames
            all_image_files = sorted(all_image_files, key=lambda x: extract_number(os.path.basename(x)))

            if not all_image_files:
                st.error("No valid images found in the ZIP files.")
                return

            # Convert images to PDF
            pdf_buffer, pdf_filename = convert_images_to_pdf(all_image_files, zip_name)

            # Cleanup temporary files
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.rmdir(temp_dir)

            # Download button for the generated PDF
            st.success(f"PDF successfully created: {pdf_filename}")
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name=pdf_filename,
                mime="application/pdf"
            )

        except zipfile.BadZipFile:
            st.error("Invalid ZIP file format. Please upload valid ZIP files.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
