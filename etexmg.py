import streamlit as st
import pytesseract
from PIL import Image
import cv2
import numpy as np

# Supported Languages
LANGUAGES = [
    'ara', 'eng', 'fra', 'spa', 'deu', 'rus', 'chi_sim', 
    'jpn', 'kor', 'por', 'ita', 'tur', 'heb'
]

def preprocess_image(image):
    """Image preprocessing to improve OCR accuracy"""
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return thresh

def extract_text(image, selected_languages):
    """Extract text from image with multiple languages"""
    preprocessed = preprocess_image(image)
    languages = '+'.join(selected_languages)
    text = pytesseract.image_to_string(preprocessed, lang=languages)
    return text

def main():
    st.title("Multilingual OCR Text Extractor")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload Image", 
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="Upload an image to extract text"
    )
    
    # Language selection moved under image upload
    selected_languages = st.multiselect(
        "Select Languages", 
        LANGUAGES, 
        default=['eng']
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Extract text button
        if st.button("Extract Text"):
            with st.spinner('Extracting text...'):
                extracted_text = extract_text(image, selected_languages)
                
            # Display results
            st.subheader("Extracted Text")
            st.text_area("", extracted_text, height=300)

if __name__ == "__main__":
    main()