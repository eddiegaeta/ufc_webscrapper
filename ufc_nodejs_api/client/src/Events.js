import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Events.css';

function Events() {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchEvents();
    }, []);

    const fetchEvents = async () => {
        try {
            const response = await axios.get('/api/events');
            console.log('Fetched events:', response.data);

            // Sort events by date
            const sortedEvents = response.data.sort((a, b) => {
                const dateA = new Date(a.event_date);
                const dateB = new Date(b.event_date);
                return dateA - dateB;
            });

            setEvents(sortedEvents);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching events:', error);
            setError('Error fetching events');
            setLoading(false);
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="events-container">
            <h1>UFC Fights - Upcoming</h1>
            <ul>
                {events.map(event => (
                    <li key={event.event_id}>
                        <h2>{event.event_title}</h2>
                        <p>Date: {event.event_date}</p>
                        <p>Event: <a href={`https://ufc.com${event.event_url}`}>{event.event_type}</a></p>
                        <p>Venue: {event.event_venue}</p>
                        <p>Location: {event.event_location}</p>
                        <p>All Fights:
                            <select>
                                {JSON.parse(event.event_all_fighters).map((fighter, index) => (
                                    <option key={index}>{fighter}</option>
                                ))}
                            </select>
                        </p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Events;