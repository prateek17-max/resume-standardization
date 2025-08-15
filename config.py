import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# File paths
TEMPLATE_PATH = os.path.join('templates', 'standard_resume_template.docx')

# Constants
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Gemini Configuration
TEMPERATURE = 0.7
TOP_K = 40
TOP_P = 0.95
MAX_OUTPUT_TOKENS = 2048

# Resume sections
RESUME_SECTIONS = [
    'personal_info',
    'summary',
    'experience',
    'education',
    'skills',
    'certifications',
    'projects'
]
