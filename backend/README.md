# Job Matcher — Backend

Backend service for the Job Matcher application, built with **FastAPI, PostgreSQL, Redis, and Gemini**.

The backend handles job data, CV processing, authentication, AI-powered job analysis, and job matching.

## Tech Stack

* Python 3.12
* FastAPI
* SQLAlchemy
* PostgreSQL 16
* Redis 7
* Gemini
* Pydantic
* Uvicorn
* Docker / Docker Compose
* Pytest
* DBeaver

## Features

* REST API built with FastAPI
* Job listing and pagination
* Job data ingestion
* PostgreSQL persistence
* Redis caching and rate limiting
* Google authentication
* CV upload and processing
* CV profile extraction
* AI-powered job requirement analysis
* Job matching based on:

  * Skills
  * Experience
  * Job roles
  * Languages
  * Education
  * Industries
* Structured API responses
* Request validation
* Centralized error handling
* Automated tests

## Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/       # API endpoints
│   │   └── router.py        # API router
│   │
│   ├── cache/               # Redis integration
│   ├── core/                # Application messages and status codes
│   ├── db/                  # Database session and configuration
│   ├── ingestion/           # Job data ingestion
│   ├── middleware/          # Request and rate-limit middleware
│   ├── models/              # SQLAlchemy models
│   ├── repositories/        # Database access layer
│   ├── schemas/             # Request and response schemas
│   ├── services/
│   │   ├── ai/              # Gemini and AI services
│   │   ├── auth.py          # Authentication
│   │   └── job.py           # Job business logic
│   └── main.py              # FastAPI application
│
├── config/
│   ├── dev_config.py
│   └── test_config.py
│
├── tests/
├── data/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Requirements

Make sure the following are installed:

* Python 3.12+
* Docker Desktop
* Git

## Environment Variables

Create the required environment configuration according to the project's environment setup.

The backend requires configuration for:

* PostgreSQL
* Redis
* Gemini
* Google authentication
* CORS
* Application environment

Do not commit `.env` files or secrets to the repository.

## Database and Redis

The project uses Docker Compose for local PostgreSQL and Redis services.

Start the services with:

```bash
docker compose up -d postgres redis
```

Check running containers:

```bash
docker ps
```

Stop the services with:

```bash
docker compose down
```

## Database Management with DBeaver

The PostgreSQL database can be inspected and managed locally using **DBeaver**.

The PostgreSQL Docker container exposes port `5432`.

Use the following connection settings:

```text
Host: localhost
Port: 5432
Database: <POSTGRES_DB>
Username: <POSTGRES_USER>
Password: <POSTGRES_PASSWORD>
```

The database credentials are configured through the backend environment variables.

### Connecting from DBeaver

1. Start the PostgreSQL container:

```bash
docker compose up -d postgres
```

2. Open DBeaver.
3. Create a new PostgreSQL connection.
4. Enter the connection details from your environment configuration.
5. Test the connection.
6. Connect to inspect the database tables and data.

DBeaver can be used during development to inspect jobs, candidate data, and other PostgreSQL records without accessing the database directly through the API.

## Python Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

and:

```text
http://127.0.0.1:8000/redoc
```

## Main API Areas

### Jobs

The jobs API provides access to available job positions, including pagination and job details.

Example:

```text
GET /jobs
```

### CV

The CV endpoint accepts an uploaded CV and processes it for matching.

Example:

```text
POST /cv/upload_cv
```

The CV flow includes:

```text
CV Upload
    ↓
CV Validation
    ↓
CV Parsing
    ↓
Candidate Profile
    ↓
Job Matching
    ↓
Ranked Matches
```

### Authentication

Protected endpoints use authentication through Google credentials.

Authentication information is validated before accessing protected resources.

## AI Job Analysis

Gemini is used to analyze job requirements and extract structured information such as required skills.

The AI layer is separated from the application business logic under:

```text
app/services/ai/
```

This keeps AI-specific functionality isolated from the rest of the application.

## Job Matching

The matching system compares the candidate profile against job requirements.

Matching considers multiple factors, including:

```text
Candidate Profile
       │
       ├── Skills
       ├── Experience
       ├── Roles
       ├── Languages
       ├── Education
       └── Industries
              │
              ↓
        Job Requirements
              │
              ↓
        Matching Score
              │
              ↓
        Ranked Jobs
```

## Data Flow

The general backend flow is:

```text
Job Sources
    ↓
Ingestion
    ↓
Validation / Mapping
    ↓
PostgreSQL
    ↓
Job API
    ↓
Frontend
```

For CV matching:

```text
CV
 ↓
CV Upload API
 ↓
CV Processing
 ↓
Candidate Profile
 ↓
AI / Matching Services
 ↓
Ranked Job Matches
 ↓
Frontend
```

## Testing

Run the test suite with:

```bash
pytest
```

For a more detailed output:

```bash
pytest -v
```

Integration tests that require external AI services can be run separately according to the project's test configuration.

## API Architecture

The backend follows a layered architecture:

```text
API Endpoints
      ↓
Services
      ↓
Repositories
      ↓
Database
```

AI functionality is isolated in:

```text
Services
   └── AI
       ├── Gemini
       └── Job Analyzer
```

Schemas are used to define structured request and response data between application layers.

## Development

The project is organized to keep responsibilities separated between:

* API endpoints
* Business logic
* Data access
* AI services
* Database models
* Request/response schemas
* Infrastructure services

This structure makes the backend easier to test, maintain, and extend.

## License

This project is currently developed as a personal portfolio project.
