import streamlit as st
from PIL import Image
import easyocr

def extract_text(image, selected_languages):
    """Extract text using EasyOCR"""
    reader = easyocr.Reader(selected_languages)
    results = reader.readtext(image)
    
    # Combine detected text
    extracted_text = ' '.join([result[1] for result in results])
    return extracted_text

def main():
    st.title("🌐 Multilingual OCR Extractor")
    
    # Image upload
    uploaded_file = st.file_uploader(
        "Upload Image", 
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="Upload an image to extract text"
    )
    
    # Language selection
    selected_languages = st.multiselect(
        "Select Languages", 
        ['en', 'ar', 'fr', 'es', 'de', 'ru', 'zh', 'ja', 'ko', 'pt', 'it', 'tr', 'he'],
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
            st.text_area("", extracted_text, height=300)

if __name__ == "__main__":
    main()