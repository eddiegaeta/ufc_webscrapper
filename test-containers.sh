#!/bin/bash

# UFC Web Scraper - Container Test Script
# Run this script to test your Docker containers

set -e

echo "🚀 Starting UFC Web Scraper Container Tests"
echo "==========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Step 1: Validate docker-compose file
echo "1️⃣  Validating docker-compose.yml..."
if docker-compose config --quiet; then
    print_success "Docker Compose configuration is valid"
else
    print_error "Docker Compose configuration has errors"
    exit 1
fi
echo ""

# Step 2: Check if ports are available
echo "2️⃣  Checking if required ports are available..."
if lsof -Pi :3306 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_error "Port 3306 is already in use"
    echo "   Run: sudo lsof -i :3306 to see what's using it"
else
    print_success "Port 3306 is available"
fi

if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_error "Port 3000 is already in use"
    echo "   Run: sudo lsof -i :3000 to see what's using it"
else
    print_success "Port 3000 is available"
fi
echo ""

# Step 3: Build containers
echo "3️⃣  Building Docker containers..."
print_info "This may take a few minutes..."
if docker-compose build; then
    print_success "All containers built successfully"
else
    print_error "Failed to build containers"
    exit 1
fi
echo ""

# Step 4: Start containers
echo "4️⃣  Starting containers..."
if docker-compose up -d; then
    print_success "All containers started"
else
    print_error "Failed to start containers"
    exit 1
fi
echo ""

# Step 5: Wait for MySQL to be ready
echo "5️⃣  Waiting for MySQL to be ready..."
MAX_TRIES=30
COUNTER=0
while [ $COUNTER -lt $MAX_TRIES ]; do
    if docker exec mysql01 mysqladmin ping -h localhost -u root -ppassword --silent 2>/dev/null; then
        print_success "MySQL is ready"
        break
    fi
    COUNTER=$((COUNTER+1))
    if [ $COUNTER -eq $MAX_TRIES ]; then
        print_error "MySQL failed to start within 60 seconds"
        echo "Check logs with: docker-compose logs mysql"
        exit 1
    fi
    sleep 2
    echo -n "."
done
echo ""

# Step 6: Check database
echo "6️⃣  Verifying database..."
if docker exec mysql01 mysql -u ufc_user -ppassword -e "USE ufc_events; SHOW TABLES;" >/dev/null 2>&1; then
    print_success "Database 'ufc_events' is accessible"
    
    # Show tables
    echo "   Tables in database:"
    docker exec mysql01 mysql -u ufc_user -ppassword ufc_events -e "SHOW TABLES;" 2>/dev/null | tail -n +2 | sed 's/^/   - /'
else
    print_error "Cannot access database"
fi
echo ""

# Step 7: Test web scraper
echo "7️⃣  Testing web scraper..."
print_info "Running scraper manually..."
if docker-compose exec -T webscraper python /app/webscrapper_ufc.py; then
    print_success "Web scraper executed successfully"
    
    # Check if data was inserted
    EVENT_COUNT=$(docker exec mysql01 mysql -u ufc_user -ppassword ufc_events -se "SELECT COUNT(*) FROM events;" 2>/dev/null)
    if [ "$EVENT_COUNT" -gt 0 ]; then
        print_success "Found $EVENT_COUNT events in database"
    else
        print_error "No events found in database"
    fi
else
    print_error "Web scraper failed"
    echo "Check logs with: docker-compose logs webscraper"
fi
echo ""

# Step 8: Test API
echo "8️⃣  Testing API..."
sleep 3  # Give API time to start
if curl -s http://localhost:3000/api/events > /dev/null; then
    print_success "API is responding"
    echo "   Test it: curl http://localhost:3000/api/events"
    echo "   Or open: http://localhost:3000"
else
    print_error "API is not responding"
    echo "Check logs with: docker-compose logs api"
fi
echo ""

# Step 9: Show container status
echo "9️⃣  Container Status:"
docker-compose ps
echo ""

# Final instructions
echo "==========================================="
echo "🎉 Container Testing Complete!"
echo ""
echo "📝 Useful Commands:"
echo "   View logs:        docker-compose logs -f"
echo "   Stop containers:  docker-compose down"
echo "   Restart:          docker-compose restart"
echo "   Clean up:         docker-compose down -v"
echo ""
echo "🌐 Access Points:"
echo "   API:              http://localhost:3000"
echo "   MySQL:            localhost:3306"
echo ""
print_info "Containers are running in the background"
print_info "Use 'docker-compose logs -f' to follow logs"
