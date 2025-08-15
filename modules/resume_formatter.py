from docx import Document
from docxtpl import DocxTemplate
import json
import os

class ResumeFormatter:
    def __init__(self):
        self.template_path = os.path.join("templates", "standard_resume.docx")

    def format_resume(self, structured_data):
        """Generate a formatted resume using the template and structured data"""
        try:
            # Parse JSON if string
            if isinstance(structured_data, str):
                data = json.loads(structured_data)
            else:
                data = structured_data

            # Load the template
            doc = DocxTemplate(self.template_path)

            # Format the data for template
            context = {
                'name': data.get('personal_info', {}).get('name', ''),
                'email': data.get('personal_info', {}).get('email', ''),
                'phone': data.get('personal_info', {}).get('phone', ''),
                'location': data.get('personal_info', {}).get('location', ''),
                'linkedin': data.get('personal_info', {}).get('linkedin', ''),
                'summary': data.get('summary', ''),
                'experience': [
                    {
                        'title': exp.get('title', ''),
                        'company': exp.get('company', ''),
                        'location': exp.get('location', ''),
                        'dates': exp.get('dates', ''),
                        'responsibilities': exp.get('responsibilities', [])
                    }
                    for exp in data.get('experience', [])
                ],
                'education': [
                    {
                        'degree': edu.get('degree', ''),
                        'institution': edu.get('institution', ''),
                        'location': edu.get('location', ''),
                        'dates': edu.get('dates', ''),
                        'gpa': edu.get('gpa', '')
                    }
                    for edu in data.get('education', [])
                ],
                'skills': {
                    'technical': data.get('skills', {}).get('technical', []),
                    'soft': data.get('skills', {}).get('soft', [])
                },
                'certifications': data.get('certifications', []),
                'projects': [
                    {'name': proj.get('name', ''), 'description': proj.get('description', '')}
                    if isinstance(proj, dict)
                    else {'name': proj, 'description': ''}
                    for proj in data.get('projects', [])
                ]
            }

            # Render the template with our data
            doc.render(context)
            
            # Save the generated resume
            output_path = "generated_resume.docx"
            doc.save(output_path)
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Error generating resume: {str(e)}")


