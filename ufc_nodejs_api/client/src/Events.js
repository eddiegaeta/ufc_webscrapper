import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Events.css';

function Events() {
    const [events, setEvents] = useState([]);
    const [filteredEvents, setFilteredEvents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchEvents();
    }, []);

    useEffect(() => {
        if (searchTerm) {
            const filtered = events.filter(event => 
                event.event_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                event.event_location.toLowerCase().includes(searchTerm.toLowerCase()) ||
                event.event_venue.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setFilteredEvents(filtered);
        } else {
            setFilteredEvents(events);
        }
    }, [searchTerm, events]);

    const fetchEvents = async () => {
        try {
            const response = await axios.get('/api/events');
            const eventsData = response.data.events || response.data;
            setEvents(eventsData);
            setFilteredEvents(eventsData);
            setLoading(false);
        } catch (error) {
            console.error('Error fetching events:', error);
            setError('Failed to load events. Please try again later.');
            setLoading(false);
        }
    };

    const getTimeUntilEvent = (eventDateStr) => {
        try {
            // Parse the event date string
            const eventDate = new Date(eventDateStr);
            const now = new Date();
            const diff = eventDate - now;

            if (diff < 0) return 'Event passed';

            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

            if (days > 0) {
                return `${days} day${days > 1 ? 's' : ''} ${hours} hour${hours > 1 ? 's' : ''}`;
            } else if (hours > 0) {
                return `${hours} hour${hours > 1 ? 's' : ''}`;
            } else {
                return 'Starting soon!';
            }
        } catch {
            return '';
        }
    };

    if (loading) {
        return (
            <div className="events-container">
                <div className="loading-spinner">
                    <h2>Loading UFC Events...</h2>
                    <div className="spinner"></div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="events-container">
                <div className="error-message">
                    <h2>⚠️ {error}</h2>
                    <button onClick={fetchEvents}>Retry</button>
                </div>
            </div>
        );
    }

    return (
        <div className="events-container">
            <header className="events-header">
                <h1>🥊 UFC Upcoming Events</h1>
                <div className="search-bar">
                    <input
                        type="text"
                        placeholder="Search by title, location, or venue..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <p className="event-count">{filteredEvents.length} upcoming event{filteredEvents.length !== 1 ? 's' : ''}</p>
            </header>

            {filteredEvents.length === 0 ? (
                <div className="no-events">
                    <p>No events found matching your search.</p>
                </div>
            ) : (
                <div className="events-grid">
                    {filteredEvents.map((event, index) => {
                        const fighters = event.event_all_fighters ? 
                            (typeof event.event_all_fighters === 'string' ? 
                                JSON.parse(event.event_all_fighters) : 
                                event.event_all_fighters) : 
                            [];

                        return (
                            <div key={index} className="event-card">
                                <div className="event-header">
                                    <h2>{event.event_title}</h2>
                                    <span className="event-type">{event.event_type?.replace(/_/g, ' ').toUpperCase()}</span>
                                </div>
                                
                                <div className="event-details">
                                    <div className="detail-item">
                                        <span className="icon">📅</span>
                                        <span>{event.event_date}</span>
                                    </div>
                                    
                                    <div className="detail-item countdown">
                                        <span className="icon">⏰</span>
                                        <span className="countdown-text">{getTimeUntilEvent(event.event_date)}</span>
                                    </div>

                                    <div className="detail-item">
                                        <span className="icon">🏟️</span>
                                        <span>{event.event_venue}</span>
                                    </div>

                                    <div className="detail-item">
                                        <span className="icon">📍</span>
                                        <span>{event.event_location}</span>
                                    </div>
                                </div>

                                {fighters.length > 0 && (
                                    <div className="fights-section">
                                        <h3>Fight Card ({fighters.length} fights)</h3>
                                        <ul className="fights-list">
                                            {fighters.map((fighter, idx) => (
                                                <li key={idx} className="fight-item">
                                                    <span className="fight-number">{idx + 1}</span>
                                                    <span className="fighters">{fighter.replace(/_/g, ' ')}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}

                                <a 
                                    href={`https://ufc.com${event.event_url}`} 
                                    target="_blank" 
                                    rel="noopener noreferrer"
                                    className="event-link"
                                >
                                    View Event Details →
                                </a>
                            </div>
                        );
                    })}
                </div>
            )}
        </div>
    );
}

export default Events;