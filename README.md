# Flask Application with Docker Best Practices

This is a Flask application containerized with Docker following DevOps best practices for security, performance, and maintainability. The application provides a weather API service using the Open-Meteo API.

## 🚀 Features

- **Multi-stage Docker build** for smaller production images
- **Non-root user** for enhanced security
- **Health checks** for container monitoring
- **Production-ready configuration** with environment variables
- **Security hardening** with read-only filesystem and no-new-privileges
- **Optimized layer caching** for faster builds
- **Weather API integration** with Open-Meteo service
- **JSON API endpoints** with proper response formatting

## 🏗️ Architecture

The application uses a multi-stage Docker build:

- **Builder stage**: Installs dependencies and creates virtual environment
- **Production stage**: Creates minimal runtime image with security hardening

### API Endpoints

- `GET /` - Welcome page
- `GET /health` - Health check endpoint
- `GET /weather` - Weather forecast endpoint (requires latitude and longitude parameters)

## 📦 Quick Start

### Using Docker Compose (Recommended)

```bash
# Production deployment
docker-compose up -d

# Development mode
docker-compose --profile dev up -d app-dev
```

### Using Docker directly

```bash
# Build the image
docker build -t flask-app .

# Run in production mode
docker run -d \
  --name flask-app \
  -p 5851:5851 \
  -e FLASK_ENV=production \
  flask-app
```

## 🔧 Configuration

### Environment Variables

| Variable     | Default      | Description                                |
| ------------ | ------------ | ------------------------------------------ |
| `FLASK_ENV`  | `production` | Flask environment (development/production) |
| `FLASK_APP`  | `app.py`     | Flask application entry point              |
| `FLASK_HOST` | `0.0.0.0`    | Host to bind Flask server                  |
| `FLASK_PORT` | `5851`       | Port to bind Flask server                  |

### Health Check

The application includes a health check endpoint at `/health` that returns:

```json
{ "status": "healthy" }
```

### Weather API

The application provides a weather forecast endpoint that integrates with the Open-Meteo API:

```bash
# Get weather forecast for specific coordinates
curl "http://localhost:5851/weather?latitude=40.7128&longitude=-74.0060"
```

**Parameters:**

- `latitude` (required): Latitude coordinate (-90 to 90)
- `longitude` (required): Longitude coordinate (-180 to 180)

**Response:** JSON weather data from Open-Meteo API

## 🔒 Security Features

- **Non-root user**: Application runs as `appuser` instead of root
- **Read-only filesystem**: Container filesystem is read-only except for `/tmp` and `/var/tmp`
- **No new privileges**: Container cannot gain additional privileges
- **Minimal base image**: Uses Python slim image for smaller attack surface
- **Pinned dependencies**: All Python packages are version-pinned
- **Multi-stage build**: Build tools are not included in production image

## 📊 Monitoring

### Health Check

```bash
# Check container health
docker ps
docker inspect <container_name> | grep Health -A 10

# Manual health check
curl http://localhost:5851/health
```

### Logs

```bash
# View application logs
docker-compose logs -f app

# View logs for specific container
docker logs <container_name>
```

## 🛠️ Development

### Local Development

```bash
# Run in development mode
docker-compose --profile dev up -d app-dev

# Access application
curl http://localhost:5852/
```

### Building for Different Environments

```bash
# Build production image
docker build --target production -t flask-app:prod .

# Build development image
docker build --target builder -t flask-app:dev .
```

## 📋 Best Practices Implemented

### Docker Best Practices

- ✅ Multi-stage builds for smaller images
- ✅ Non-root user for security
- ✅ Health checks for monitoring
- ✅ Proper layer caching
- ✅ Read-only filesystem
- ✅ No new privileges
- ✅ Minimal base image
- ✅ Proper labels and metadata

### Security Best Practices

- ✅ Pinned base image version
- ✅ Pinned dependency versions
- ✅ Non-root user execution
- ✅ Read-only filesystem
- ✅ Security options enabled
- ✅ Minimal attack surface

### Performance Best Practices

- ✅ Optimized layer caching
- ✅ Multi-stage builds
- ✅ Minimal production image
- ✅ Efficient dependency installation

## 🚨 Security Considerations

1. **Never run containers as root** - This application runs as `appuser`
2. **Use read-only filesystem** - Implemented with `read_only: true`
3. **Pin all dependencies** - All versions are explicitly specified
4. **Regular security updates** - Keep base images and dependencies updated
5. **Network security** - Use custom networks and limit port exposure

## 📝 Troubleshooting

### Common Issues

1. **Permission denied errors**

   - Ensure files are owned by `appuser:appuser`
   - Check file permissions in mounted volumes

2. **Health check failures**

   - Verify the application is running on the correct port
   - Check if the `/health` endpoint is accessible

3. **Build failures**
   - Ensure all dependencies are properly specified in `requirements.txt`
   - Check for syntax errors in Dockerfile

### Debug Mode

```bash
# Run with debug output
docker-compose up app

# Access container shell
docker exec -it <container_name> /bin/bash
```

## 📄 License

This project follows security best practices for containerized applications. Always review and update security configurations based on your specific requirements.
