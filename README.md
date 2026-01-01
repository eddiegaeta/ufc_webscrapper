# UFC Event Web Scraper & Dashboard

A full-stack application that automatically scrapes UFC event data and displays it through a modern web interface.

## 🏗️ Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│                 │      │                  │      │                 │
│  Python Scraper │─────▶│  MySQL Database  │◀─────│   Node.js API   │
│  (BeautifulSoup)│      │                  │      │   + React UI    │
│                 │      │                  │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
        ↓                                                     ↓
   Cron Job                                           Web Dashboard
  (Every 5 min)                                    (localhost:3000)
```

## 🚀 Features

### Backend
- **🕷️ Web Scraper**: Automated scraping of UFC.com for upcoming events
- **🔄 Retry Logic**: Exponential backoff for failed requests
- **📊 Structured Logging**: Comprehensive logging with timestamps and log levels
- **⚡ Connection Pooling**: Efficient database connections in Node.js API
- **🏥 Health Checks**: Monitoring endpoints for container orchestration
- **🔒 CORS Support**: Secure cross-origin resource sharing
- **⏱️ Rate Limiting**: Respectful scraping with delays

### Frontend
- **🎨 Modern UI**: Clean, responsive design with UFC branding
- **🔍 Search & Filter**: Find events by title, location, or venue
- **⏰ Countdown Timer**: Real-time countdown to each event
- **📱 Responsive Design**: Works on desktop, tablet, and mobile
- **🥊 Fight Cards**: View complete fighter matchups per event

### DevOps
- **🐳 Docker**: Containerized services for easy deployment
- **☸️ Kubernetes**: Ready for k8s deployment with provided YAML files
- **📝 Documentation**: Comprehensive setup and testing guides
- **🔧 Environment Templates**: .env.example files for quick setup

## 📦 Services

### 1. Python Web Scraper
- Scrapes UFC.com every 5 minutes via cron
- Extracts event details, dates, venues, and fight cards
- Stores data in MySQL database
- Built-in error handling and retry logic

### 2. MySQL Database
- Stores event information with proper indexing
- Automatic timestamp tracking
- Optimized queries for performance

### 3. Node.js API + React Frontend
- RESTful API with connection pooling
- Modern React dashboard
- Real-time event countdown
- Search and filter capabilities

## 🛠️ Tech Stack

**Backend:**
- Python 3.8+ (BeautifulSoup, Requests, MySQL Connector)
- Node.js 18+ (Express)
- MySQL 8.4

**Frontend:**
- React
- Axios
- CSS3 with modern animations

**DevOps:**
- Docker & Docker Compose
- Kubernetes
- GitHub Actions (optional CI/CD)

## 🚦 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000 (API) and 3306 (MySQL) available

### 1. Clone Repository
```bash
git clone https://github.com/eddiegaeta/ufc_webscrapper.git
cd ufc_webscrapper
```

### 2. Set Up Environment Variables
```bash
# Copy example files
cp .env.example .env
cp ufc_nodejs_api/.env.example ufc_nodejs_api/.env
cp ufc_python_webscrapper/.env.example ufc_python_webscrapper/.env

# Edit with your credentials
nano .env
```

### 3. Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 4. Access the Dashboard
Open your browser to: `http://localhost:3000`

### 5. Check Health Status
```bash
curl http://localhost:3000/health
```

## 📖 Detailed Setup

See [DOCKER_TESTING.md](DOCKER_TESTING.md) for:
- Individual container testing
- Troubleshooting guide
- Manual deployment steps
- Database verification

## 🧪 Testing

### Automated Testing Script
```bash
chmod +x test-containers.sh
./test-containers.sh
```

This script will:
- ✅ Validate Docker Compose configuration
- ✅ Check port availability
- ✅ Build all containers
- ✅ Start services with health checks
- ✅ Test the web scraper
- ✅ Verify database connectivity
- ✅ Test API endpoints

### Manual Testing
```bash
# Test scraper directly
docker exec ufc_webscrapper python3 /app/webscrapper_ufc.py

# Query database
docker exec mysql01 mysql -u ufc_user -ppassword ufc_events \\
  -e "SELECT event_title, event_date FROM events LIMIT 5;"

# Test API
curl http://localhost:3000/api/events
```

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check status |
| `/api/events` | GET | Get upcoming events (limit=8) |
| `/api/events?limit=20` | GET | Get up to 20 events |
| `/api/events/:eventUrl` | GET | Get specific event details |

## 📁 Project Structure

```
ufc_webscrapper/
├── ufc_python_webscrapper/    # Python scraper
│   ├── webscrapper_ufc.py     # Main scraper script
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile
│   └── .env.example
├── ufc_nodejs_api/            # Node.js API + React UI
│   ├── server.js              # Express API
│   ├── package.json
│   ├── Dockerfile
│   ├── client/                # React frontend
│   │   └── src/
│   │       ├── Events.js      # Main component
│   │       └── Events.css
│   └── .env.example
├── ufc_mysql_db/              # MySQL setup
│   ├── init.sql
│   ├── Dockerfile
│   └── my.cnf
├── k8s_yamls/                 # Kubernetes manifests
├── docker-compose.yml         # Multi-container orchestration
├── test-containers.sh         # Automated testing
└── DOCKER_TESTING.md          # Testing guide
```

## 🔧 Environment Variables

### Required Variables
```bash
DB_HOST=mysql              # Database hostname
DB_PORT=3306              # Database port
DB_USER=ufc_user          # Database user
DB_PASS=your_password     # Database password
DB_NAME=ufc_events        # Database name
```

### Optional Variables
```bash
PORT=3000                 # API port (default: 3000)
NODE_ENV=development      # Environment mode
```

## 📊 Database Schema

```sql
CREATE TABLE events (
    event_title VARCHAR(255),
    event_date VARCHAR(255),
    event_url VARCHAR(255) PRIMARY KEY,
    event_type VARCHAR(15),
    event_all_fighters TEXT,
    event_venue VARCHAR(255),
    event_location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_event_date (event_date),
    INDEX idx_event_type (event_type)
);
```

## 🐛 Troubleshooting

### Scraper Not Working
```bash
# Check scraper logs
docker logs ufc_webscrapper

# Run scraper manually
docker exec -it ufc_webscrapper python3 /app/webscrapper_ufc.py
```

### Database Connection Issues
```bash
# Verify MySQL is running
docker exec mysql01 mysqladmin ping -h localhost -u root -ppassword

# Check network connectivity
docker exec ufc_webscrapper ping -c 3 mysql
```

### Frontend Not Loading
```bash
# Rebuild React app
docker-compose build api
docker-compose up -d api
```

## 🤝 Contributing

This project is for personal learning and benefit. Feedback and advice are welcome, but no pull requests at this time.

## 📝 License

This project is for educational and personal use only.

## 🙏 Acknowledgments

- UFC.com for event data
- BeautifulSoup for web scraping capabilities
- The open-source community

## 📧 Contact

Ed Gaeta - GitHub: [@eddiegaeta](https://github.com/eddiegaeta)

---

**Note:** This scraper is for personal use only. Please respect UFC.com's terms of service and implement appropriate rate limiting.
