# AI Resume & Job Match Analyzer 🎯📄

An intelligent, production-ready backend service built with **FastAPI**, **SQLAlchemy**, and **LLMs (Google Gemini, OpenAI, OpenRouter)** that analyzes candidate resumes against job descriptions. It provides deterministic skill matching, TF-IDF semantic text similarity, experience/education extraction, and AI-powered actionable career recommendations.

---

## 📌 Table of Contents

- [Overview & How It Works](#-how-it-works)
- [Architecture & Processing Pipeline](#-architecture--processing-pipeline)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables Configuration](#environment-variables-configuration)
  - [Database Migrations](#database-migrations)
  - [Running the Application](#running-the-application)
- [API Reference](#-api-reference)
  - [1. Complete End-to-End Analysis](#1-complete-end-to-end-analysis)
  - [2. Resume Parsing & Extraction](#2-resume-parsing--extraction)
  - [3. Job Description Analysis](#3-job-description-analysis)
  - [4. Skill Matching & Scoring](#4-skill-matching--scoring)
  - [5. AI Recommendations](#5-ai-recommendations)
  - [6. Users, Resumes & Saved Jobs](#6-users-resumes--saved-jobs)
- [AI Provider Configuration](#-ai-provider-configuration)
- [Running Tests](#-running-tests)
- [License](#-license)

---

## ⚙️ How It Works

When a candidate uploads their resume alongside a target job description, the system executes an automated 7-step analysis pipeline:

1. **Document Parsing**: Extracts clean raw text from PDF (via PyMuPDF) or DOCX (via python-docx) documents up to 5 MB in size.
2. **Entity & Skill Extraction**:
   - Matches candidate skills against a categorized taxonomy spanning Programming Languages, Backend, Frontend/Mobile, Databases, and Cloud/DevOps.
   - Extracts degrees, universities, and graduation dates (handling wrapped lines and Unicode date intervals).
   - Identifies explicit duration mentions and calculates cumulative employment tenure from date ranges (`MM/YYYY – Present`).
3. **Job Description Profiling**: Identifies required versus preferred skills, bonus qualifications, and required years of experience.
4. **Deterministic Weighted Scoring**:
   - Calculates the candidate's coverage of required skills (weighted at **80%**) and preferred skills (weighted at **20%**).
   - Generates lists of matched vs. missing skills.
5. **Semantic Text Similarity**: Evaluates textual alignment between resume and job description using **TF-IDF vectorization** and **Cosine Similarity** (0–100%).
6. **Multi-Model AI Recommendations**:
   - Sends the candidate profile and job requirements to a configured LLM (**Gemini**, **OpenAI**, or **OpenRouter**).
   - Produces structured Pydantic outputs: overall career summary, key strengths, weaknesses with actionable remediation, prioritized missing skills, ATS bullet point rewrites, and keyword recommendations.
   - Features automatic JSON repair fallbacks to recover truncated responses from token-limited free tier models.
7. **Data Persistence**: Optionally stores candidate resumes, saved jobs, and historical analysis reports in a relational **PostgreSQL** database.

---

## 🏗 Architecture & Processing Pipeline

```mermaid
flowchart TD
    A["Candidate Uploads Resume (PDF/DOCX) + Job Description"] --> B["FastAPI Server: /analysis/full"]
    
    subgraph Ingestion ["1. Document Ingestion"]
        B --> C["Resume Parser (PyMuPDF / python-docx)"]
        C --> D["Raw Extracted Text"]
    end

    subgraph Extraction ["2. Deterministic Extraction Engine"]
        D --> E["Skill Extractor\n(5 Skill Categories)"]
        D --> F["Resume Analyzer\n(Education & Experience Extraction)"]
        B --> G["Job Analyzer\n(Required vs. Preferred Skills)"]
    end

    subgraph Scoring ["3. Scoring & Similarity Engine"]
        E & G --> H["Skill Matcher\n(80% Required / 20% Preferred)"]
        D & B --> I["Text Similarity\n(TF-IDF + Cosine Similarity)"]
    end

    subgraph Intelligence ["4. Multi-Provider AI Assistant"]
        D & B --> J["AI Assistant Dispatcher\n(ai_resume_assistant.py)"]
        J --> K["Gemini Service\n(gemini-2.5-flash)"]
        J --> L["OpenAI Service\n(gpt-4o-mini)"]
        J --> M["OpenRouter Service\n(Llama 3.3 / Free Models)"]
        K & L & M --> N["JSON Repair Fallback &\nResumeRecommendation Pydantic Schema"]
    end

    H & I & N --> O["Consolidated JSON Analysis Report"]
    O --> P["PostgreSQL Database / Client UI"]
```

---

## ✨ Key Features

- **Multi-Format Resume Support**: Handles PDF and DOCX documents with automated MIME-type validation and size controls (up to 5 MB).
- **Categorized Skill Database**: Recognizes skills across 5 distinct domains:
  - `programming_languages`: Python, TypeScript, JavaScript, Java, Go, C++, etc.
  - `backend`: FastAPI, Django, Flask, Express, NestJS, REST APIs, GraphQL, etc.
  - `frontend_mobile`: React, React Native, Next.js, Redux, HTML, CSS, etc.
  - `database`: PostgreSQL, MySQL, MongoDB, Redis, SQLite, etc.
  - `cloud_devops`: AWS, Docker, Kubernetes, CI/CD, Git, Jenkins, etc.
- **Robust Education & Experience Detection**:
  - Handles multi-line degrees (e.g., `Master of Computer\nScience`).
  - Recognizes academic credentials, institutions, and date ranges (`07/2020 – 05/2022`).
  - Supports Unicode en-dashes (`–`), em-dashes (`—`), and hyphenated dates.
  - Calculates cumulative years of experience from employment dates (`07/2022 – Present`).
- **Weighted Match Scoring**: Weights required skills at 80% and preferred skills at 20% to prevent unneeded bonus skills from skewing match percentages.
- **TF-IDF Semantic Matching**: Provides an unbiased mathematical similarity baseline using scikit-learn.
- **Modular Multi-Provider LLM Integration**:
  - Decoupled implementations for **Google Gemini**, **OpenAI**, and **OpenRouter**.
  - Dynamic runtime selection via `.env` or request parameters.
  - Built-in automatic JSON repair to salvage truncated responses without 502/500 crashes.
- **Relational PostgreSQL Architecture**: Complete database models for users, resumes, jobs, analyses, and recommendations with Alembic migrations.

---

## 🛠 Tech Stack

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database & ORM**: [PostgreSQL](https://www.postgresql.org/), [SQLAlchemy 2.0](https://www.sqlalchemy.org/), [Alembic](https://alembic.sqlalchemy.org/)
- **Document Processing**: [PyMuPDF](https://pymupdf.readthedocs.io/), [python-docx](https://python-docx.readthedocs.io/)
- **NLP & Similarity**: [scikit-learn](https://scikit-learn.org/) (TF-IDF & Cosine Similarity)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **AI / LLM Providers**:
  - [Google GenAI SDK](https://github.com/google/generative-ai-python) (`google-genai`)
  - [OpenAI Python SDK](https://github.com/openai/openai-python)
  - [OpenRouter](https://openrouter.ai/) (via AsyncOpenAI)

---

## 📂 Project Structure

```text
ai-resume-job-matcher/
├── app/
│   ├── core/
│   │   └── security.py                  # Password hashing & verification
│   ├── data/
│   │   └── skills.py                    # Master taxonomy of categorized skills
│   ├── database/
│   │   ├── base.py                      # SQLAlchemy DeclarativeBase
│   │   ├── connection.py                # Database engine & session generator
│   │   └── session.py                   # SessionLocal configuration
│   ├── models/                          # SQLAlchemy database entities
│   │   ├── user.py                      # User model
│   │   ├── resume.py                    # Stored resume model
│   │   ├── job_description.py           # Saved job posting model
│   │   ├── resume_analysis.py           # Match analysis records
│   │   └── recommendation.py            # AI recommendations storage
│   ├── repositories/                    # Database CRUD operations
│   │   ├── user_repository.py
│   │   ├── resume_repository.py
│   │   └── job_repository.py
│   ├── routers/                         # FastAPI route endpoints
│   │   ├── analysis.py                  # /analysis/full end-to-end pipeline
│   │   ├── resumes.py                   # /resumes CRUD
│   │   ├── jobs.py                      # /jobs/analyze
│   │   ├── matching.py                  # /matching/analyze
│   │   ├── ai.py                        # /ai/recommendations
│   │   ├── users.py                     # /users registration & profile
│   │   └── saved_jobs.py                # /saved-jobs management
│   ├── schemas/                         # Pydantic validation schemas
│   │   ├── user.py
│   │   ├── resume.py
│   │   ├── job.py
│   │   ├── matching.py
│   │   └── ai_recommendation.py         # Structured AI output schema
│   ├── services/                        # Business logic & AI pipelines
│   │   ├── resume_parser.py             # PDF & DOCX text extraction
│   │   ├── skill_extractor.py           # Regex skill taxonomy matcher
│   │   ├── resume_analyzer.py           # Education & Experience parsing
│   │   ├── job_analyzer.py              # Required vs preferred skill profiling
│   │   ├── job_matcher.py               # Weighted scoring algorithm
│   │   ├── text_similarity.py           # TF-IDF cosine similarity
│   │   ├── promt.py                     # System & user prompt templates
│   │   ├── json_utils.py                # Truncated JSON recovery utilities
│   │   ├── ai_gemini.py                 # Google Gemini implementation
│   │   ├── ai_openai.py                 # OpenAI implementation
│   │   ├── ai_openrouter.py             # OpenRouter implementation
│   │   ├── ai_resume_assistant.py       # Unified AI provider coordinator
│   │   └── analysis_service.py          # Consolidated analysis pipeline
│   └── main.py                          # FastAPI application initialization & CORS
├── migrations/                          # Alembic database migrations
│   ├── env.py
│   └── versions/
├── tests/                               # Verification & unit test scripts
│   ├── test_skills.py                   # Skill & education extraction test
│   └── test_similarity.py               # Text similarity test
├── alembic.ini                          # Alembic migration configuration
├── requirements.txt                     # Python dependencies
└── README.md                            # Documentation
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** (Tested on Python 3.12)
- **PostgreSQL Database** running locally or on a remote host (e.g. Supabase, AWS RDS, Docker)
- An API Key for at least one AI provider:
  - [Google AI Studio](https://aistudio.google.com/) for **Gemini**
  - [OpenAI Platform](https://platform.openai.com/) for **OpenAI**
  - [OpenRouter](https://openrouter.ai/) for **OpenRouter** (Llama, Gemma, etc.)

---

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-resume-job-matcher.git
   cd ai-resume-job-matcher
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On Linux/macOS
   # .\venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

### Environment Variables Configuration

Create a `.env` file in the project root directory:

```env
# ==========================================
# Database Configuration
# ==========================================
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/resume_matcher_db

# ==========================================
# Active AI Provider ('gemini', 'openai', or 'openrouter')
# ==========================================
AI_PROVIDER=gemini

# ==========================================
# Google Gemini Configuration
# ==========================================
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
GEMINI_MAX_OUTPUT_TOKENS=8192

# ==========================================
# OpenAI Configuration
# ==========================================
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_MAX_TOKENS=4000

# ==========================================
# OpenRouter Configuration
# ==========================================
OPEN_ROUTER_API_KEY=your_openrouter_api_key_here
OPEN_ROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
OPEN_ROUTER_MAX_TOKENS=4000
```

---

### Database Migrations

Apply database schema migrations to PostgreSQL using Alembic:

```bash
alembic upgrade head
```

*(Alternatively, to create all tables directly via SQLAlchemy:)*
```bash
python3 -c "from app.database.connection import engine; from app.database.base import Base; import app.models; Base.metadata.create_all(bind=engine)"
```

---

### Running the Application

Start the development server with live reload enabled:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **Interactive API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Database Health Check**: [http://127.0.0.1:8000/health/database](http://127.0.0.1:8000/health/database)

---

## 📡 API Reference

### 1. Complete End-to-End Analysis

Execute the full extraction, matching, TF-IDF scoring, and AI recommendation pipeline in a single request.

- **Endpoint**: `POST /analysis/full`
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `file`: Resume file (`.pdf` or `.docx`, max 5 MB)
  - `job_title`: Target job title (e.g. `Senior Python Developer`)
  - `job_description`: Full text of the job description
  - `include_ai`: Boolean (`true` or `false`, defaults to `true`)

#### Sample cURL:
```bash
curl -X POST "http://127.0.0.1:8000/analysis/full" \
  -F "file=@/path/to/resume.pdf" \
  -F "job_title=Senior Backend Engineer" \
  -F "job_description=We are seeking a Python/FastAPI engineer with experience in PostgreSQL, Docker, and AWS." \
  -F "include_ai=true"
```

#### Sample Response:
```json
{
  "job_title": "Senior Backend Engineer",
  "resume_analysis": {
    "filename": "resume.pdf",
    "word_count": 480,
    "character_count": 3150,
    "skills": {
      "programming_languages": ["python", "javascript"],
      "backend": ["fastapi", "rest api"],
      "database": ["postgresql"],
      "cloud_devops": ["docker", "git"]
    },
    "total_skills": 7,
    "experience_mentions": ["4.5"],
    "education": [
      {
        "degree": "Bachelor of Technology",
        "institution": "Pune University",
        "dates": "07/2018 – 05/2022"
      }
    ]
  },
  "job_analysis": {
    "required_skills": {
      "backend": ["fastapi"],
      "database": ["postgresql"]
    },
    "preferred_skills": {
      "cloud_devops": ["aws"]
    },
    "experience_years": 4.0,
    "total_required_skills": 2,
    "total_preferred_skills": 1
  },
  "match_analysis": {
    "match_score": 85.0,
    "required_coverage": 100.0,
    "preferred_coverage": 25.0,
    "matched_required": ["fastapi", "postgresql"],
    "missing_required": [],
    "matched_preferred": ["docker"],
    "missing_preferred": ["aws"]
  },
  "text_similarity": 68.42,
  "ai_recommendations": {
    "overall_feedback": "Strong fit for the Python Backend role with demonstrated FastAPI API development experience.",
    "strengths": [
      {
        "title": "FastAPI & Microservices Architecture",
        "explanation": "Proven track record designing scalable REST APIs."
      }
    ],
    "weaknesses": [
      {
        "title": "Cloud Deployment Evidence",
        "explanation": "AWS is required by the role but not explicitly listed in work bullets.",
        "improvement": "Highlight specific AWS services used in production (e.g. ECS, S3, RDS)."
      }
    ],
    "missing_skills": [
      {
        "skill": "AWS",
        "reason": "Crucial for cloud infrastructure deployment mentioned in the JD.",
        "priority": "high"
      }
    ],
    "bullet_improvements": [
      {
        "original": "Built APIs for internal services.",
        "improved": "Architected high-throughput REST APIs using FastAPI and PostgreSQL, serving 15+ microservices with sub-50ms latency.",
        "explanation": "Quantifies technical scope and clarifies underlying tools without inventing facts."
      }
    ],
    "ats_recommendations": [
      "AWS ECS",
      "Asynchronous Python",
      "Unit Testing (pytest)"
    ]
  },
  "status": "success"
}
```

---

### 2. Resume Parsing & Extraction

Extract clean text, categorized skills, education details, and experience without running job comparison.

- **Endpoint**: `POST /resume/parse`
- **Content-Type**: `multipart/form-data`
- **Request Body**: `file` (PDF/DOCX)

---

### 3. Job Description Analysis

Extract skills and experience constraints from a job description.

- **Endpoint**: `POST /jobs/analyze`
- **Request Body**:
  ```json
  {
    "description": "Looking for a Python developer with 3+ years experience, FastAPI and Redis knowledge."
  }
  ```

---

### 4. Skill Matching & Scoring

Compare categorized candidate skills with job skills.

- **Endpoint**: `POST /matching/analyze`
- **Scoring Formula**:
  $$\text{Final Match Score} = (\text{Required Coverage} \times 0.8) + (\text{Preferred Coverage} \times 0.2)$$

---

### 5. AI Recommendations

Generate standalone structured recommendations for an existing text pair.

- **Endpoint**: `POST /ai/recommendations`
- **Request Body**:
  ```json
  {
    "resume_text": "Experienced Python Engineer...",
    "job_description": "We need a Senior Backend Developer..."
  }
  ```

---

### 6. Users, Resumes & Saved Jobs

| Route | Method | Description |
| :--- | :--- | :--- |
| `/users/` | `POST` | Register a new user |
| `/users/{id}` | `GET` | Get user details by ID |
| `/resumes/` | `POST` | Upload and store resume metadata in DB |
| `/resumes/{id}` | `GET` | Retrieve stored resume record |
| `/saved-jobs/` | `POST` | Save a job description to a user account |
| `/saved-jobs/user/{user_id}` | `GET` | List all saved jobs for a user |

---

## 🤖 AI Provider Configuration

The application features a clean, decoupled service architecture for LLM providers:

```text
app/services/
├── ai_gemini.py          # Google GenAI SDK integration
├── ai_openai.py          # OpenAI SDK integration (Structured Outputs)
├── ai_openrouter.py      # OpenRouter API integration
├── ai_resume_assistant.py# Unified dispatcher with auto-provider selection
└── json_utils.py         # Resilient JSON repair utility
```

### Switching Providers Dynamically:

1. **Via `.env`**:
   Set `AI_PROVIDER=gemini`, `AI_PROVIDER=openai`, or `AI_PROVIDER=openrouter`.
2. **Auto-Detection**:
   If `AI_PROVIDER` is not set, the dispatcher automatically selects whichever provider has an active API key in `.env`.
3. **In Code**:
   ```python
   from app.services.ai_resume_assistant import generate_resume_recommendations

   # Force specific provider:
   result = await generate_resume_recommendations(
       resume_text=resume_text,
       job_description=job_description,
       provider="gemini"  # or "openai", "openrouter"
   )
   ```

---

## 🧪 Running Tests

The test suite includes dedicated scripts to verify extraction accuracy and mathematical similarity calculations:

```bash
# Test skill, experience, and education extraction
python3 tests/test_skills.py

# Test TF-IDF text similarity
python3 tests/test_similarity.py
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

