const express = require('express');
const path = require('path');
const app = express();
const mysql = require('mysql2');
require('dotenv').config();
const moment = require('moment-timezone');
const cors = require('cors');

const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Create connection pool for better performance
const pool = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
    enableKeepAlive: true,
    keepAliveInitialDelay: 0
});

const promisePool = pool.promise();

// Health check endpoint
app.get('/health', async (req, res) => {
    try {
        await promisePool.query('SELECT 1');
        res.status(200).json({
            status: 'healthy',
            timestamp: new Date().toISOString(),
            database: 'connected'
        });
    } catch (error) {
        console.error('Health check failed:', error);
        res.status(503).json({
            status: 'unhealthy',
            timestamp: new Date().toISOString(),
            database: 'disconnected',
            error: error.message
        });
    }
});

// API endpoint to get upcoming events
app.get('/api/events', async (req, res) => {
    try {
        const limit = parseInt(req.query.limit) || 8;
        
        // Validate limit
        if (limit < 1 || limit > 50) {
            return res.status(400).json({
                error: 'Invalid limit parameter. Must be between 1 and 50.'
            });
        }

        // Simple query - just get all events and let client-side handle date filtering
        // The date format from scraper is complex and varies (EST/EDT)
        const query = `
            SELECT * FROM events 
            ORDER BY event_date
            LIMIT ?
        `;
        
        const [results] = await promisePool.query(query, [limit]);
        
        res.json({
            count: results.length,
            events: results
        });
    } catch (error) {
        console.error('Error fetching events:', error);
        res.status(500).json({
            error: 'Internal Server Error',
            message: process.env.NODE_ENV === 'development' ? error.message : undefined
        });
    }
});

// API endpoint to get event by URL
app.get('/api/events/:eventUrl', async (req, res) => {
    try {
        const eventUrl = decodeURIComponent(req.params.eventUrl);
        const query = 'SELECT * FROM events WHERE event_url = ?';
        
        const [results] = await promisePool.query(query, [eventUrl]);
        
        if (results.length === 0) {
            return res.status(404).json({
                error: 'Event not found'
            });
        }
        
        res.json(results[0]);
    } catch (error) {
        console.error('Error fetching event:', error);
        res.status(500).json({
            error: 'Internal Server Error',
            message: process.env.NODE_ENV === 'development' ? error.message : undefined
        });
    }
});

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

// The "catchall" handler: for any request that doesn't match "/api", send back React's index.html file.
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});

// Graceful shutdown
const gracefulShutdown = async () => {
    console.log('Received shutdown signal, closing server gracefully...');
    
    server.close(async () => {
        console.log('HTTP server closed');
        
        try {
            await pool.end();
            console.log('Database pool closed');
            process.exit(0);
        } catch (error) {
            console.error('Error closing database pool:', error);
            process.exit(1);
        }
    });
    
    // Force close after 10 seconds
    setTimeout(() => {
        console.error('Forcing shutdown after timeout');
        process.exit(1);
    }, 10000);
};

process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

const server = app.listen(PORT, () => {
    console.log(`Node.js API server running on port ${PORT}`);
    console.log(`Health check available at http://localhost:${PORT}/health`);
});