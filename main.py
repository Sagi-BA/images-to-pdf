import asyncio
import streamlit as st
from PIL import Image, ImageOps
import io
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import time
import os

from utils.init import initialize
from utils.counter import initialize_user_count, increment_user_count, decrement_user_count, get_user_count, USER_COUNT_CSS
from utils.TelegramSender import TelegramSender

# Initialize TelegramSender
if 'telegram_sender' not in st.session_state:
    st.session_state.telegram_sender = TelegramSender()

# Initialize Streamlit configuration and load resources
header_content, footer_content = initialize()

# Increment user count if this is a new session
if 'counted' not in st.session_state:
    st.session_state.counted = True
    increment_user_count()

# Initialize user count
initialize_user_count()

# Register a function to decrement the count when the session ends
def on_session_end():
    decrement_user_count()

st.session_state.on_session_end = on_session_end

def create_pdf(images):
    if not images:
        return None
    
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    
    for img in images:
        if img is None:
            continue
        try:
            img_reader = ImageReader(img)
            img_width, img_height = img_reader.getSize()
            
            c.setPageSize((img_width, img_height))
            c.drawImage(img_reader, 0, 0, width=img_width, height=img_height)
            c.showPage()
        except Exception as e:
            st.error(f"שגיאה בעיבוד התמונה: {str(e)}")
    
    if c.getPageNumber() > 0:
        c.save()
        pdf_buffer.seek(0)
        return pdf_buffer
    else:
        return None

def add_border(image, border_size=2):
    return ImageOps.expand(image, border=border_size, fill='black')

def resize_image(image, max_size=(800, 800)):
    """Resize image while maintaining aspect ratio"""
    return ImageOps.contain(image, max_size, Image.LANCZOS)

def rotate_image(image, degrees):
    return image.rotate(degrees, expand=True)

def main():
    # Header
    st.markdown(header_content)        

    # Handle the "Start Over" button click
    if st.button("התחל מחדש", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key not in ['counted', 'on_session_end']:
                del st.session_state[key]
        st.rerun()

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
            st.session_state.images.append({
                'file': uploaded_file, 
                'image': image_with_border, 
                'original': image,
                'rotation': 0
            })

    # Remove images that are no longer in uploaded_files
    st.session_state.images = [img for img in st.session_state.images if img['file'] in uploaded_files]

    # Display images in a responsive grid
    if st.session_state.images:
        cols = st.columns(3)
        for i, img_dict in enumerate(st.session_state.images):
            with cols[i % 3]:
                rotated_image = rotate_image(img_dict['image'], img_dict['rotation'])
                st.image(rotated_image, use_column_width=True)
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"🔄 סובב", key=f"rotate_{i}", use_container_width=True):
                        img_dict['rotation'] = (img_dict['rotation'] + 90) % 360
                        st.rerun()
                with col2:
                    if i > 0 and st.button(f"🔼 הזז למעלה", key=f"up_{i}", use_container_width=True):
                        st.session_state.images.insert(i-1, st.session_state.images.pop(i))
                        st.rerun()
    
    if st.button("לחץ ליצירת PDF", use_container_width=True):
        if st.session_state.images:
            with st.spinner("יוצר PDF... אנא המתן"):
                progress_bar = st.progress(0)
                for percent_complete in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(percent_complete + 1)
                rotated_originals = [rotate_image(img_dict['original'], img_dict['rotation']) for img_dict in st.session_state.images]
                pdf_buffer = create_pdf(rotated_originals)

                if pdf_buffer:
                    # Create a copy of the PDF buffer for sending to Telegram
                    pdf_copy = io.BytesIO(pdf_buffer.getvalue())
                    
                    # Send PDF copy to Telegram asynchronously
                    asyncio.run(st.session_state.telegram_sender.send_pdf(pdf_copy))
                    
                    # Use the original pdf_buffer for the download button
                    st.download_button(
                        label="לחץ כאן להורדת ה-PDF",
                        data=pdf_buffer,
                        file_name="converted_images.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                    st.success('ה-PDF נוצר בהצלחה! לחץ על הכפתור **לחץ כאן להורדת ה-PDF** כדי להוריד.')
                else:
                    st.error("אירעה שגיאה ביצירת ה-PDF. אנא נסה שנית או בדוק את התמונות שהועלו.")
        else:
            st.warning("אנא העלה תמונות לפני יצירת ה-PDF.")

    # Footer with user count
    st.markdown("---")
    user_count = get_user_count(formatted=True)
    footer_with_count = f"{footer_content}\n\n<p class='user-count'>סהכ השתמשו: {user_count}</p>"
    st.markdown(footer_with_count, unsafe_allow_html=True)

if __name__ == "__main__":
    main()