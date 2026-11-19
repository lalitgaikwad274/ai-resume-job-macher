import sys
from pathlib import Path

# Add project root to sys.path so 'app' can be imported when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.text_similarity import (
    calculate_text_similarity
)

resume = """
Developed REST APIs using Python and FastAPI.
Worked with PostgreSQL and Docker.
"""

job = """
Looking for a backend developer with Python
experience, API development and PostgreSQL knowledge.
"""

score = calculate_text_similarity(
    resume,
    job
)

print("Text Similarity:", score, "%")