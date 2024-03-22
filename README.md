# Resume Matcher API

This project runs off Django Framework and is the backend for the Kompletion Resume Matcher

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Installation

1. Clone the repository
   ```
   git clone <repository_url>
   ```
2. Navigate to the project directory
   ```
   cd <project_directory>
   ```
3. Start the Docker container
   ```
   docker-compose up
   ```

### Database Migrations

To make database migrations, use the following command:
`docker-compose exec web python manage.py migrate`

### Restarting and Running service

```
docker-compose down
docker-compose up -d
```

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Docker](https://www.docker.com/) - Used for containerization

## Dependency Management

This project uses [Poetry](https://python-poetry.org/) for dependency management. Poetry is a tool for Python application package management. It not only handles dependencies but also is capable of building, packaging, and publishing Python packages.

Windows Users run:

```
cd venv_scripts
./create_venv_windows.bat
```

Mac users run:

```
cd venv_scripts
./setup_venv_mac.sh
```
