# Testing Docker Containers

This guide helps you test all three containerized services locally using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed
- Ports 3000 (API) and 3306 (MySQL) available

## Quick Start

### 1. Build and Start All Services

```bash
# Build and start all containers
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

### 2. View Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f mysql
docker-compose logs -f webscraper
docker-compose logs -f api
```

### 3. Check Service Status

```bash
docker-compose ps
```

### 4. Test Individual Services

#### Test MySQL Database
```bash
# Connect to MySQL
docker exec -it mysql01 mysql -u ufc_user -ppassword ufc_events

# Or from host (if mysql client installed)
mysql -h 127.0.0.1 -P 3306 -u ufc_user -ppassword ufc_events
```

#### Test Web Scraper
```bash
# Run scraper manually
docker-compose exec webscraper python /app/webscrapper_ufc.py

# Check if data was inserted
docker exec -it mysql01 mysql -u ufc_user -ppassword ufc_events -e "SELECT COUNT(*) FROM events;"
```

#### Test API
```bash
# Test API endpoint
curl http://localhost:3000/api/events

# Or open in browser
http://localhost:3000
```

### 5. Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

## Testing Individual Containers

### Build and Test MySQL Only
```bash
docker build -t ufc-mysql ./ufc_mysql_db
docker run -d --name mysql01 \
  -e MYSQL_ROOT_PASSWORD=password \
  -e MYSQL_DATABASE=ufc_events \
  -e MYSQL_USER=ufc_user \
  -e MYSQL_PASSWORD=password \
  -p 3306:3306 \
  ufc-mysql
```

### Build and Test Web Scraper Only
```bash
# First ensure MySQL is running
docker build -t ufc-scraper ./ufc_python_webscrapper

# Create network if not exists
docker network create dev_network
docker network connect dev_network mysql01

# Run scraper
docker run --rm --name ufc_webscrapper \
  --network dev_network \
  -e DB_HOST=mysql01 \
  -e DB_PORT=3306 \
  -e DB_USER=ufc_user \
  -e DB_PASS=password \
  -e DB_NAME=ufc_events \
  ufc-scraper
```

### Build and Test API Only
```bash
docker build -t ufc-api ./ufc_nodejs_api
docker run -d --name ufc_scrapper_api \
  --network dev_network \
  -e DB_HOST=mysql01 \
  -e DB_PORT=3306 \
  -e DB_USER=ufc_user \
  -e DB_PASS=password \
  -e DB_NAME=ufc_events \
  -p 3000:3000 \
  ufc-api
```

## Troubleshooting

### Container won't start
```bash
# Check container logs
docker logs <container_name>

# Inspect container
docker inspect <container_name>
```

### Database connection issues
```bash
# Check if MySQL is ready
docker exec mysql01 mysqladmin ping -h localhost -u root -ppassword

# Verify network connectivity
docker exec webscraper ping -c 3 mysql
```

### Port already in use
```bash
# Find what's using the port
sudo lsof -i :3306  # or :3000

# Stop the service or change port in docker-compose.yml
```

### Reset everything
```bash
# Stop all containers and remove volumes
docker-compose down -v

# Remove all related containers and images
docker rm -f mysql01 ufc_webscrapper ufc_scrapper_api
docker rmi ufc-mysql ufc-scraper ufc-api

# Rebuild from scratch
docker-compose up --build
```

## Environment Variables

The following environment variables are configured in `docker-compose.yml`:

- `DB_HOST`: Database hostname (mysql in container network)
- `DB_PORT`: Database port (3306)
- `DB_USER`: Database user (ufc_user)
- `DB_PASS`: Database password (password)
- `DB_NAME`: Database name (ufc_events)

**Note**: Change these values for production deployments!

## Kubernetes Deployment

For Kubernetes deployment, see the YAML files in `k8s_yamls/` directory.
