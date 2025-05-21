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
                # Let user enter a range of image numbers to remove
                remove_range_input = st.text_input(
                    f"Enter image numbers to remove from {zip_name} (e.g. 2,5,10-12):", key=f"range_input_{zip_name}"
                )
                if not image_files_temp:
                    st.error(f"No valid images found in {zip_name}.")
                    continue
                # Parse removal range
                def parse_ranges(input_str):
                    removal_indices = set()
                    parts = input_str.split(',')
                    for part in parts:
                        if '-' in part:
                            start, end = part.split('-')
                            if start.strip().isdigit() and end.strip().isdigit():
                                removal_indices.update(range(int(start.strip()), int(end.strip()) + 1))
                        elif part.strip().isdigit():
                            removal_indices.add(int(part.strip()))
                    return removal_indices
                
                removal_indices = parse_ranges(remove_range_input)
                # Show images with checkboxes for deletion and page numbers
                st.subheader(f"Review images from {zip_name}")
                images_to_keep = []
                cols = st.columns(4)
                
                for idx, image_path in enumerate(image_files_temp):
                    page_number = idx + 1  # Page numbers start at 1
                    remove_by_range = page_number in removal_indices
                
                    with cols[idx % 4]:
                        st.image(image_path, caption=f"Page {page_number}: {os.path.basename(image_path)}", use_container_width=True)
                        remove = st.checkbox("Remove", key=f"{zip_name}_{os.path.basename(image_path)}", value=remove_by_range)
                        if not remove:
                            images_to_keep.append(image_path)
                
                if not images_to_keep:
                    st.warning(f"All images from {zip_name} were removed.")
                    continue
                
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
