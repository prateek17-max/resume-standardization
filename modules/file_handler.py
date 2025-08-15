import pdfplumber
from docx import Document
import pytesseract
from PIL import Image
import io
import os

class FileHandler:
    def __init__(self):
        self.supported_formats = {'.pdf', '.docx'}

    def read_file(self, file_obj):
        """Read and extract text from PDF or DOCX file"""
        filename = file_obj.name.lower()
        ext = os.path.splitext(filename)[1]

        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {ext}")

        if ext == '.pdf':
            return self._process_pdf(file_obj)
        else:
            return self._process_docx(file_obj)

    def _process_pdf(self, file_obj):
        """Extract text from PDF, using OCR if needed"""
        try:
            # First try normal text extraction
            with pdfplumber.open(file_obj) as pdf:
                text = ''
                for page in pdf.pages:
                    text += page.extract_text() or ''
                
                # If no text was extracted, try OCR
                if not text.strip():
                    return self._process_pdf_ocr(file_obj)
                return text
        except Exception as e:
            raise Exception(f"Error processing PDF: {str(e)}")

    def _process_pdf_ocr(self, file_obj):
        """Process PDF using OCR when text extraction fails"""
        try:
            text = ''
            pdf = pdfplumber.open(file_obj)
            for page in pdf.pages:
                # Convert PDF page to image
                img = page.to_image()
                # Use pytesseract for OCR
                text += pytesseract.image_to_string(img.original)
            return text
        except Exception as e:
            raise Exception(f"Error processing PDF with OCR: {str(e)}")

    def _process_docx(self, file_obj):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_obj)
            return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error processing DOCX: {str(e)}")
