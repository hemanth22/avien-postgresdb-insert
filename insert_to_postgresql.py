import psycopg2 
from datetime import datetime
import os
import requests
import pytz

postgres_hostname = os.environ.get('postgres_hostname')
postgres_database = os.environ.get('postgres_database')
postgres_port = os.environ.get('postgres_port')
postgres_username = os.environ.get('postgres_username')
postgres_password = os.environ.get('postgres_password')
bot_token = os.environ.get('Priyoid_bot')

def telegram_send_message(message):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id=-1002266504611&text={}".format(bot_token, message)
    requests.get(url)

def insert_remainder_message():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(database=postgres_database, user=postgres_username, password=postgres_password, host=postgres_hostname, port=postgres_port)
        cursor = connection.cursor()

        # Insert the specified message
        insert_query = """
        INSERT INTO remainder_messages (message_date, message) VALUES (TO_DATE('06-01-2025', 'DD-MM-YYYY'), 'Ensure to close the CR Approvals and Sign-off Submissions before 11:00 AM');
        """
        cursor.execute(insert_query)
        connection.commit()
        print(f"Message inserted successfully: {insert_query}")
        return f"Message inserted successfully: {insert_query}"
    except (Exception, psycopg2.Error) as error:
        print(f"Error while inserting into PostgreSQL: {error}")
        return f"Error while inserting into PostgreSQL: {error}"

    finally:
        # Close the database connection
        if connection:
            cursor.close()
            connection.close()

# Usage example
if __name__ == "__main__":
    # Insert the specific remainder message
    message = insert_remainder_message()
    # Specify the date in YYYY-MM-DD format
    ist_timezone = pytz.timezone("Asia/Kolkata")
    # Create a datetime object
    current_date = datetime.now(ist_timezone)
    # Format it to YYYY-MM-DD
    formatted_date = current_date.strftime("%Y-%m-%d")
    print(f"Formatted Date: {formatted_date}")
    date_to_query = formatted_date
    
    # Send messages to Telegram
    for new_sendMessage_tele in message.split("\n"):
        telegram_send_message(new_sendMessage_tele)
    print(f"Message for {date_to_query}: {message}")
