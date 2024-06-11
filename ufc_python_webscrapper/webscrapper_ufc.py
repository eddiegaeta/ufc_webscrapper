import requests
from bs4 import BeautifulSoup
import json
import datetime
from dotenv import load_dotenv
import os
import mysql.connector
import moment

# Load environment variables from .env file
load_dotenv()

# Print environment variables for debugging
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASS:", os.getenv("DB_PASS"))
print("DB_NAME:", os.getenv("DB_NAME"))

# Get current time
now = datetime.datetime.now()

# Get environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Connect to the MySQL database
conn = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASS,
    database=DB_NAME
)

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Function to create the database table if it doesn't exist
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_title VARCHAR(255),
            event_date VARCHAR(255),
            event_url VARCHAR(255) PRIMARY KEY,
            event_type VARCHAR(15),
            event_all_fighters VARCHAR(1024),
            event_venue VARCHAR(255),
            event_location VARCHAR(255)
        )
    ''')

# Function to insert event data into the database
def insert_event(event_title, event_date, event_url, event_type, event_all_fighters, event_venue, event_location):
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

# Function to query the database and get upcoming events
def query_database(limit=8):
    now = moment.now().tz("America/New_York").format("ddd, MMM D , h:mm A z")
    query = '''
        SELECT * FROM events 
        WHERE STR_TO_DATE(event_date, "%a, %b %e , %l:%i %p %Z ") >= STR_TO_DATE(%s, "%a, %b %e , %l:%i %p %Z ")
        ORDER BY STR_TO_DATE(event_date, "%a, %b %e , %l:%i %p %Z ")
        LIMIT %s
    '''
    cursor.execute(query, (now, limit))
    rows = cursor.fetchall()
    for row in rows:
        print("Event Title:", row[0])
        print("Event Date:", row[1])
        print("Event URL:", row[2])
        print("Event Type:", row[3])
        print("Event Fighter Roster:", row[4])
        print("-" * 40)
    return rows

if __name__ == "__main__":
    # Drop and recreate the table to ensure it matches your code's structure
    cursor.execute("DROP TABLE IF EXISTS events")
    create_table()  # Create the table if it doesn't exist

    # URL of the website you want to scrape
    url = 'https://www.ufc.com/events'
    # Send a GET request to the website
    response = requests.get(url)
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

    # Get subURL fighter information
    def all_fights(url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")              
        fighter_divs = soup.find_all('div', class_='c-listing-fight__names-row')
        fight_roster = []  # Create an empty list to store fighter names

        for fighter_href in fighter_divs:
            red_fighter = fighter_href.find('div', class_='c-listing-fight__corner-name c-listing-fight__corner-name--red')
            blue_fighter = fighter_href.find('div', class_='c-listing-fight__corner-name c-listing-fight__corner-name--blue')    
            fighter1 = ((red_fighter.a['href']).replace("https://www.ufc.com/athlete/","")).replace("-","_")
            fighter2 = ((blue_fighter.a['href']).replace("https://www.ufc.com/athlete/","")).replace("-","_")            
            fighter_vs_fighter = fighter1 + " vs " + fighter2
            fight_roster.append(fighter_vs_fighter)  # Append each fighter name to the list
        return(fight_roster)

    # Loop through the article titles, event dates, and venue elements
    for title, date, venue_element, venue_location in zip(article_titles, event_dates, venue_elements, venue_locations):
        event_title = title.a.text  # Extract the text of the <a> tag within <h3>
        event_date = (date.a.text.replace("/ Main Card","")).replace("/",",")    # Extract the text of the <a> tag within <div>
        event_url = title.a['href'] # Extract the "href" attribute from the <a> tag
        full_event_url = 'https://www.ufc.com' + event_url  # Construct the full URL
        event_type = (event_url.split("/")[2]).replace("-","_")[:15]
        event_all_fighters = all_fights(full_event_url)
        event_main_card = event_all_fighters[0].replace("_"," ").title()
        
        venue_h5 = venue_element.find('h5')
        event_venue = venue_h5.text.strip() if venue_h5 is not None else "N/A"
        
        event_location = venue_location.find('span class')

        print(f"Event Title: {event_title}")
        print(f"Event MainCard: {event_main_card}")
        print(f"Event Date: {event_date}")
        print(f"Event URL: {full_event_url}")
        print(f"Event Type: {event_type}")
        print(f"Event AllFights: {event_all_fighters}")
        print(f"Event Venue: {event_venue}")
        print(f"Event Location: {event_location}")
        print("-" * 40)
        
        insert_event(event_title, event_date, event_url, event_type, event_all_fighters, event_venue, event_location)
    
    # Query the database to verify data (optional)
    upcoming_events = query_database(limit=8)
    print(upcoming_events)
    
    # Close the database connection
    conn.close()
