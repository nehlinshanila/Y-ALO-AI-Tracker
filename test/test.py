import firebase_admin
from firebase_admin import credentials, firestore
from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta
import calendar

# Initialize Firebase with the service account key file
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)

# TOKEN: Final = '7023708802:AAEwGyDpcL4Uvgb9QGK_H5YQUn11L0KuZSc'
BOT_USERNAME: Final = 'YAlo_tracker_bot'

# Helper function to create a calendar
def create_calendar(year: int, month: int) -> InlineKeyboardMarkup:
    keyboard = []

    # First row - Month and Year
    keyboard.append([InlineKeyboardButton(f'{calendar.month_name[month]} {year}', callback_data='ignore')])

    # Second row - Weekdays
    days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    keyboard.append([InlineKeyboardButton(day, callback_data='ignore') for day in days_of_week])

    # Calendar rows
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(' ', callback_data='ignore'))
            else:
                row.append(InlineKeyboardButton(str(day), callback_data=f'select_date_{year}-{month:02d}-{day:02d}'))
        keyboard.append(row)

    # Last row - Navigation
    prev_month = month - 1 if month > 1 else 12
    next_month = month + 1 if month < 12 else 1
    prev_year = year if month > 1 else year - 1
    next_year = year if month < 12 else year + 1
    keyboard.append([
        InlineKeyboardButton('<', callback_data=f'change_month_{prev_year}_{prev_month}'),
        InlineKeyboardButton('>', callback_data=f'change_month_{next_year}_{next_month}')
    ])

    return InlineKeyboardMarkup(keyboard)

# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome_message(update)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome_message(update)

async def send_welcome_message(update: Update):
    welcome_text_en = "Hello, Welcome to the Y-Alo period tracker app! Please choose your language to continue."
    welcome_text_bn = "Y-Alo পিরিয়ড ট্র্যাকার অ্যাপে আপনাকে স্বাগতম! চালিয়ে যেতে আপনার ভাষা চয়ন করুন।"
    combined_text = f"{welcome_text_en}\n\n{welcome_text_bn}"
    
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='lang_en'),
            InlineKeyboardButton("বাংলা", callback_data='lang_bn')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(combined_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query
    
    if query.data == 'lang_en':
        await send_english_options(query)
    elif query.data == 'lang_bn':
        await query.edit_message_text("আপনি বাংলা নির্বাচন করেছেন। আমি কীভাবে আপনাকে সাহায্য করতে পারি?")
    elif query.data == 'track_period':
        await send_date_picker(query)
    elif query.data == 'book_appointment':
        await book_appointment(query)
    elif 'book_dr_' in query.data:
        doctor_name = query.data.split('book_dr_')[1]
        await handle_doctor_selection(query, doctor_name)
    elif 'change_month_' in query.data:
        await change_month(query)
    elif 'select_date_' in query.data:
        selected_date = query.data.split('select_date_')[1]
        await log_selected_date(query, selected_date)

async def send_english_options(query):
    text = "Thank you for using Y-Alo tracker. Please let us know what we may help you with today."
    keyboard = [
        [
            InlineKeyboardButton("Track my period date", callback_data='track_period'),
        ],
        [
            InlineKeyboardButton("Book an appointment", callback_data='book_appointment'),
        ],
        [
            InlineKeyboardButton("Give me advice", callback_data='give_advice'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def send_date_picker(query):
    today = datetime.now()
    await query.edit_message_text('Please select the date to log your period:', reply_markup=create_calendar(today.year, today.month))

async def change_month(query):
    # Splitting the query data
    parts = query.data.split('_')
    if len(parts) == 3:  # Ensure there are exactly three parts
        _, year, month = parts
        # Convert year and month to integers
        year = int(year)
        month = int(month)
        # Calculate previous month
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        # Create calendar for previous month
        await query.edit_message_text('Please select the date to log your period:', reply_markup=create_calendar(prev_year, prev_month))
    else:
        print("Invalid query data format")

async def log_selected_date(query, selected_date):
    # Parse the selected date
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    
    # Calculate the next period date by adding 28 days
    next_period_date = selected_date_obj + timedelta(days=28)
    next_period_date_str = next_period_date.strftime('%Y-%m-%d')

    # Send message indicating the last period date is logged
    text = f"Your last period date is now logged in: {selected_date}"
    await query.edit_message_text(text)

    # Store the last period date in Firebase
    user_id = query.from_user.id  # Assuming each user has a unique Telegram ID
    await store_period_date_in_firebase(user_id, selected_date)

    # Calculate and send message indicating the next period date
    next_period_text = f"Your next period date is estimated to be on: {next_period_date_str}"
    await query.message.reply_text(next_period_text)

async def store_period_date_in_firebase(user_id, period_date):
    db = firestore.client()
    doc_ref = db.collection('users').document(str(user_id))
    doc_ref.update({
        'last_period_date': period_date
    })

async def book_appointment(query: Update):
    await query.edit_message_text("Please choose your preferred gynaecologist:",
                                  reply_markup=create_doctor_menu())

def create_doctor_menu():
    keyboard = [
        [InlineKeyboardButton("Dr. Ayesha Begum", callback_data='book_dr_ayesha')],
        [InlineKeyboardButton("Dr. Humayra Akter", callback_data='book_dr_humayra')],
        [InlineKeyboardButton("Dr. Safina Karim", callback_data='book_dr_safina')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def handle_doctor_selection(query: Update, doctor_name: str):
    await query.edit_message_text(f"Your appointment with {doctor_name} has been successfully booked!")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')        

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Handle all text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback handler for inline buttons
    app.add_handler(CallbackQueryHandler(button_callback))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Bot is polling...')
    app.run_polling()

