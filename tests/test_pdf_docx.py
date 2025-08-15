import pytest
from modules.file_handler import FileHandler
from modules.text_extractor import TextExtractor
import io

def test_pdf_text_extraction():
    """Test PDF text extraction"""
    handler = FileHandler()
    # Add test implementation

def test_docx_text_extraction():
    """Test DOCX text extraction"""
    handler = FileHandler()
    # Add test implementation

def test_text_cleaning():
    """Test text cleaning and preprocessing"""
    extractor = TextExtractor()
    sample_text = """
    EDUCATION
    University of Example
    
    EXPERIENCE
    Software Engineer
    """
    cleaned_text = extractor.clean_text(sample_text)
    assert "EDUCATION" in cleaned_text
    assert "EXPERIENCE" in cleaned_text

def test_section_extraction():
    """Test section extraction from text"""
    extractor = TextExtractor()
    sample_text = """
    EDUCATION
    BS in Computer Science
    
    EXPERIENCE
    Software Developer
    """
    sections = extractor.extract_sections(sample_text)
    assert "EDUCATION" in sections
    assert "EXPERIENCE" in sections
