import os
import streamlit as st
from PIL import Image, ImageOps
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import time
from utils.init import initialize

# Initialize Streamlit configuration and load resources
header_content, footer_content = initialize()


def create_pdf(images):
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    
    for img in images:
        img_reader = ImageReader(img)
        img_width, img_height = img_reader.getSize()
        
        c.setPageSize((img_width, img_height))
        c.drawImage(img_reader, 0, 0, width=img_width, height=img_height)
        c.showPage()
    
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

def add_border(image, border_size=2):
    return ImageOps.expand(image, border=border_size, fill='black')

def resize_image(image, size=(300, 300)):
    return ImageOps.contain(image, size, Image.LANCZOS)

def main():
    # Right sidebar
    right_sidebar = st.sidebar
    
    # Add header content to the top of the right sidebar
    right_sidebar.markdown(header_content)
    
    if right_sidebar.button("התחל מחדש"):
        st.markdown("<script>reloadPage();</script>", unsafe_allow_html=True)
        st.session_state.clear()
        st.rerun()

    # Move "Upload Images" to right sidebar
    uploaded_files = right_sidebar.file_uploader("העלה תמונות", accept_multiple_files=True, type=['png', 'jpg', 'jpeg'], key="file_uploader")
    
    if 'images' not in st.session_state:
        st.session_state.images = []

    # Synchronize uploaded files with session state
    current_files = [img['file'] for img in st.session_state.images]
    for uploaded_file in uploaded_files:
        if uploaded_file not in current_files:
            image = Image.open(uploaded_file)
            image_resized = resize_image(image)
            image_with_border = add_border(image_resized)
            st.session_state.images.append({'file': uploaded_file, 'image': image_with_border, 'original': image})
    
    # Remove images that are no longer in uploaded_files
    st.session_state.images = [img for img in st.session_state.images if img['file'] in uploaded_files]

    # Main content area
    main_content = st.container()    
    
    main_content.title("📷➡️📄 המרת תמונות לקובץ PDF ")

    # Display images
    if st.session_state.images:
        cols = main_content.columns(3)
        for i, img_dict in enumerate(st.session_state.images):
            col = cols[i % 3]
            col.image(img_dict['image'], use_column_width=True)
            
            if i > 0:
                col.button(f"{i+1} הזז למעלה", key=f"up_{i}", on_click=lambda i=i: st.session_state.images.insert(i-1, st.session_state.images.pop(i)))

    # Create and Download PDF button
    if right_sidebar.button("צור והורד PDF"):
        if st.session_state.images:
            # Create a placeholder for the spinner
            spinner_placeholder = st.empty()
            with spinner_placeholder.container():
                st.markdown("## נא להמתין יוצר PDF...")
                progress_bar = st.progress(0)
                
                # Simulate PDF creation process
                for percent_complete in range(100):
                    time.sleep(0.05)  # Simulate work being done
                    progress_bar.progress(percent_complete + 1)
                
                # Create the actual PDF
                pdf = create_pdf([img_dict['original'] for img_dict in st.session_state.images])
            
            # Remove the spinner
            spinner_placeholder.empty()
            
            # Provide the PDF for download
            right_sidebar.download_button(
                label="לחץ כאן להורדת ה-PDF",
                data=pdf,
                file_name="converted_images.pdf",
                mime="application/pdf"
            )
            st.success('ה-PDF נוצר בהצלחה! לחץ על הכפתור **לחץ כאן להורדת ה-PDF** בסרגל מימין כדי להוריד.')
        else:
            st.warning("אנא העלה תמונות לפני יצירת ה-PDF.")

    # Add footer to the bottom of the right sidebar
    right_sidebar.markdown("---")
    right_sidebar.markdown(footer_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()