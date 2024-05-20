# from typing import Final
# from telegram import Update
# from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# TOKEN: Final = '--token'
# BOT_USERNAME: Final = 'Y_Alo_Bot'

# # COMMANDS
# async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("স্বাগতম! এটি আপনার মাসিক চক্র ট্র্যাক করার জন্য একটি নিরাপদ স্থান।")
    
# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("মাসিক সেট করা: আপনার শেষ কয়েকটি মাসিকের তারিখ প্রবেশ করুন। একবার সেট করা হলে, অ্যালগরিদম স্বয়ংক্রিয়ভাবে আপনার চক্র ট্র্যাক করবে। ভয়েস ইনপুট: আপনি বাংলায় ভয়েস ইনপুট ব্যবহার করে তারিখ দিতে পারেন। নোটিফিকেশন: আপনি আপনার আগাম মাসিক, উর্বর সময় এবং অন্যান্য স্বাস্থ্য তথ্য সম্পর্কে নোটিফিকেশন পাবেন। পরামর্শ: কোনো সমস্যার সম্মুখীন হলে, আমাদের অ্যাপের মাধ্যমে ডাক্তারের পরামর্শ নিতে পারেন।")
    
# async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("নোটিফিকেশন পছন্দ: আপনি আপনার পছন্দ অনুযায়ী নোটিফিকেশন সেট করতে পারেন। এসএমএস বা ইন-অ্যাপ নোটিফিকেশন। ডেটা ব্যাকআপ: আপনার মাসিক চক্রের ডেটা স্বয়ংক্রিয়ভাবে ব্যাকআপ করা হবে, যাতে আপনি সহজেই এটি পুনরুদ্ধার করতে পারেন। অ্যাপ থিম: আপনার পছন্দ অনুযায়ী অ্যাপ থিম পরিবর্তন করুন। অ্যাকাউন্ট সেটিংস: আপনার প্রোফাইল এবং স্বাস্থ্য তথ্য আপডেট করতে পারেন।")
    
# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text: str = update.message.text
#     response: str = handle_response(text)
#     await update.message.reply_text(response)
# # RESPONSES 

# def handle_response(text: str) -> str:
#     if 'মাসিক সেট' in text:
#         return 'মাসিকের তারিখ প্রবেশ করুন।'
#     if 'নোটিফিকেশন' in text:
#         return 'নোটিফিকেশন সেট করতে পারেন।'
#     if 'ভয়েস ইনপুট' in text:
#         return 'আপনি বাংলায় ভয়েস ইনপুট ব্যবহার করতে পারেন।'
#     if 'পরামর্শ' in text:
#         return 'আমাদের অ্যাপের মাধ্যমে ডাক্তারের পরামর্শ নিতে পারেন।'
#     return "I did not understand that."

# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f'Update {update} caused error {context.error}')
        
# if __name__ == '__main__':
#     app = Application.builder().token(TOKEN).build()

#     # Commands
#     app.add_handler(CommandHandler('start', start_command))
#     app.add_handler(CommandHandler('help', help_command))
#     app.add_handler(CommandHandler('custom', custom_command))

#     # Messages
#     app.add_handler(MessageHandler(filters.TEXT, handle_message))

#     # Errors
#     app.add_error_handler(error)

#     # Polls the bot
#     print('Bot is polling...')
#     app.run_polling()