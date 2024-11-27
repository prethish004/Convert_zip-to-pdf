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
# import zipfile
# import os
# from PIL import Image
# from io import BytesIO

# # Set Streamlit configuration
# st.set_page_config(page_title="Large ZIP to PDF Converter", layout="centered")

# # Function to extract numerical order from filenames
# def extract_number(filename):
#     import re
#     match = re.search(r'(\d+)', filename)
#     return int(match.group(1)) if match else float('inf')

# # Function to resize and process images for PDF
# def process_images_for_pdf(zip_file_path, output_pdf_name):
#     temp_dir = "temp_images"
#     os.makedirs(temp_dir, exist_ok=True)
#     pdf_images = []

#     try:
#         # Extract ZIP contents to the temp directory
#         with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
#             zip_ref.extractall(temp_dir)

#         # Collect image files and sort them
#         image_files = [
#             os.path.join(temp_dir, f) for f in os.listdir(temp_dir)
#             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp'))
#         ]
#         image_files.sort(key=lambda x: extract_number(os.path.basename(x)))

#         if not image_files:
#             st.error("No valid images found in the ZIP file.")
#             return None

#         # Resize images and prepare for PDF
#         for image_path in image_files:
#             with Image.open(image_path) as img:
#                 img = img.convert("RGB")
#                 # Resize to 70% of original size to save memory
#                 img = img.resize((int(img.width * 0.7), int(img.height * 0.7)))
#                 pdf_images.append(img)

#         # Save to a single PDF
#         pdf_buffer = BytesIO()
#         pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
#         pdf_buffer.seek(0)

#         # Clean up temporary directory
#         for f in os.listdir(temp_dir):
#             os.remove(os.path.join(temp_dir, f))
#         os.rmdir(temp_dir)

#         return pdf_buffer, output_pdf_name

#     except Exception as e:
#         st.error(f"Error processing images: {str(e)}")
#         return None

# # Streamlit UI
# st.title("Large ZIP to PDF Converter")
# st.write("Upload a ZIP file containing images to convert them into a single PDF.")

# # File uploader
# uploaded_file = st.file_uploader("Upload ZIP File", type=["zip"])

# if uploaded_file:
#     try:
#         # Save uploaded file temporarily
#         zip_file_path = f"temp_{uploaded_file.name}"
#         with open(zip_file_path, "wb") as temp_zip:
#             temp_zip.write(uploaded_file.read())

#         # Process the ZIP file
#         pdf_name = uploaded_file.name.rsplit('.', 1)[0] + ".pdf"
#         result = process_images_for_pdf(zip_file_path, pdf_name)

#         if result:
#             pdf_buffer, output_pdf_name = result
#             st.success(f"PDF {output_pdf_name} generated successfully!")

#             # Provide download button for the generated PDF
#             st.download_button(
#                 label="Download PDF",
#                 data=pdf_buffer,
#                 file_name=output_pdf_name,
#                 mime="application/pdf"
#             )

#         # Clean up temporary ZIP file
#         os.remove(zip_file_path)

#     except Exception as e:
#         st.error(f"Error: {str(e)}")

# import streamlit as st
# import zipfile
# import os
# from PIL import Image
# from io import BytesIO

# # Specify a larger temporary storage directory
# TEMP_DIR = "/data/temp_images"  # Adjust path based on Render disk mount
# os.makedirs(TEMP_DIR, exist_ok=True)

# # Streamlit UI setup
# st.title("Large ZIP to PDF Converter")
# st.write("Upload a ZIP file containing images to convert them into a single PDF.")

# # Function to process images into a PDF
# def process_zip_to_pdf(zip_path):
#     pdf_images = []

#     try:
#         # Extract ZIP contents
#         with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#             zip_ref.extractall(TEMP_DIR)

#         # Collect valid image files
#         image_files = [
#             os.path.join(TEMP_DIR, f)
#             for f in os.listdir(TEMP_DIR)
#             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')) and 'final' not in f.lower()
#         ]

#         if not image_files:
#             st.error("No valid images found in the ZIP file.")
#             return None

#         # Resize and process images for PDF
#         for image_file in sorted(image_files):
#             with Image.open(image_file) as img:
#                 img = img.convert("RGB")
#                 img = img.resize((int(img.width * 0.7), int(img.height * 0.7)))  # Resize to 70%
#                 pdf_images.append(img)

#         # Generate PDF in memory
#         pdf_buffer = BytesIO()
#         pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
#         pdf_buffer.seek(0)
#         return pdf_buffer

#     except Exception as e:
#         st.error(f"Error processing ZIP file: {e}")
#         return None

#     finally:
#         # Clean up temporary files
#         for root, dirs, files in os.walk(TEMP_DIR):
#             for file in files:
#                 os.remove(os.path.join(root, file))

# # Upload ZIP file
# uploaded_file = st.file_uploader("Upload ZIP File", type=["zip"])

# if uploaded_file:
#     temp_zip_path = os.path.join(TEMP_DIR, uploaded_file.name)

#     # Save uploaded file to disk
#     with open(temp_zip_path, "wb") as temp_zip:
#         temp_zip.write(uploaded_file.read())

#     pdf_buffer = process_zip_to_pdf(temp_zip_path)

#     if pdf_buffer:
#         # Provide download button
#         st.download_button(
#             label="Download PDF",
#             data=pdf_buffer,
#             file_name="converted.pdf",
#             mime="application/pdf"
#         )

import streamlit as st
import zipfile
import os
from PIL import Image
from io import BytesIO

# Use a writable directory for temporary storage (e.g., '/tmp' on Render)
TEMP_DIR = "/tmp/temp_images"  # Use '/tmp' for writable storage in cloud platforms
os.makedirs(TEMP_DIR, exist_ok=True)

# Streamlit UI setup
st.title("Large ZIP to PDF Converter")
st.write("Upload a ZIP file containing images to convert them into a single PDF.")

# Function to process images into a PDF
def process_zip_to_pdf(zip_path):
    pdf_images = []

    try:
        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TEMP_DIR)

        # Collect valid image files
        image_files = [
            os.path.join(TEMP_DIR, f)
            for f in os.listdir(TEMP_DIR)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')) and 'final' not in f.lower()
        ]

        if not image_files:
            st.error("No valid images found in the ZIP file.")
            return None

        # Resize and process images for PDF
        for image_file in sorted(image_files):
            with Image.open(image_file) as img:
                img = img.convert("RGB")
                img = img.resize((int(img.width * 0.7), int(img.height * 0.7)))  # Resize to 70%
                pdf_images.append(img)

        # Generate PDF in memory
        pdf_buffer = BytesIO()
        pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
        pdf_buffer.seek(0)
        return pdf_buffer

    except zipfile.BadZipFile:
        st.error("Invalid ZIP file format. Please upload a valid ZIP file.")
        return None

    except Exception as e:
        st.error(f"Error processing ZIP file: {e}")
        return None

    finally:
        # Clean up temporary files
        for root, dirs, files in os.walk(TEMP_DIR):
            for file in files:
                os.remove(os.path.join(root, file))

# Upload ZIP file
uploaded_file = st.file_uploader("Upload ZIP File", type=["zip"])

if uploaded_file:
    temp_zip_path = os.path.join(TEMP_DIR, uploaded_file.name)

    # Save uploaded file to disk
    with open(temp_zip_path, "wb") as temp_zip:
        temp_zip.write(uploaded_file.read())

    # Process ZIP file to convert images to PDF
    pdf_buffer = process_zip_to_pdf(temp_zip_path)

    if pdf_buffer:
        # Provide download button
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="converted.pdf",
            mime="application/pdf"
        )
