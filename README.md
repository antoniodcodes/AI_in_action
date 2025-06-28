# AI_in_action

A simple Flask web application that displays "Hello World" when accessed.

## Project Overview

This is a basic Flask application that runs on port 5851 and serves a simple "Hello World" message. The application is containerized using Docker for easy deployment and distribution.

## Prerequisites

Before deploying this application, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (optional, for easier management)

## Docker Deployment Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AI_In_Action
```

### 2. Build the Docker Image

```bash
docker build -t ai-in-action .
```

This command will:

- Use Python 3.11 slim image as the base
- Install all dependencies from `requirements.txt`
- Copy the application code to the container
- Set up the working directory and environment variables

### 3. Run the Docker Container

```bash
docker run -d -p 5851:5851 --name ai-in-action-app ai-in-action
```

**Parameters explained:**

- `-d`: Run the container in detached mode (background)
- `-p 5851:5851`: Map port 5851 from the host to port 5851 in the container
- `--name ai-in-action-app`: Give the container a friendly name
- `ai-in-action`: The name of the Docker image to run

### 4. Verify the Deployment

Once the container is running, you can access the application by opening your web browser and navigating to:

```
http://localhost:5851
```

You should see "Hello World" displayed in your browser.

### 5. Container Management

**Stop the container:**

```bash
docker stop ai-in-action-app
```

**Start the container:**

```bash
docker start ai-in-action-app
```

**Remove the container:**

```bash
docker rm ai-in-action-app
```

**View container logs:**

```bash
docker logs ai-in-action-app
```

**View running containers:**

```bash
docker ps
```

## Alternative: Using Docker Compose

If you prefer using Docker Compose for easier management, create a `docker-compose.yml` file:

```yaml
version: "3.8"
services:
  ai-in-action:
    build: .
    ports:
      - "5851:5851"
    container_name: ai-in-action-app
    restart: unless-stopped
```

Then run:

```bash
docker-compose up -d
```

To stop:

```bash
docker-compose down
```

## Development

### Local Development Setup

1. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python app.py
```

The application will be available at `http://localhost:5851`

## Project Structure

```
AI_In_Action/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── README.md          # This file
└── .gitignore         # Git ignore rules
```

## Troubleshooting

### Common Issues

1. **Port already in use**: If port 5851 is already in use, you can map to a different port:

   ```bash
   docker run -d -p 8080:5851 --name ai-in-action-app ai-in-action
   ```

   Then access the app at `http://localhost:8080`

2. **Container won't start**: Check the logs for errors:

   ```bash
   docker logs ai-in-action-app
   ```

3. **Build fails**: Ensure all files are present and the Dockerfile is in the root directory.

## License

[Add your license information here]
