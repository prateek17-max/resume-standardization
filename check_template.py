from docxtpl import DocxTemplate

def check_template():
    try:
        # Load the template
        doc = DocxTemplate("Resume Template.docx")
        print("Template loaded successfully!")
        
        # Try rendering with sample data
        context = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123-456-7890',
            'location': 'City, Country',
            'linkedin': 'linkedin.com/in/johndoe',
            'summary': 'Experienced professional...',
            'experience': [
                {
                    'title': 'Software Engineer',
                    'company': 'Tech Corp',
                    'location': 'City',
                    'dates': '2020-Present',
                    'responsibilities': [
                        'Developed features',
                        'Led team projects'
                    ]
                }
            ],
            'education': [
                {
                    'degree': 'BS Computer Science',
                    'institution': 'University',
                    'location': 'City',
                    'dates': '2016-2020',
                    'gpa': '3.8'
                }
            ],
            'skills': {
                'technical': ['Python', 'Java', 'SQL'],
                'soft': ['Leadership', 'Communication']
            },
            'certifications': ['AWS Certified', 'PMP'],
            'projects': ['Project 1', 'Project 2']
        }
        
        doc.render(context)
        print("Template variables are correct!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nMake sure your template uses these variables:")
        print("""
In your template, use these variables:
{{ name }} - for the name
{{ email }} - for email
{{ phone }} - for phone number
{{ location }} - for location
{{ linkedin }} - for LinkedIn URL
{{ summary }} - for professional summary

For experience (in a loop):
{% for job in experience %}
    {{ job.title }}
    {{ job.company }}
    {{ job.location }}
    {{ job.dates }}
    {% for duty in job.responsibilities %}
        • {{ duty }}
    {% endfor %}
{% endfor %}

For education (in a loop):
{% for edu in education %}
    {{ edu.degree }}
    {{ edu.institution }}
    {{ edu.location }}
    {{ edu.dates }}
    {{ edu.gpa }}
{% endfor %}

For skills:
{% for skill in skills.technical %}
    • {{ skill }}
{% endfor %}
{% for skill in skills.soft %}
    • {{ skill }}
{% endfor %}

For certifications:
{% for cert in certifications %}
    • {{ cert }}
{% endfor %}

For projects:
{% for project in projects %}
    • {{ project }}
{% endfor %}
        """)

if __name__ == "__main__":
    check_template()
