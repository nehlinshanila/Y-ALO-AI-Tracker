from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import validate_date
from calendar_utils import create_calendar
import datetime
import calendar

# Start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌸 Set Period Date 🌸", callback_data='set_period')],
        [InlineKeyboardButton("🌸 Get Advice 🌸", callback_data='get_advice')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🌸 স্বাগতম! এটি আপনার মাসিক চক্র ট্র্যাক করার জন্য একটি নিরাপদ স্থান। 🌸\n\nPlease choose an option:",
        reply_markup=reply_markup
    )

# Callback query handler
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'set_period':
        year, month = datetime.datetime.now().year, datetime.datetime.now().month
        reply_markup = create_calendar(year, month)
        await query.message.edit_text(f'🌸 {calendar.month_name[month]} {year} 🌸\nPlease select the date to log your period:', reply_markup=reply_markup)
    elif data == 'get_advice':
        await query.message.edit_text('🌸 You can ask for health advice here. Please type your question. 🌸')
    elif data.startswith("day_"):
        _, day, month, year = data.split("_")
        date_logged = datetime.datetime(int(year), int(month), int(day)).strftime('%Y-%m-%d')
        await query.message.edit_text(f"🌸 Period date logged: {date_logged} 🌸")
    elif data.startswith("prev_month_") or data.startswith("next_month_"):
        _, direction, month, year = data.split("_")
        year, month = int(year), int(month)
        if direction == 'prev':
            month -= 1
            if month == 0:
                month = 12
                year -= 1
        elif direction == 'next':
            month += 1
            if month == 13:
                month = 1
                year += 1
        reply_markup = create_calendar(year, month)
        await query.message.edit_text(f'🌸 {calendar.month_name[month]} {year} 🌸\nPlease select the date to log your period:', reply_markup=reply_markup)

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if validate_date(text):
        date = datetime.datetime.strptime(text, '%Y-%m-%d')
        next_period_date = date + datetime.timedelta(days=28)  # assuming a 28-day cycle
        response = f"🌸 Your next period is expected around {next_period_date.strftime('%Y-%m-%d')}. 🌸"
    else:
        response = "🌸 Please enter a valid date in YYYY-MM-DD format. 🌸"
    await update.message.reply_text(response)

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')
