import re
import string

class TextExtractor:
    def __init__(self):
        self.section_headers = [
            'education', 'experience', 'skills', 'projects',
            'work history', 'employment', 'qualifications',
            'certifications', 'achievements', 'summary'
        ]

    def clean_text(self, text):
        """Clean and preprocess the extracted text"""
        # Remove multiple newlines and spaces
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters while preserving important ones
        text = ''.join(char for char in text if char in string.printable)
        
        # Standardize section headers
        for header in self.section_headers:
            pattern = re.compile(f"{header}", re.IGNORECASE)
            text = pattern.sub(header.upper(), text)
            
        return text.strip()

    def extract_sections(self, text):
        """Split text into different resume sections"""
        sections = {}
        current_section = 'OTHER'
        current_content = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            is_header = any(header.upper() in line.upper() 
                          for header in self.section_headers)
            
            if is_header:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                    current_content = []
                
                # Update current section
                current_section = line.upper()
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
            
        return sections
