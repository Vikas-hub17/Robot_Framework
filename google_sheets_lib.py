import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
SHEET1 = os.getenv('SHEET1', 'Sheet1')
SHEET2 = os.getenv('SHEET2', 'Sheet2')

# PostgreSQL setup
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

# Configure logging
logging.basicConfig(filename='automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '15LziGkhsTY-GvGRAW-Q5OCXy7znuJhVJE8RZjKdltL8'

def get_service():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        return build('sheets', 'v4', credentials=credentials)
    except Exception as e:
        logging.error("Failed to initialize Google Sheets service: %s", e)
        raise

from datetime import datetime

def copy_sheet_data():
    service = get_service()
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID, range='Sheet1').execute()
        values = result.get('values', [])

        # Add timestamp as the first row
        timestamp = [f"Data copied on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]
        values.insert(0, timestamp)

        if values:
            service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range='Sheet2',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            logging.info("Data with timestamp copied successfully.")
        else:
            logging.warning("No data found in Sheet1.")
    except HttpError as err:
        logging.error("An error occurred: %s", err)

def insert_data_to_db(data):
    """Insert Google Sheets data into PostgreSQL database."""
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Insert each row into the table
        for row in data:
            # Ensure your INSERT query matches the number of columns in the row
            cursor.execute(
                "INSERT INTO sample (Name, Salesman, Item, Units) VALUES (%s, %s, %s,%s)",
                (row[0], row[1], row[2], row[3])
            )

        # Commit the transaction and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Data inserted into PostgreSQL database successfully.")
    except Exception as e:
        logging.error("Failed to insert data into PostgreSQL: %s", e)
