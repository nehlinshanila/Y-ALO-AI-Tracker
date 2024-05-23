import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import validate_date, get_user_data, update_user_data, plot_cycles
from calendar_utils import create_calendar
import datetime
import calendar

# Initialize logger for this module
logger = logging.getLogger(__name__)

# Start command handler
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🌸 Set Period Date 🌸", callback_data='set_period')],
        [InlineKeyboardButton("🌺 My Cycles 🌺", callback_data='my_cycles')],
        [InlineKeyboardButton("🌼 More Options 🌼", callback_data='more_options')]
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
    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    if data == 'set_period':
        year, month = datetime.datetime.now().year, datetime.datetime.now().month
        reply_markup = create_calendar(year, month)
        await query.message.edit_text(f'🌸 {calendar.month_name[month]} {year} 🌸\nPlease select the date to log your period:', reply_markup=reply_markup)
    elif data == 'get_advice':
        await query.message.edit_text('🌸 You can ask for health advice here. Please type your question. 🌸')
    elif data == 'my_cycles':
        if len(user_data.get('cycles', [])) < 5:
            await query.message.edit_text('🌺 You need to input at least 5 cycles to view the charts. 🌺\nWould you like to input your period dates now?', reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Yes", callback_data='set_period')],
                [InlineKeyboardButton("No", callback_data='cancel')]
            ]))
        else:
            plot_cycles(user_data['cycles'])
            await query.message.reply_photo(photo=open('cycles.png', 'rb'), caption='🌺 Here are your cycle charts. 🌺')
    elif data == 'more_options':
        await query.message.edit_text('🌼 Explore additional options and settings. 🌼')
    elif data.startswith("day_"):
        _, day, month, year = data.split("_")
        date_logged = datetime.datetime(int(year), int(month), int(day)).strftime('%Y-%m-%d')
        user_data.setdefault('cycles', []).append(date_logged)
        update_user_data(user_id, user_data)
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

# Message handler for textual messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)

    if validate_date(text):
        date = datetime.datetime.strptime(text, '%Y-%m-%d')
        user_data.setdefault('cycles', []).append(date.strftime('%Y-%m-%d'))
        update_user_data(user_id, user_data)
        if len(user_data.get('cycles', [])) >= 5:
            await update.message.reply_text("🌸 You have inputted 5 cycles. You can now view your cycle charts. 🌸")
        else:
            await update.message.reply_text("🌸 Period date logged. Please input more dates. 🌸")
    else:
        await update.message.reply_text("🌸 Please enter a valid date in YYYY-MM-DD format. 🌸")

# Error handler for catching errors
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')
