const express = require('express');
const path = require('path');
const app = express();
const mysql = require('mysql2');
require('dotenv').config();
const moment = require('moment-timezone');

const PORT = process.env.PORT || 3000;

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

app.get('/api/events', (req, res) => {
    const connection = mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME
    });

    connection.connect();

    const now = moment().tz('America/Los_Angeles').format('ddd, MMM D , h:mm A z'); // Adjust timezone as needed
    const query = 'SELECT * FROM events WHERE STR_TO_DATE(event_date, "%a, %b %e , %l:%i %p %Z ") >= STR_TO_DATE(?, "%a, %b %e , %l:%i %p %Z ") ORDER BY STR_TO_DATE(event_date, "%a, %b %e , %l:%i %p %Z ") LIMIT 8';
    
    connection.query(query, [now], function (error, results, fields) {
        if (error) {
            console.error('Error executing query:', error);
            res.status(500).send('Internal Server Error');
            return;
        }

        res.json(results);
    });

    connection.end();
});

// The "catchall" handler: for any request that doesn't match "/api", send back React's index.html file.
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'client/build', 'index.html'));
});

app.listen(PORT, () => {
    console.log(`Node is running on port ${PORT}`);
});