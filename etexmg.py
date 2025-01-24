import streamlit as st
import numpy as np
from PIL import Image
import easyocr

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
                st.session_state.extracted_text = extract_text(image, selected_languages)
    
    if hasattr(st.session_state, 'extracted_text'):
        # Display results
        st.subheader("Extracted Text")
        text_area = st.text_area("", st.session_state.extracted_text, height=300)
        
        # Provide a download button directly
        st.download_button(
            label="💾 Save Text",
            data=st.session_state.extracted_text,
            file_name="extracted_text.txt",
            mime="text/plain"
        )

main()



# إخفاء العناصر غير المرغوب فيها
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            #stStreamlitLogo {display: none;}
            a {
                text-decoration: none;
                color: inherit;
                pointer-events: none;
            }
            a:hover {
                text-decoration: none;
                color: inherit;
                cursor: default;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)