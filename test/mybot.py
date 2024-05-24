from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN: Final = '7023708802:AAEwGyDpcL4Uvgb9QGK_H5YQUn11L0KuZSc'
BOT_USERNAME: Final = 'YAlo_tracker_bot'

# COMMANDS
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Define the text in both languages
    welcome_text_en = "Hello, Welcome to the Y-Alo period tracker app! Please choose your language to continue."
    welcome_text_bn = "Y-Alo পিরিয়ড ট্র্যাকার অ্যাপে আপনাকে স্বাগতম! চালিয়ে যেতে আপনার ভাষা চয়ন করুন."
    combined_text = f"{welcome_text_en}\n\n{welcome_text_bn}"
    
    # Create inline buttons for language selection
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='lang_en'),
            InlineKeyboardButton("বাংলা", callback_data='lang_bn')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the welcome message with buttons
    await update.message.reply_text(combined_text, reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query
    
    if query.data == 'lang_en':
        await query.edit_message_text("You have selected English. How can I assist you today?")
    elif query.data == 'lang_bn':
        await query.edit_message_text("আপনি বাংলা নির্বাচন করেছেন। আমি কীভাবে আপনাকে সাহায্য করতে পারি?")
    
    # Here you can set the user's language preference in context.user_data or a database

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))

    # Callback handler for inline buttons
    app.add_handler(CallbackQueryHandler(button_callback))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Bot is polling...')
    app.run_polling()
