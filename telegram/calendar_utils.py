from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import calendar

# Generate inline keyboard for calendar
def create_calendar(year, month):
    cal = calendar.Calendar()
    month_days = cal.monthdayscalendar(year, month)

    keyboard = []
    # Add week days header
    keyboard.append([
        InlineKeyboardButton("Mon", callback_data="ignore"),
        InlineKeyboardButton("Tue", callback_data="ignore"),
        InlineKeyboardButton("Wed", callback_data="ignore"),
        InlineKeyboardButton("Thu", callback_data="ignore"),
        InlineKeyboardButton("Fri", callback_data="ignore"),
        InlineKeyboardButton("Sat", callback_data="ignore"),
        InlineKeyboardButton("Sun", callback_data="ignore")
    ])

    # Add day buttons
    for week in month_days:
        week_buttons = []
        for day in week:
            if day == 0:
                week_buttons.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                week_buttons.append(InlineKeyboardButton(str(day), callback_data=f"day_{day}_{month}_{year}"))
        keyboard.append(week_buttons)

    # Add navigation buttons
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    keyboard.append([
        InlineKeyboardButton("<", callback_data=f"prev_month_{prev_month}_{prev_year}"),
        InlineKeyboardButton(">", callback_data=f"next_month_{next_month}_{next_year}")
    ])

    return InlineKeyboardMarkup(keyboard)
