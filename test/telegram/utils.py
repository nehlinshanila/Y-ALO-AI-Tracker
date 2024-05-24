# utils.py
import logging
logger = logging.getLogger(__name__)
import datetime
import firebase_admin
from firebase_admin import credentials, db
from config import FIREBASE_KEY_PATH, FIREBASE_DB_URL
import matplotlib.pyplot as plt

# Initialize Firebase Admin
cred = credentials.Certificate(FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred, {
    'databaseURL': FIREBASE_DB_URL
})

# Validate date function
def validate_date(date_text: str) -> bool:
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Firebase user data functions
def get_user_data(user_id):
    try:
        ref = db.reference(f'/users/{user_id}')
        data = ref.get()
        if data:
            logger.info(f"Data retrieved for user {user_id}")
            return data
        else:
            logger.info(f"No data found for user {user_id}")
            return {'cycles': []}
    except Exception as e:
        logger.error(f"Failed to retrieve data for user {user_id}: {str(e)}")
        return {'cycles': []}

def update_user_data(user_id, data):
    try:
        ref = db.reference(f'/users/{user_id}')
        ref.set(data)
        logger.info(f"Data successfully saved for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to save data for user {user_id}: {str(e)}")

def plot_cycles(cycles):
    dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in cycles]
    intervals = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]

    plt.figure(figsize=(10, 5))
    plt.plot(dates[1:], intervals, marker='o', linestyle='-')
    plt.xlabel('Date')
    plt.ylabel('Cycle Length (days)')
    plt.title('Menstrual Cycle Length Over Time')
    plt.grid(True)
    plt_path = 'cycles.png'
    plt.savefig(plt_path)
    plt.close()

    # When using the file, ensure it is appropriately opened and closed
    with open(plt_path, 'rb') as file:
        # Use the file, e.g., sending it via Telegram API
        pass
