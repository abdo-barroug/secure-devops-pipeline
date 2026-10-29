
# Secure DevOps Pipeline

[![Secure DevOps Pipeline](https://github.com/abdo-barroug/secure-devops-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/abdo-barroug/secure-devops-pipeline/actions/workflows/ci.yml)

A beginner-friendly **DevSecOps / CI/CD project** demonstrating automated testing, Docker containerization, security scanning, and automated image publishing to GitHub Container Registry (GHCR).

The goal is to build a Python REST API and automate the steps required to test, scan, package, and publish it.

## Features

- REST API built with Python and Flask.
- Automated tests using pytest.
- Docker containerization with a non-root application user.
- Continuous integration with GitHub Actions.
- Filesystem security scanning with Trivy.
- Docker image vulnerability scanning with Trivy.
- Automated Docker image publishing to GitHub Container Registry.
- SHA-based image tags for identifying specific builds.
- Automated pipeline triggered by pushes and pull requests.

## Architecture

```text
Developer pushes code to main
             |
             v
       GitHub Actions
             |
             v
       Run pytest tests
             |
             v
    Scan repository with Trivy
             |
             v
       Build Docker image
             |
             v
     Scan Docker image
             |
             v
       Publish image to GHCR
```

The publishing job runs only after the tests, build, and security scans succeed. Pull requests run the test and security workflow but do not publish an image.

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.12 | Application language |
| Flask | REST API framework |
| pytest | Automated testing |
| Docker | Containerization |
| GitHub Actions | CI/CD automation |
| Trivy | Vulnerability, secret, and misconfiguration scanning |
| GitHub Container Registry (GHCR) | Docker image storage |

## Project Structure

```text
secure-devops-pipeline/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app.py
├── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/abdo-barroug/secure-devops-pipeline.git
cd secure-devops-pipeline
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements-dev.txt
```

### 4. Run automated tests

```bash
python -m pytest -v
```

### 5. Start the API

```bash
python app.py
```

Open the health endpoint:

http://localhost:8000/health

## Run with Docker

### 1. Build the image

```bash
docker build -t secure-devops-api:1.0 .
```

### 2. Run the container

```bash
docker run --rm -p 8000:8000 secure-devops-api:1.0
```

### 3. Test the application

Open:

http://localhost:8000/health

To stop the application, press `Ctrl+C` in the terminal running the container.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/tasks` | List tasks |
| POST | `/tasks` | Create a task |

### Example: Create a Task

Using PowerShell:

```powershell
$body = @{ title = "Learn DevSecOps" } | ConvertTo-Json

Invoke-RestMethod `
  -Uri http://localhost:8000/tasks `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

List tasks:

```powershell
Invoke-RestMethod http://localhost:8000/tasks
```

Tasks are stored in memory and are not persistent. They are lost when the application restarts.

## CI/CD Pipeline

The GitHub Actions workflow is defined in `.github/workflows/ci.yml`.

The pipeline performs the following steps:

1. Checks out the source code.
2. Sets up Python 3.12.
3. Installs project dependencies.
4. Runs automated tests with pytest.
5. Scans repository files with Trivy.
6. Builds the Docker image.
7. Scans the Docker image with Trivy.
8. Publishes the image to GHCR if the previous jobs succeed.

The workflow runs on:

- Pushes to the `main` branch.
- Pull requests targeting `main`.
- Manual workflow dispatch.

Pull requests do not publish images. Publishing occurs on pushes to `main` and manual runs.

## Security

This project integrates security checks into the CI/CD pipeline.

- **Non-root container:** the application runs as a non-root user inside the Docker image.
- **Filesystem scanning:** Trivy scans for vulnerabilities, exposed secrets, and configuration issues.
- **Container scanning:** Trivy scans operating-system packages and application libraries for vulnerabilities.
- **Security gate:** scans are configured to fail on findings matching the selected severity criteria.
- **Registry authentication:** GitHub Actions uses the temporary `GITHUB_TOKEN` with package-write permission to publish the image.

The scans focus on `HIGH` and `CRITICAL` findings. The container scan ignores unfixed vulnerabilities.

A successful pipeline does not guarantee that the application is completely secure. Results depend on the scanner version, configuration, vulnerability database, and selected severity filters.

## Published Docker Image

The image is published to GitHub Container Registry:

`ghcr.io/abdo-barroug/secure-devops-api`

### Pull the latest image

```bash
docker pull ghcr.io/abdo-barroug/secure-devops-api:latest
```

### Run the published image

```bash
docker run --rm -p 8000:8000 ghcr.io/abdo-barroug/secure-devops-api:latest
```

Open:

http://localhost:8000/health

### Pull a specific build

Each published build is also tagged with its Git commit SHA.

```bash
docker pull ghcr.io/abdo-barroug/secure-devops-api:<commit-sha>
```

Replace `<commit-sha>` with the relevant commit SHA.

If the package is private, authenticate to GHCR before pulling the image.

## Limitations

- Tasks are stored in memory and are not persistent.
- The API does not implement authentication or authorization.
- The project does not include deployment to a remote server.
- The security scans cover the configured checks and do not guarantee complete security.

## Future Improvements

- Add persistent storage using a database.
- Implement API authentication and authorization.
- Automate dependency updates.
- Add code-quality checks and static analysis.
- Deploy the application to a test environment.
- Add monitoring and structured logging.

## Author

**Abdellah Barroug**

Computer Engineering Student | Cybersecurity & DevSecOps

- GitHub: [abdo-barroug](https://github.com/abdo-barroug)
- Project: [Secure DevOps Pipeline](https://github.com/abdo-barroug/secure-devops-pipeline)
