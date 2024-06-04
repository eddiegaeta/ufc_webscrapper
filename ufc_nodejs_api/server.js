const express = require('express');
const path = require('path');
const mysql = require('mysql2');
const app = express();
require('dotenv').config();

// Serve static files from the React app
app.use(express.static(path.join(__dirname, 'client/build')));

app.get('/api/events', (req, res) => {
    const connection = mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME
    });

    connection.connect((err) => {
        if (err) {
            console.error('Error connecting to MySQL:', err);
            res.status(500).send('Internal Server Error');
            return;
        }

        connection.query('SELECT * FROM events', function (error, results, fields) {
            if (error) {
                console.error('Error executing query:', error);
                res.status(500).send('Internal Server Error');
                return;
            }

            res.json(results);
            connection.end();
        });
    });
});

// The "catchall" handler: for any request that doesn't match one above, send back React's index.html file.
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname + '/client/build/index.html'));
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Node is running on port ${PORT}`);
});