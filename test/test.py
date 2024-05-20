# from typing import Final
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
# import datetime
# import calendar

# TOKEN: Final = '--token'  # Replace with your actual Telegram bot token

# # ============================
# # COMMAND HANDLERS
# # ============================

# # Start command handler
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     keyboard = [
#         [InlineKeyboardButton("🌸 Set Period Date 🌸", callback_data='set_period')],
#         [InlineKeyboardButton("🌸 Get Advice 🌸", callback_data='get_advice')]
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     await update.message.reply_text(
#         "🌸 স্বাগতম! এটি আপনার মাসিক চক্র ট্র্যাক করার জন্য একটি নিরাপদ স্থান। 🌸\n\nPlease choose an option:",
#         reply_markup=reply_markup
#     )

# # Generate inline keyboard for calendar
# def create_calendar(year, month):
#     cal = calendar.Calendar()
#     month_days = cal.monthdayscalendar(year, month)

#     keyboard = []
#     # Add week days header
#     keyboard.append([
#         InlineKeyboardButton("Mon", callback_data="ignore"),
#         InlineKeyboardButton("Tue", callback_data="ignore"),
#         InlineKeyboardButton("Wed", callback_data="ignore"),
#         InlineKeyboardButton("Thu", callback_data="ignore"),
#         InlineKeyboardButton("Fri", callback_data="ignore"),
#         InlineKeyboardButton("Sat", callback_data="ignore"),
#         InlineKeyboardButton("Sun", callback_data="ignore")
#     ])

#     # Add day buttons
#     for week in month_days:
#         week_buttons = []
#         for day in week:
#             if day == 0:
#                 week_buttons.append(InlineKeyboardButton(" ", callback_data="ignore"))
#             else:
#                 week_buttons.append(InlineKeyboardButton(str(day), callback_data=f"day_{day}_{month}_{year}"))
#         keyboard.append(week_buttons)

#     # Add navigation buttons
#     keyboard.append([
#         InlineKeyboardButton("<", callback_data=f"prev_month_{month}_{year}"),
#         InlineKeyboardButton(">", callback_data=f"next_month_{month}_{year}")
#     ])

#     return InlineKeyboardMarkup(keyboard)

# # Callback query handler
# async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     await query.answer()
#     data = query.data

#     if data == 'set_period':
#         year, month = datetime.datetime.now().year, datetime.datetime.now().month
#         reply_markup = create_calendar(year, month)
#         await query.message.edit_text('🌸 Please select the date to log your period: 🌸', reply_markup=reply_markup)
#     elif data == 'get_advice':
#         await query.message.edit_text('🌸 You can ask for health advice here. Please type your question. 🌸')
#     elif data.startswith("day_"):
#         day, month, year = map(int, data.split("_")[1:])
#         date_logged = datetime.datetime(year, month, day).strftime('%Y-%m-%d')
#         await query.message.edit_text(f"🌸 Period date logged: {date_logged} 🌸")
#     elif data.startswith("prev_month_") or data.startswith("next_month_"):
#         _, month, year = map(int, data.split("_")[2:])
#         if "prev_month" in data:
#             month -= 1
#             if month == 0:
#                 month = 12
#                 year -= 1
#         elif "next_month" in data:
#             month += 1
#             if month == 13:
#                 month = 1
#                 year += 1
#         reply_markup = create_calendar(year, month)
#         await query.message.edit_text('🌸 Please select the date to log your period: 🌸', reply_markup=reply_markup)

# # Message handler
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
#     if validate_date(text):
#         date = datetime.datetime.strptime(text, '%Y-%m-%d')
#         next_period_date = date + datetime.timedelta(days=28)  # assuming a 28-day cycle
#         response = f"🌸 Your next period is expected around {next_period_date.strftime('%Y-%m-%d')}. 🌸"
#     else:
#         response = "🌸 Please enter a valid date in YYYY-MM-DD format. 🌸"
#     await update.message.reply_text(response)

# # ============================
# # UTILITY FUNCTIONS
# # ============================

# # Validate date function
# def validate_date(date_text: str) -> bool:
#     try:
#         datetime.datetime.strptime(date_text, '%Y-%m-%d')
#         return True
#     except ValueError:
#         return False

# # Error handler
# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f'Update {update} caused error {context.error}')

# # ============================
# # MAIN APPLICATION SETUP
# # ============================

# if __name__ == '__main__':
#     app = Application.builder().token(TOKEN).read_timeout(20).write_timeout(20).build()

#     # Command handlers
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('help', handle_message))
#     app.add_handler(CommandHandler('custom', handle_message))

#     # Message handlers
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

#     # Callback query handler
#     app.add_handler(CallbackQueryHandler(handle_callback))

#     # Error handler
#     app.add_error_handler(error)

#     # Polls the bot
#     print('Bot is polling...')
#     app.run_polling()
