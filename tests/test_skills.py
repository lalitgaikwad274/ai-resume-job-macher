import sys
from pathlib import Path

# Add project root to sys.path so 'app' can be imported when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.skill_extractor import extract_skills, get_total_skills
sample_resume = """
React Native Developer

Skills:
Python, FastAPI, PostgreSQL,
Docker, React Native, JavaScript,
TypeScript, AWS.

Experience:
4 years of experience in software development.

Education:
Bachelor of Engineering.
"""

skills = extract_skills(sample_resume)

print("Extracted Skills:")
print(skills)

print("Total Skills:", get_total_skills(skills))