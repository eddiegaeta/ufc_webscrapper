# Requirements:
# pip3 install requests beautifulsoup4
# pip3 install mysql-connector-python
# pip3 install python-dotenv
# pip3 install python-dateutil

import requests
from bs4 import BeautifulSoup
import json
import datetime
from dotenv import load_dotenv
import os
import mysql.connector
from dateutil import parser
from dateutil.tz import gettz
import logging
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/scraper.log') if os.path.exists('/var/log') else logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()  # take environment variables from .env.

# Convert now to a timezone-aware datetime
now = datetime.datetime.now(gettz("America/New_York"))

# Database integration
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT") or "3306")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Validate required environment variables
required_vars = ["DB_HOST", "DB_USER", "DB_PASS", "DB_NAME"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

logger.info(f"Connecting to database at {DB_HOST}:{DB_PORT}")

# Configure requests session with retry strategy
def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    return session

session = create_session()

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )
    logger.info("Database connection established successfully")
except mysql.connector.Error as err:
    logger.error(f"Database connection failed: {err}")
    raise

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Function to create the database table if it doesn't exist
def create_table():
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
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
            )
        ''')
        conn.commit()
        logger.info("Database table verified/created successfully")
    except mysql.connector.Error as err:
        logger.error(f"Error creating table: {err}")
        raise

# Function to insert event data into the database
def insert_event(event_title, event_date, event_url, event_type, event_all_fighters, event_venue, event_location):
    try:
        event_fights_json = json.dumps(event_all_fighters)  # Serialize the list to JSON
        query = '''
            INSERT INTO events (event_title, event_date, event_url, event_type, event_all_fighters, event_venue, event_location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            event_title = VALUES(event_title),
            event_date = VALUES(event_date),
            event_type = VALUES(event_type),
            event_all_fighters = VALUES(event_all_fighters),
            event_venue = VALUES(event_venue),
            event_location = VALUES(event_location)
        '''
        data = (event_title, event_date, event_url, event_type, event_fights_json, event_venue, event_location)
        cursor.execute(query, data)
        conn.commit()
        logger.debug(f"Event inserted/updated: {event_title}")
    except mysql.connector.Error as err:
        logger.error(f"Error inserting event '{event_title}': {err}")
        raise

# Function to query the database and return only upcoming events
def query_database(limit=8):
    cursor.execute('SELECT * FROM events')
    rows = cursor.fetchall()
    upcoming_events = []
    for row in rows:
        event_date_str = row[1].strip()  # Event date is in row[1]
        try:
            # Parse with timezone info for both EST and EDT
            event_date = parser.parse(event_date_str, tzinfos={
                "EDT": gettz("America/New_York"),
                "EST": gettz("America/New_York")
            })
            # If parsing resulted in a naive datetime, make it aware
            if event_date.tzinfo is None:
                event_date = event_date.replace(tzinfo=gettz("America/New_York"))
        except (ValueError, TypeError):
            continue  # Skip rows with invalid date formats

        if event_date >= now:
            event = {
                "event_title": row[0],
                "event_date": row[1],
                "event_url": row[2],
                "event_type": row[3],
                "event_all_fighters": row[4],
                "event_venue": row[5],
                "event_location": row[6],
            }
            upcoming_events.append(event)

    # Sort the events by date
    upcoming_events.sort(key=lambda x: parser.parse(x["event_date"], tzinfos={
        "EDT": gettz("America/New_York"),
        "EST": gettz("America/New_York")
    }))
    
    return upcoming_events[:limit]

# Main script execution
if __name__ == "__main__":
    logger.info("Starting UFC event scraper...")
    start_time = time.time()
    
    try:
        # Create the table if it doesn't exist (don't drop it)
        create_table()

        # URL of the website you want to scrape
        url = 'https://www.ufc.com/events'
        logger.info(f"Fetching events from {url}")
        
        # Send a GET request to the website
        response = session.get(url, timeout=30)
        response.raise_for_status()
        logger.info(f"Successfully fetched events page (status: {response.status_code})")
        
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the elements containing article titles
        article_titles = soup.find_all('h3', class_='c-card-event--result__headline')
        # Find the elements containing event dates
        event_dates = soup.find_all('div', class_='c-card-event--result__date')
        # Venue information
        venue_elements = soup.find_all('div', class_='field--name-taxonomy-term-title')
        # Venue Location
        venue_locations = soup.find_all('div', class_='field--name-location')
        
        logger.info(f"Found {len(article_titles)} events on the page")

        # Get subURL fighter information
        def all_fights(url):
            try:
                time.sleep(0.5)  # Rate limiting - be nice to the server
                page = session.get(url, timeout=30)
                page.raise_for_status()
                soup = BeautifulSoup(page.content, "html.parser")              
                fighter_divs = soup.find_all('div', class_='c-listing-fight__names-row')
                fight_roster = []  # Create an empty list to store fighter names

                for fighter_href in fighter_divs:
                    try:
                        red_fighter = fighter_href.find('div', class_='c-listing-fight__corner-name c-listing-fight__corner-name--red')
                        blue_fighter = fighter_href.find('div', class_='c-listing-fight__corner-name c-listing-fight__corner-name--blue')
                        
                        # Check if fighter elements and their links exist
                        if red_fighter and red_fighter.a and blue_fighter and blue_fighter.a:
                            fighter1 = ((red_fighter.a['href']).replace("https://www.ufc.com/athlete/","")).replace("-","_")
                            fighter2 = ((blue_fighter.a['href']).replace("https://www.ufc.com/athlete/","")).replace("-","_")            
                            fighter_vs_fighter = fighter1 + " vs " + fighter2
                            fight_roster.append(fighter_vs_fighter)  # Append each fighter name to the list
                    except (AttributeError, KeyError, TypeError) as e:
                        logger.warning(f"Error parsing fighter in {url}: {e}")
                        continue
                        
                logger.debug(f"Found {len(fight_roster)} fights for event {url}")
                return fight_roster
            except requests.RequestException as e:
                logger.error(f"Error fetching fighter data from {url}: {e}")
                return []

        # Loop through the article titles, event dates, and venue elements
        event_count = 0
        events_inserted = 0
        events_failed = 0
        
        for title, date, venue_element, venue_location in zip(article_titles, event_dates, venue_elements, venue_locations):
            if event_count >= 8:
                break

            try:
                event_title = title.a.text  # Extract the text of the <a> tag within <h3>
                event_date = (date.a.text.replace("/ Main Card","")).replace("/",",")    # Extract the text of the <a> tag within <div>
                event_url = title.a['href'] # Extract the "href" attribute from the <a> tag
                full_event_url = 'https://www.ufc.com' + event_url  # Construct the full URL
                event_type = (event_url.split("/")[2]).replace("-","_")[:15]
                
                logger.info(f"Processing event {event_count + 1}: {event_title}")
                event_all_fighters = all_fights(full_event_url)

                venue_h5 = venue_element.find('h5')
                event_venue = venue_h5.text.strip() if venue_h5 is not None else "N/A"
                
                event_location = venue_location.find('span').text.strip() if venue_location.find('span') else "N/A"

                logger.info(f"  Date: {event_date}, Venue: {event_venue}, Location: {event_location}")
                logger.info(f"  Fighters: {len(event_all_fighters)} fights")
                
                insert_event(event_title, event_date, event_url, event_type, event_all_fighters, event_venue, event_location)
                events_inserted += 1
                event_count += 1
                
            except Exception as e:
                logger.error(f"Error processing event: {e}", exc_info=True)
                events_failed += 1
                continue
        
        elapsed_time = time.time() - start_time
        logger.info(f"Scraping completed in {elapsed_time:.2f} seconds")
        logger.info(f"Events processed: {events_inserted} successful, {events_failed} failed")
        
        # Query the database to verify data
        logger.info("Querying database for upcoming events...")
        upcoming_events = query_database(limit=8)
        logger.info(f"Found {len(upcoming_events)} upcoming events in database")

    except Exception as e:
        logger.error(f"Fatal error in scraper: {e}", exc_info=True)
        raise
    finally:
        # Close the database connection
        if conn.is_connected():
            cursor.close()
            conn.close()
            logger.info("Database connection closed")