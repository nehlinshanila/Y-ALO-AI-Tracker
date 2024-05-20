from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers import start_command, handle_callback, handle_message, error_handler
from config import TOKEN  # Import the token from config.py

def main():
    app = Application.builder().token(TOKEN).read_timeout(20).write_timeout(20).build()

    # Command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', handle_message))
    app.add_handler(CommandHandler('custom', handle_message))

    # Message handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Callback query handler
    app.add_handler(CallbackQueryHandler(handle_callback))

    # Error handler
    app.add_error_handler(error_handler)

    # Polls the bot
    print('Bot is polling...')
    app.run_polling()

if __name__ == '__main__':
    main()
