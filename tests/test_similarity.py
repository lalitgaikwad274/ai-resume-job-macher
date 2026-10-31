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