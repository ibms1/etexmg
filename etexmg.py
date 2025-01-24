import streamlit as st
import numpy as np
from PIL import Image
import easyocr
import base64

# Mapping of language codes
LANGUAGE_MAP = {
    'en': 'English', 
    'ar': 'Arabic', 
    'fr': 'French', 
    'es': 'Spanish', 
    'de': 'German', 
    'ru': 'Russian', 
    'zh': 'Chinese', 
    'ja': 'Japanese', 
    'ko': 'Korean', 
    'pt': 'Portuguese', 
    'it': 'Italian', 
    'tr': 'Turkish', 
    'he': 'Hebrew'
}

def extract_text(image, selected_languages):
    """Extract text using EasyOCR"""
    try:
        reader = easyocr.Reader(selected_languages)
        results = reader.readtext(np.array(image))
        
        # Combine detected text
        extracted_text = ' '.join([result[1] for result in results])
        return extracted_text
    except Exception as e:
        st.error(f"Error in text extraction: {e}")
        return ""

def get_download_link(text):
    """Create a download link for text file"""
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="extracted_text.txt">Download Text File</a>'
    return href

def main():
    st.title("🌐 Multilingual OCR Extractor")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload Image", 
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="Upload an image to extract text"
    )
    
    # Language selection with full names
    selected_languages = st.multiselect(
        "Select Languages", 
        list(LANGUAGE_MAP.keys()),
        format_func=lambda x: LANGUAGE_MAP[x],
        default=['en']
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # Extract text button
        if st.button("Extract Text"):
            with st.spinner('Extracting text...'):
                extracted_text = extract_text(image, selected_languages)
                
            # Display results
            st.subheader("Extracted Text")
            text_area = st.text_area("", extracted_text, height=300)
            
            # Copy and Save buttons
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 Copy Text"):
                    st.code(extracted_text)
                    st.success("Text copied to clipboard!")
            
            with col2:
                if st.button("💾 Save Text"):
                    st.markdown(get_download_link(extracted_text), unsafe_allow_html=True)

main()