from docxtpl import DocxTemplate
import json
import os
from config import TEMPLATE_PATH

class ResumeGenerator:
    def __init__(self):
        self.template_path = TEMPLATE_PATH

    def generate_resume(self, structured_data):
        """Generate a formatted resume using the template and structured data"""
        try:
            # Parse JSON if string
            if isinstance(structured_data, str):
                data = json.loads(structured_data)
            else:
                data = structured_data

            if not os.path.exists(self.template_path):
                raise FileNotFoundError(f"Template file not found at {self.template_path}")

            # Load template
            doc = DocxTemplate(self.template_path)
            
            # Prepare the data context
            context = {
                'personal_info': data.get('personal_info', {}),
                'summary': data.get('summary', ''),
                'experience': data.get('experience', []),
                'education': data.get('education', []),
                'skills': data.get('skills', {'technical': [], 'soft': []}),
                'certifications': data.get('certifications', []),
                'projects': data.get('projects', [])
            }
            
            # Render template with data
            doc.render(context)
            
            # Save the generated resume
            output_path = "generated_resume.docx"
            doc.save(output_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error generating resume: {str(e)}")

    def _format_text(self, text, style="normal"):
        """Apply formatting to text based on style"""
        # Implementation for different text styling if needed
        return text
