# Secure DevOps Pipeline

A beginner-friendly DevSecOps project demonstrating automated
testing, Docker containerization, and security scanning.

## Objectives

- Build a small REST API with Python and Flask.
- Write automated tests with pytest.
- Package the application in a Docker image.
- Run tests automatically with GitHub Actions.
- Scan project files and the Docker image with Trivy.

## Architecture

Developer push
      |
      v
GitHub Actions
      |
      v
Python tests
      |
      v
Docker image build
      |
      v
Trivy security scans

## Technologies

- Python 3.12
- Flask
- pytest
- Docker
- GitHub Actions
- Trivy

## Run locally

Create a virtual environment:

    python -m venv .venv

Activate it in PowerShell:

    .\.venv\Scripts\Activate.ps1

Install dependencies:

    python -m pip install -r requirements-dev.txt

Run tests:

    python -m pytest -v

Start the API:

    python app.py

Open http://localhost:8000/health

## Run with Docker

Build the image:

    docker build -t secure-devops-api:1.0 .

Run the container:

    docker run --rm -p 8000:8000 secure-devops-api:1.0

Open http://localhost:8000/health

## API endpoints

| Method | Endpoint | Description |
| GET | / | API information |
| GET | /health | Health check |
| GET | /tasks | List tasks |
| POST | /tasks | Create a task |

## Security

The Docker image runs the application as a non-root user.
GitHub Actions runs automated tests and invokes Trivy scans
on the repository and Docker image.

The scans are informational in this initial version:
they do not block the pipeline based on vulnerability findings.

## Limitations

- Tasks are stored in memory and are not persistent.
- The application has no authentication.
- The pipeline does not publish the image or deploy the API.
- Passing tests and security scans do not guarantee security.

## Future improvements

- Add dependency pinning and automated dependency updates.
- Add a security gate for high and critical vulnerabilities.
- Publish versioned images to GitHub Container Registry.
- Add API authentication and persistent storage.
- Deploy to a test server.
