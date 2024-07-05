import streamlit as st
from PIL import Image, ImageOps
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import time
from utils.init import initialize
from utils.counter import get_user_count, update_user_count, USER_COUNT_CSS
import atexit

# Initialize Streamlit configuration and load resources
header_content, footer_content = initialize()

# Add user count CSS
st.markdown(USER_COUNT_CSS, unsafe_allow_html=True)

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

def resize_image(image, max_size=(800, 800)):
    """Resize image while maintaining aspect ratio"""
    return ImageOps.contain(image, max_size, Image.LANCZOS)

def main():
    # Increment user count when a new session starts
    if 'user_counted' not in st.session_state:
        st.session_state.user_counted = True
        update_user_count(1)

    # Header
    st.markdown(header_content)        

    # Handle the "Start Over" button click
    if st.button("התחל מחדש", use_container_width=True):
        st.session_state.clear()               

    # Register function to decrement user count when the session ends
    atexit.register(update_user_count, -1)

    # File uploader
    uploaded_files = st.file_uploader(
        "העלה תמונות",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg'],
        key="file_uploader"
    )

    # Initialize session state
    if 'images' not in st.session_state:
        st.session_state.images = []

    # Process uploaded files
    current_files = [img['file'] for img in st.session_state.images]
    for uploaded_file in uploaded_files:
        if uploaded_file not in current_files:
            image = Image.open(uploaded_file)
            image_resized = resize_image(image)
            image_with_border = add_border(image_resized)
            st.session_state.images.append({'file': uploaded_file, 'image': image_with_border, 'original': image})

    # Remove images that are no longer in uploaded_files
    st.session_state.images = [img for img in st.session_state.images if img['file'] in uploaded_files]

    # Display images in a responsive grid
    if st.session_state.images:
        cols = st.columns(3)
        for i, img_dict in enumerate(st.session_state.images):
            with cols[i % 3]:
                st.image(img_dict['image'], use_column_width=True)
                if i > 0:
                    if st.button(f"🔼 הזז למעלה", key=f"up_{i}", use_container_width=True):
                        st.session_state.images.insert(i-1, st.session_state.images.pop(i))
                        # st.experimental_rerun()
    
    if st.button("לחץ ליצירת PDF", use_container_width=True):
        if st.session_state.images:
            with st.spinner("יוצר PDF... אנא המתן"):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(percent_complete + 1)
                pdf = create_pdf([img_dict['original'] for img_dict in st.session_state.images])
            
            st.download_button(
                label="לחץ כאן להורדת ה-PDF",
                data=pdf,
                file_name="converted_images.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.success('ה-PDF נוצר בהצלחה! לחץ על הכפתור **לחץ כאן להורדת ה-PDF** כדי להוריד.')
        else:
            st.warning("אנא העלה תמונות לפני יצירת ה-PDF.")

    # Footer with user count
    st.markdown("---")
    user_count = get_user_count()
    footer_with_count = f"{footer_content}\n\n<p class='user-count'>מספר משתמשים מחוברים: {user_count}</p>"
    st.markdown(footer_with_count, unsafe_allow_html=True)

if __name__ == "__main__":
    main()