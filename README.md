![image](https://github.com/user-attachments/assets/812d2958-ac52-458f-a74c-1f83c1165bc0)

![image](https://github.com/user-attachments/assets/1d6d906a-fd59-4c09-a6ce-af9d9a811bd7)


Hosted website Link ="https://ziptopdfconvertor.streamlit.app/"


### **1. Library Imports:**
- **Streamlit (`st`)**: For creating the web interface.
- **`BytesIO`**: To handle in-memory binary streams.
- **`zipfile`**: For handling ZIP files.
- **`os` & `shutil`**: For file operations and temporary directory management.
- **`re`**: For extracting numeric parts from filenames.
- **`PIL (Pillow)`**: For image processing.
- **`PyPDF2.PdfMerger`**: For merging PDFs.

---

### **2. Helper Functions:**

#### **Extract Number:**
```python
def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else float('inf')
```
- Extracts numeric values from filenames for sorting.

---

#### **Resize Image to A4:**
```python
def process_and_resize_to_a4(image_path):
    A4_WIDTH, A4_HEIGHT = 595, 842
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        if img.width > img.height:
            img = img.rotate(90, expand=True)
        img.thumbnail((A4_WIDTH, A4_HEIGHT), Image.ANTIALIAS)
        a4_canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
        x_offset = (A4_WIDTH - img.width) // 2
        y_offset = (A4_HEIGHT - img.height) // 2
        a4_canvas.paste(img, (x_offset, y_offset))
        return a4_canvas
```
- Resizes images to fit within A4 dimensions (595x842 points).

---

#### **Convert Images to PDF:**
```python
def convert_images_to_pdf(image_files):
    pdf_images = []
    for image_path in image_files:
        if not os.path.exists(image_path):
            continue
        a4_image = process_and_resize_to_a4(image_path)
        pdf_images.append(a4_image)
    pdf_buffer = BytesIO()
    pdf_images[0].save(pdf_buffer, format="PDF", save_all=True, append_images=pdf_images[1:])
    pdf_buffer.seek(0)
    return pdf_buffer
```
- Converts a list of images into a single PDF in A4 format.

---

### **3. Main Function:**

#### **User Interface:**
```python
uploaded_files = st.file_uploader("Upload ZIP files", type=["zip"], accept_multiple_files=True)
zip_names = [uploaded_file.name for uploaded_file in uploaded_files]
ordered_zip_names = st.multiselect("Reorder ZIP files:", zip_names, default=zip_names)
```
- Allows users to upload and reorder ZIP files.

---

#### **File Extraction and Conversion:**
```python
for zip_name in ordered_zip_names:
    uploaded_file = next(file for file in uploaded_files if file.name == zip_name)
    current_temp_dir = os.path.join(temp_dir, zip_name)
    os.makedirs(current_temp_dir, exist_ok=True)
    all_image_files = []
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall(current_temp_dir)
    for f in os.listdir(current_temp_dir):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
            all_image_files.append(os.path.join(current_temp_dir, f))
    all_image_files = sorted(all_image_files, key=lambda x: extract_number(os.path.basename(x)))
    pdf_buffer = convert_images_to_pdf(all_image_files)
    pdf_merger.append(pdf_buffer)
    shutil.rmtree(current_temp_dir)
```
- Extracts and processes images from each ZIP file, then converts them into PDFs.

---

#### **Final PDF Creation:**
```python
final_pdf_buffer = BytesIO()
pdf_merger.write(final_pdf_buffer)
final_pdf_buffer.seek(0)
final_pdf_filename = f"{ordered_zip_names[0].rsplit('.', 1)[0]}.pdf"
shutil.rmtree(temp_dir)
st.download_button(
    label="Download PDF",
    data=final_pdf_buffer,
    file_name=final_pdf_filename,
    mime="application/pdf"
)
```
- Merges all PDFs and provides a download button for the final PDF.

---

### **Error Handling & Cleanup:**
- Ensures invalid ZIP files or missing images are handled gracefully.
- Cleans up temporary directories after processing. 

---

This app is ideal for users looking to convert multiple ZIP files containing images into a single PDF file with A4 page formatting in a Streamlit interface.
