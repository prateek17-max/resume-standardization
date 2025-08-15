"""
Main Streamlit application for resume standardization
"""
import streamlit as st
import json
import os
from pathlib import Path
from modules.file_handler import FileHandler
from modules.llm_extractor import LLMExtractor
from modules.resume_formatter import ResumeFormatter
import json

def main():
    st.title("Resume Standardization Tool")
    st.write("Upload your resume (PDF/DOCX) to convert it to our standard format")

    # File upload
    uploaded_file = st.file_uploader("Choose your resume", type=['pdf', 'docx'])
    
    # Tone selection
    tone = st.select_slider(
        "Select resume tone",
        options=['Formal', 'Balanced', 'Casual'],
        value='Balanced'
    )

    if uploaded_file is not None:
        try:
            with st.spinner('Processing your resume...'):
                # Initialize components
                file_handler = FileHandler()
                llm_extractor = LLMExtractor()
                resume_formatter = ResumeFormatter()

                # Process file and show debug info
                st.write("### Processing Steps:")
                
                # Extract text
                st.write("1️⃣ Extracting text from document...")
                raw_text = file_handler.read_file(uploaded_file)
                st.text_area("Extracted Text Preview:", 
                            value=raw_text[:1000] + "..." if len(raw_text) > 1000 else raw_text,
                            height=150)
                
                # Extract structured data
                st.write("2️⃣ Analyzing and structuring information...")
                structured_data = llm_extractor.extract_information(raw_text, tone)
                st.write("Structured Data:")
                if isinstance(structured_data, str):
                    structured_data = json.loads(structured_data)
                st.json(structured_data)
                
                # Generate formatted resume
                st.write("3️⃣ Generating formatted resume...")
                output_file = resume_formatter.format_resume(structured_data)

                # Success message and download
                st.success("✅ Resume processed successfully!")
                
                with open(output_file, 'rb') as file:
                    st.download_button(
                        label="📥 Download Standardized Resume",
                        data=file,
                        file_name="standardized_resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

                st.info("""
                💡 **Tip:** Review the processed data above to ensure all information 
                was extracted correctly.
                """)
                    
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
