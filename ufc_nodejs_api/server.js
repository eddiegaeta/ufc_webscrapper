const express = require('express');
const path = require('path');
const mysql = require('mysql2');
const moment = require('moment-timezone');
require('dotenv').config();

const app = express();
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

    connection.query('SELECT * FROM events', function (error, results) {
        if (error) {
            console.error('Error executing query:', error);
            res.status(500).send('Internal Server Error');
            return;
        }

        const now = moment();

        const futureEvents = results.filter(event => {
            const eventDate = moment(event.event_date, 'ddd, MMM D , h:mm A z');
            return eventDate.isSameOrAfter(now);
        }).sort((a, b) => {
            const dateA = moment(a.event_date, 'ddd, MMM D , h:mm A z');
            const dateB = moment(b.event_date, 'ddd, MMM D , h:mm A z');
            return dateA - dateB;
        });

        res.json(futureEvents);
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