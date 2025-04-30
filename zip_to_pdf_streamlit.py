# <-------for single zipfile--->
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


# import streamlit as st
# from io import BytesIO
# import zipfile
# import os
# import re
# from PIL import Image
# from PyPDF2 import PdfMerger
# import shutil  # For removing temporary directories

# # Helper function to extract numeric parts from filenames
# def extract_number(filename):
#     """Extract the numerical part of the filename."""
#     match = re.search(r'(\d+)', filename)
#     return int(match.group(1)) if match else float('inf')

# # Helper function to process and resize an image to A4 portrait size
# def process_and_resize_to_a4(image_path):
#     """Resize an image to fit within A4 size (595x842 points in portrait)."""
#     A4_WIDTH, A4_HEIGHT = 595, 842  # A4 size in points
#     with Image.open(image_path) as img:
#         img = img.convert("RGB")  # Ensure image is in RGB format

#         # Check if the image is in landscape
#         if img.width > img.height:
#             # Swap dimensions to make it portrait
#             img = img.rotate(90, expand=True)

#         # Resize image to fit within A4 dimensions
#         img.thumbnail((A4_WIDTH, A4_HEIGHT), Image.Resampling.LANCZOS)

#         # Create a blank A4 canvas
#         a4_canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
#         # Center the image on the A4 canvas
#         x_offset = (A4_WIDTH - img.width) // 2
#         y_offset = (A4_HEIGHT - img.height) // 2
#         a4_canvas.paste(img, (x_offset, y_offset))

#         return a4_canvas
      
# # Helper function to convert images to PDF
# def convert_images_to_pdf(image_files):
#     """Convert a list of images to a single PDF in A4 portrait size."""
#     pdf_images = []

#     # Process and resize images
#     for image_path in image_files:
#         if not os.path.exists(image_path):
#             continue  # Skip missing files
#         a4_image = process_and_resize_to_a4(image_path)
#         pdf_images.append(a4_image)

#     # Save the images to a single PDF (in memory)
#     pdf_buffer = BytesIO()
#     pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
#     pdf_buffer.seek(0)

#     return pdf_buffer

# # Streamlit app
# def main():
#     st.title("ZIP to PDF Converter with A4 Portrait Pages")
#     st.write(
#         "Upload 1 to 5 ZIP files containing images. Rearrange the ZIP file order, and we'll create a PDF based on your selection. "
#         "The first ZIP file's name will be used for the PDF. All images will be resized to A4 portrait size."
#     )

#     # File upload (accept multiple ZIP files)
#     uploaded_files = st.file_uploader("Upload ZIP files", type=["zip"], accept_multiple_files=True)

#     if uploaded_files:
#         if len(uploaded_files) < 1 or len(uploaded_files) > 5:
#             st.error("Please upload between 1 and 5 ZIP files.")
#             return

#         # Display uploaded ZIP files for reordering
#         zip_names = [uploaded_file.name for uploaded_file in uploaded_files]
#         ordered_zip_names = st.multiselect("Reorder ZIP files:", zip_names, default=zip_names)

#         if len(ordered_zip_names) != len(uploaded_files):
#             st.error("Please select all uploaded ZIP files in your desired order.")
#             return

#         temp_dir = "temp_images"
#         os.makedirs(temp_dir, exist_ok=True)

#         try:
#             # List to store all PDFs to be merged
#             pdf_merger = PdfMerger()

#             # Iterate over the reordered ZIP files
#             for zip_name in ordered_zip_names:
#                 # Get the corresponding uploaded file object
#                 uploaded_file = next(file for file in uploaded_files if file.name == zip_name)

#                 # Create a unique directory for the current ZIP file
#                 current_temp_dir = os.path.join(temp_dir, zip_name)
#                 os.makedirs(current_temp_dir, exist_ok=True)

#                 all_image_files = []

#                 # Extract images from the current ZIP file
#                 with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
#                     zip_ref.extractall(current_temp_dir)

#                 # Collect valid image files from the current ZIP
#                 for f in os.listdir(current_temp_dir):
#                     file_path = os.path.join(current_temp_dir, f)
#                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')) and 'final' not in f.lower():
#                         all_image_files.append(file_path)

#                 # Sort files numerically based on filenames
#                 all_image_files = sorted(all_image_files, key=lambda x: extract_number(os.path.basename(x)))

#                 if not all_image_files:
#                     st.error(f"No valid images found in {zip_name}.")
#                     continue

#                 # Convert images to PDF for the current ZIP file
#                 pdf_buffer = convert_images_to_pdf(all_image_files)

#                 # Merge the current PDF into the final merged PDF
#                 pdf_merger.append(pdf_buffer)

#                 # Cleanup temporary files for the current ZIP
#                 shutil.rmtree(current_temp_dir)

#             # Final merged PDF
#             final_pdf_buffer = BytesIO()
#             pdf_merger.write(final_pdf_buffer)
#             final_pdf_buffer.seek(0)

#             # Use the first reordered ZIP file's name for the final PDF
#             final_pdf_filename = f"{ordered_zip_names[0].rsplit('.', 1)[0]}.pdf"

#             # Cleanup temp directory
#             shutil.rmtree(temp_dir)

#             # Download button for the generated PDF
#             st.success(f"PDF successfully created: {final_pdf_filename}")
#             st.download_button(
#                 label="Download PDF",
#                 data=final_pdf_buffer,
#                 file_name=final_pdf_filename,
#                 mime="application/pdf"
#             )

#         except zipfile.BadZipFile:
#             st.error("Invalid ZIP file format. Please upload valid ZIP files.")
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#         finally:
#             # Ensure temp directory cleanup
#             if os.path.exists(temp_dir):
#                 shutil.rmtree(temp_dir)

# if __name__ == "__main__":
#     main()

# import streamlit as st
# from io import BytesIO
# import zipfile
# import os
# import re
# from PIL import Image
# from PyPDF2 import PdfMerger

# # Constants for A4 size in pixels (assuming 72 DPI)
# A4_WIDTH = 595
# A4_HEIGHT = 842

# # Helper function to extract numeric parts from filenames
# def extract_number(filename):
#     """Extract the numerical part of the filename."""
#     match = re.search(r'(\d+)', filename)
#     return int(match.group(1)) if match else float('inf')

# # Helper function to resize an image to fit A4 size
# def resize_to_a4(image_path):
#     """Resize an image to fit within A4 size, maintaining orientation."""
#     with Image.open(image_path) as img:
#         img = img.convert("RGB")  # Ensure RGB format
#         original_width, original_height = img.size

#         # Check if the image is landscape or portrait
#         if original_width > original_height:  # Portrait
#             # Resize to fit portrait A4 size
#             img.thumbnail((A4_HEIGHT, A4_WIDTH), Image.Resampling.LANCZOS)
#             new_img = Image.new("RGB", (A4_HEIGHT, A4_WIDTH), (255, 255, 255))
#             new_img.paste(img, ((A4_HEIGHT - img.width) // 2, (A4_WIDTH - img.height) // 2))

#         else:  #  Landscape
#             # Resize to fit landscape A4 size
#             img.thumbnail((A4_WIDTH, A4_HEIGHT), Image.Resampling.LANCZOS)
#             new_img = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
#             new_img.paste(img, ((A4_WIDTH - img.width) // 2, (A4_HEIGHT - img.height) // 2))

#         return new_img

# # Helper function to convert images to a single PDF
# def convert_images_to_pdf(image_files):
#     """Convert a list of images to a single PDF with A4 size pages."""
#     pdf_images = []

#     # Process and resize images
#     for image_path in image_files:
#         resized_img = resize_to_a4(image_path)
#         pdf_images.append(resized_img)

#     # Save the images to a single PDF (in memory)
#     pdf_buffer = BytesIO()
#     pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
#     pdf_buffer.seek(0)

#     return pdf_buffer

# # Streamlit app
# def main():
#     st.title("ZIP to PDF Converter")
#     st.write("Upload 1 to 15 ZIP files containing images. Rearrange the ZIP file order, and we'll create a PDF based on your selection. The first ZIP file's name will be used for the PDF.")

#     # File upload (accept multiple ZIP files)
#     uploaded_files = st.file_uploader("Upload ZIP files", type=["zip"], accept_multiple_files=True)

#     if uploaded_files:
#         if len(uploaded_files) < 1 or len(uploaded_files) > 15:
#             st.error("Please upload between 1 and 15 ZIP files.")
#             return

#         # Display uploaded ZIP files for reordering
#         zip_names = [uploaded_file.name for uploaded_file in uploaded_files]
#         ordered_zip_names = st.multiselect("Reorder ZIP files:", zip_names, default=zip_names)

#         if len(ordered_zip_names) != len(uploaded_files):
#             st.error("Please select all uploaded ZIP files in your desired order.")
#             return

#         temp_dir = "temp_images"
#         os.makedirs(temp_dir, exist_ok=True)

#         try:
#             # List to store all PDFs to be merged
#             pdf_merger = PdfMerger()

#             # Iterate over the reordered ZIP files
#             for zip_name in ordered_zip_names:
#                 # Get the corresponding uploaded file object
#                 uploaded_file = next(file for file in uploaded_files if file.name == zip_name)
#                 all_image_files = []

#                 # Extract images from the current ZIP file
#                 with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
#                     zip_ref.extractall(temp_dir)

#                 # Collect valid image files from the current ZIP
#                 for f in os.listdir(temp_dir):
#                     file_path = os.path.join(temp_dir, f)
#                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp','.tiff', '.webp'))and 'final' not in f.lower():
#                         all_image_files.append(file_path)

#                 # Sort files numerically based on filenames
#                 all_image_files = sorted(all_image_files, key=lambda x: extract_number(os.path.basename(x)))

#                 if not all_image_files:
#                     st.error(f"No valid images found in {zip_name}.")
#                     continue

#                 # Convert images to PDF for the current ZIP file
#                 pdf_buffer = convert_images_to_pdf(all_image_files)

#                 # Merge the current PDF into the final merged PDF
#                 pdf_merger.append(pdf_buffer)

#                 # Cleanup temporary files for the current ZIP
#                 for f in os.listdir(temp_dir):
#                     os.remove(os.path.join(temp_dir, f))

#             # Final merged PDF
#             final_pdf_buffer = BytesIO()
#             pdf_merger.write(final_pdf_buffer)
#             final_pdf_buffer.seek(0)

#             # Use the first reordered ZIP file's name for the final PDF
#             final_pdf_filename = f"{ordered_zip_names[0].rsplit('.', 1)[0]}.pdf"

#             # Cleanup temp directory
#             os.rmdir(temp_dir)

#             # Download button for the generated PDF
#             st.success(f"PDF successfully created: {final_pdf_filename}")
#             st.download_button(
#                 label="Download PDF",
#                 data=final_pdf_buffer,
#                 file_name=final_pdf_filename,
#                 mime="application/pdf"
#             )

#         except zipfile.BadZipFile:
#             st.error("Invalid ZIP file format. Please upload valid ZIP files.")
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")

# if __name__ == "__main__":
#     main()
# <------------>

# import streamlit as st
# from io import BytesIO
# import zipfile
# import os
# import re
# import shutil
# from PIL import Image, ImageOps,ImageFile
# from PyPDF2 import PdfMerger

# ImageFile.LOAD_TRUNCATED_IMAGES = True

# # Helper function to extract numeric parts from filenames
# def extract_number(filename):
#     """Extract the numerical part of the filename."""
#     match = re.search(r'(\d+)', filename)
#     return int(match.group(1)) if match else float('inf')

# # Helper function to process and resize an image to fit A4 size
# def process_and_resize_image(image_path):
#     """Resize an image to fit within A4 dimensions, maintaining aspect ratio."""
#     A4_WIDTH = 595
#     A4_HEIGHT = 842
#     with Image.open(image_path) as img:
#         img = img.convert("RGB")  # Ensure RGB format
#         original_width, original_height = img.size

#         # Check if the image is landscape or portrait
#         if original_width > original_height:  # Portrait
#             # Resize to fit portrait A4 size
#             img.thumbnail((A4_HEIGHT, A4_WIDTH), Image.Resampling.LANCZOS)
#             canvas = Image.new("RGB", (A4_HEIGHT, A4_WIDTH), (255, 255, 255))
#             canvas.paste(img, ((A4_HEIGHT - img.width) // 2, (A4_WIDTH - img.height) // 2))

#         else:  #  Landscape
#             # Resize to fit landscape A4 size
#             img.thumbnail((A4_WIDTH, A4_HEIGHT), Image.Resampling.LANCZOS)
#             canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
#             canvas.paste(img, ((A4_WIDTH - img.width) // 2, (A4_HEIGHT - img.height) // 2))

#         return canvas

# # Helper function to convert images to PDF
# def convert_images_to_pdf(image_files):
#     """Convert a list of images to a single PDF."""
#     pdf_images = []
#     for image_path in image_files:
#         img = process_and_resize_image(image_path)
#         pdf_images.append(img)

#     # Save the images to a single PDF (in memory)
#     pdf_buffer = BytesIO()
#     pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:], quality=99)
#     pdf_buffer.seek(0)

#     return pdf_buffer

# # Streamlit app
# def main():
#     st.title("ZIP to PDF Converter")
#     st.write("Upload 1 to 15 ZIP files containing images. Rearrange the ZIP file order, and we'll create a PDF based on your selection. The first ZIP file's name will be used for the PDF.")

#     # File upload (accept multiple ZIP files)
#     uploaded_files = st.file_uploader("Upload ZIP files", type=["zip"], accept_multiple_files=True)

#     if uploaded_files:
#         if len(uploaded_files) < 1 or len(uploaded_files) > 15:
#             st.error("Please upload between 1 and 15 ZIP files.")
#             return

#         # Display uploaded ZIP files for reordering
#         zip_names = [uploaded_file.name for uploaded_file in uploaded_files]
#         ordered_zip_names = st.multiselect("Reorder ZIP files:", zip_names, default=zip_names)

#         if len(ordered_zip_names) != len(uploaded_files):
#             st.error("Please select all uploaded ZIP files in your desired order.")
#             return

#         temp_dir = "temp_images"
#         os.makedirs(temp_dir, exist_ok=True)

#         try:
#             # List to store all PDFs to be merged
#             pdf_merger = PdfMerger()

#             # Iterate over the reordered ZIP files
#             for zip_name in ordered_zip_names:
#                 # Get the corresponding uploaded file object
#                 uploaded_file = next(file for file in uploaded_files if file.name == zip_name)
#                 all_image_files = []

#                 # Extract images from the current ZIP file
#                 with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
#                     zip_ref.extractall(temp_dir)

#                 # Collect valid image files from the current ZIP
#                 for f in os.listdir(temp_dir):
#                     file_path = os.path.join(temp_dir, f)
#                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp','.tiff', '.webp')) and 'final' not in f.lower():
#                         all_image_files.append(file_path)

#                 # Sort files numerically based on filenames
#                 all_image_files = sorted(all_image_files, key=lambda x: extract_number(os.path.basename(x)))

#                 if not all_image_files:
#                     st.error(f"No valid images found in {zip_name}.")
#                     continue

#                 # Convert images to PDF for the current ZIP file
#                 pdf_buffer = convert_images_to_pdf(all_image_files)

#                 # Merge the current PDF into the final merged PDF
#                 pdf_merger.append(pdf_buffer)

#                 # Cleanup temporary files for the current ZIP
#                 for f in os.listdir(temp_dir):
#                     os.remove(os.path.join(temp_dir, f))

#             # Final merged PDF
#             final_pdf_buffer = BytesIO()
#             pdf_merger.write(final_pdf_buffer)
#             final_pdf_buffer.seek(0)

#             # Use the first reordered ZIP file's name for the final PDF
#             final_pdf_filename = f"{ordered_zip_names[0].rsplit('.', 1)[0]}.pdf"

#             # Cleanup temp directory
#             shutil.rmtree(temp_dir)

#             # Download button for the generated PDF
#             st.success(f"PDF successfully created: {final_pdf_filename}")
#             st.download_button(
#                 label="Download PDF",
#                 data=final_pdf_buffer,
#                 file_name=final_pdf_filename,
#                 mime="application/pdf"
#             )

#         except zipfile.BadZipFile:
#             st.error("Invalid ZIP file format. Please upload valid ZIP files.")
#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#         finally:
#             if os.path.exists(temp_dir):
#                 shutil.rmtree(temp_dir)

# if __name__ == "__main__":
#     main() 

# with resize option orginal or A4<------->
import streamlit as st
from io import BytesIO
import zipfile
import os
import re
import shutil
from PIL import Image, ImageFile
from PyPDF2 import PdfMerger

ImageFile.LOAD_TRUNCATED_IMAGES = True

# Helper function to extract numeric parts from filenames
def extract_number(filename):
    """Extract the numerical part of the filename."""
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')

# Helper function to process and resize an image to fit A4 size
def process_and_resize_image(image_path):
    """Resize an image to fit within A4 dimensions, maintaining aspect ratio."""
    A4_WIDTH = 595
    A4_HEIGHT = 842
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Ensure RGB format
        original_width, original_height = img.size

        # Check if the image is landscape or portrait
        if original_width > original_height:  # Portrait
            # Resize to fit portrait A4 size
            img.thumbnail((A4_HEIGHT, A4_WIDTH), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (A4_HEIGHT, A4_WIDTH), (255, 255, 255))
            canvas.paste(img, ((A4_HEIGHT - img.width) // 2, (A4_WIDTH - img.height) // 2))

        else:  # Landscape
            # Resize to fit landscape A4 size
            img.thumbnail((A4_WIDTH, A4_HEIGHT), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), (255, 255, 255))
            canvas.paste(img, ((A4_WIDTH - img.width) // 2, (A4_HEIGHT - img.height) // 2))

        return canvas

# Helper function to convert images to PDF
def convert_images_to_pdf(image_files, retain_original_size):
    """Convert a list of images to a single PDF, optionally resizing."""
    pdf_images = []
    for image_path in image_files:
        if retain_original_size:
            with Image.open(image_path) as img:
                img = img.convert("RGB")  # Ensure RGB format
                pdf_images.append(img)
        else:
            img = process_and_resize_image(image_path)
            pdf_images.append(img)

    # Save the images to a single PDF (in memory)
    pdf_buffer = BytesIO()
    pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:], quality=99)
    pdf_buffer.seek(0)

    return pdf_buffer

# Streamlit app
def main():
    st.title("ZIP to PDF Converter")
    st.write("Upload 1 to 15 ZIP files containing images. Rearrange the ZIP file order, and we'll create a PDF based on your selection. The first ZIP file's name will be used for the PDF.")

    # File upload (accept multiple ZIP files)
    uploaded_files = st.file_uploader("Upload ZIP files", type=["zip"], accept_multiple_files=True)

    # Option to retain original image size
    retain_original_size = st.checkbox("Retain original image size (Do not resize to A4)")

    if uploaded_files:
        if len(uploaded_files) < 1 or len(uploaded_files) > 15:
            st.error("Please upload between 1 and 15 ZIP files.")
            return

        # Display uploaded ZIP files for reordering
        zip_names = [uploaded_file.name for uploaded_file in uploaded_files]
        ordered_zip_names = st.multiselect("Reorder ZIP files:", zip_names, default=zip_names)

        if len(ordered_zip_names) != len(uploaded_files):
            st.error("Please select all uploaded ZIP files in your desired order.")
            return

        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            # List to store all PDFs to be merged
            pdf_merger = PdfMerger()

            # Iterate over the reordered ZIP files
            for zip_name in ordered_zip_names:
                # Get the corresponding uploaded file object
                uploaded_file = next(file for file in uploaded_files if file.name == zip_name)
                all_image_files = []

                # Extract images from the current ZIP file
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Collect valid image files from the current ZIP
                # for f in os.listdir(temp_dir):
                #     file_path = os.path.join(temp_dir, f)
                #     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and 'final' not in f.lower():
                #         all_image_files.append(file_path)

                # # Sort files numerically based on filenames
                # all_image_files = sorted(all_image_files, key=lambda x: extract_number(os.path.basename(x)))
                # Collect valid image files from the current ZIP
                image_files_temp = []
                for f in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, f)
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')) and 'final' not in f.lower():
                        image_files_temp.append(file_path)
                
                # Sort files numerically
                image_files_temp = sorted(image_files_temp, key=lambda x: extract_number(os.path.basename(x)))
                
                if not image_files_temp:
                    st.error(f"No valid images found in {zip_name}.")
                    continue
                
                # Show images with checkboxes for deletion
                st.subheader(f"Select images to REMOVE from: {zip_name}")
                images_to_keep = []
                cols = st.columns(4)
                
                for idx, image_path in enumerate(image_files_temp):
                    with cols[idx % 4]:
                        st.image(image_path, caption=os.path.basename(image_path), use_container_width=True)
                        keep = not st.checkbox(f"Remove", key=f"{zip_name}_{os.path.basename(image_path)}")
                        if keep:
                            images_to_keep.append(image_path)
                
                if not images_to_keep:
                    st.warning(f"All images from {zip_name} were removed.")
                    continue
                
                # Proceed only with images the user wants to keep
                all_image_files = images_to_keep

                if not all_image_files:
                    st.error(f"No valid images found in {zip_name}.")
                    continue

                # Convert images to PDF for the current ZIP file
                pdf_buffer = convert_images_to_pdf(all_image_files, retain_original_size)

                # Merge the current PDF into the final merged PDF
                pdf_merger.append(pdf_buffer)

                # Cleanup temporary files for the current ZIP
                for f in os.listdir(temp_dir):
                    os.remove(os.path.join(temp_dir, f))

            # Final merged PDF
            final_pdf_buffer = BytesIO()
            pdf_merger.write(final_pdf_buffer)
            final_pdf_buffer.seek(0)

            # Use the first reordered ZIP file's name for the final PDF
            final_pdf_filename = f"{ordered_zip_names[0].rsplit('.', 1)[0]}.pdf"

            # Cleanup temp directory
            shutil.rmtree(temp_dir)

            # Download button for the generated PDF
            st.success(f"PDF successfully created: {final_pdf_filename}")
            st.download_button(
                label="Download PDF",
                data=final_pdf_buffer,
                file_name=final_pdf_filename,
                mime="application/pdf"
            )

        except zipfile.BadZipFile:
            st.error("Invalid ZIP file format. Please upload valid ZIP files.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
