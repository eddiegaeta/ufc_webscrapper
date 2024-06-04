// Install dependencies: 
// npm i express
// npm run serve
// npm i nodemon -D
// npm i nodemon -g
// npm run dev
// npm i mysql
// npm install dotenv --save
// npm install ejs --save

const express = require('express');
const app = express();
const mysql = require('mysql2');
const ejs = require('ejs');
require('dotenv').config();

app.set('view engine', 'ejs');

app.get('/events', (req, res) => {
    const connection = mysql.createConnection({
        host: process.env.DB_HOST,
        user: process.env.DB_USER,
        password: process.env.DB_PASS,
        database: process.env.DB_NAME
    });

    connection.connect();

    connection.query('SELECT * FROM events', function (error, results, fields) {
        if (error) {
            console.error('Error executing query:', error);
            res.status(500).send('Internal Server Error');
            return;
        }

        res.render('events', { events: results });
    });

    connection.end();
});

app.listen(3000, () => {
    console.log('Node is running on port 3000');
});
