"""
Module for extracting structured information from resume text using Google's Gemini API
"""
import json
import requests
from typing import Dict, Any, Optional
from config import GOOGLE_API_KEY, TEMPERATURE

class LLMExtractor:
    """Handles the extraction of structured information from resume text using Gemini API."""
    
    def __init__(self):
        """Initialize the LLM extractor with API configuration."""
        self.api_key = GOOGLE_API_KEY
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }

    def extract_information(self, text: str, tone: str = "Balanced") -> Dict[str, Any]:
        """
        Extract structured information from resume text using Gemini.
        
        Args:
            text (str): The raw text extracted from the resume
            tone (str, optional): Tone for the output (Formal/Casual). Defaults to "Balanced".
            
        Returns:
            Dict[str, Any]: Structured resume data
            
        Raises:
            Exception: If there's an error in processing or parsing the LLM response
        """
        try:
            # Create the prompt with examples
            prompt = self._create_prompt(text, tone)
            
            # Prepare the request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": TEMPERATURE,
                    "topP": 0.8,
                    "topK": 40,
                    "maxOutputTokens": 2048
                }
            }
            
            # Make the API request
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload
            )
                
            # Check response status
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")

            # Parse the response
            response_json = response.json()
            
            # Extract the generated text
            if 'candidates' in response_json:
                generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
                
                # Try to parse as JSON
                try:
                    return json.loads(generated_text)
                except json.JSONDecodeError:
                    # Try to extract JSON from text
                    import re
                    json_match = re.search(r'\{.*\}', generated_text, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                    raise Exception("Could not extract valid JSON from response")
            else:
                raise Exception("Unexpected API response format")
                
        except Exception as e:
            raise Exception(f"Error in LLM processing: {str(e)}")

    def _create_example_output(self) -> Dict[str, Any]:
        """Create an example of properly formatted output."""
        return {
            "personal_info": {
                "name": "John Smith",
                "email": "john.smith@email.com",
                "phone": "+1 123-456-7890",
                "location": "New York, NY",
                "linkedin": "linkedin.com/in/johnsmith"
            },
            "summary": "Experienced software engineer with 5 years of expertise...",
            "experience": [
                {
                    "title": "Senior Software Engineer",
                    "company": "Tech Corp",
                    "location": "New York, NY",
                    "dates": "Jan 2020 - Present",
                    "responsibilities": [
                        "Led development of cloud-based application...",
                        "Managed team of 5 developers..."
                    ]
                }
            ],
            "education": [
                {
                    "degree": "B.S. Computer Science",
                    "institution": "University of Technology",
                    "location": "Boston, MA",
                    "dates": "2015-2019",
                    "gpa": "3.8"
                }
            ],
            "skills": {
                "technical": ["Python", "Java", "AWS", "Docker"],
                "soft": ["Leadership", "Communication", "Problem Solving"]
            },
            "certifications": [
                "AWS Certified Solutions Architect",
                "Professional Scrum Master"
            ],
             "projects": [
            {
                "name": "AI Resume Parser",
                "description": "Developed an AI-powered resume parser using Python and NLP."
            },
            {
                "name": "Microservices Architecture",
                "description": "Created a scalable microservices architecture for a SaaS product."
            }
        ]
        }

    def _create_prompt(self, text: str, tone: str) -> str:
        """
        Create a detailed prompt for the LLM with examples and specific instructions.
        
        Args:
            text (str): The resume text to analyze
            tone (str): Desired tone for the output
            
        Returns:
            str: The formatted prompt
        """
        example_output = self._create_example_output()
        
        return f"""You are an expert resume analyzer. Extract information from the resume below and format it following these rules:

1. Extract ALL relevant information, don't skip details.
2. Format dates consistently as "MMM YYYY" (e.g., "Jan 2020").
3. For experience:
   - Keep action verbs and achievements.
   - Make descriptions {tone.lower()} but professional.
   - Maintain chronological order.
4. For skills:
   - Separate technical and soft skills.
   - Include ALL mentioned skills.
5. For the summary:
   - If the resume does not have a summary, GENERATE a professional summary based on the candidate's experience and education. NEVER return null or none for summary.
6. For projects:
   - Always return a list of objects, each with "name" and "description" keys. If the resume does not have projects, infer at least one project from the experience or education, or return an empty list, but NEVER return null or none.
7. Return ONLY valid JSON matching this structure:

{json.dumps(example_output, indent=2)}

Resume to analyze:
{text}

Return ONLY the JSON, no other text. Ensure all dates use MMM YYYY format."""
