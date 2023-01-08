import telebot
import time
from telebot import types
from date_parser import DateParser
from date_parser import check_date
from team_parser import TeamParser
from team_parser import check_team

TOKEN = ""

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup_start_choice = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)  # задали формат кнопок
    search_by_date_button = types.KeyboardButton("Пошук за датою")
    search_by_team_button = types.KeyboardButton("Пошук за командою")
    help = types.KeyboardButton("Допомога")
    markup_start_choice.add(search_by_date_button, search_by_team_button, help)  # добавили кнопки

    bot.send_message(
        message.chat.id,
        "Привіт! \nЦе бот для пошуку футбольних матчів. \nНатисни кнопку щоб почати...",
        reply_markup=markup_start_choice)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id,
        "Щоб почати використання боту введіть команду '/start';"
        "\nЯкщо виникли проблеми — перезапустіть бот і натисніть '/start';"
        "\nЩоб переглянути всі можливості боту введіть '/all_commands'.",
    )

@bot.message_handler(commands=['help'])
def end(message):
    bot.send_message(
        message.chat.id,
        "Пошук завершено успішно!"
        "\nЯкщо бажаєте продовжити пошук —"
        "\n— натисніть відповідну кнопку. "
        "\nАбо скористайтеся командами: "
        "\n'/search_by_date' та '/search_by_team'.",
    )


@bot.message_handler(commands=['all_commands'])
def all_commands(message):
    bot.send_message(
        message.chat.id,
        "Перелік всіх команд: "
        "\n/start — перезапуск боту; "
        "\n/help — інструкція використання; "
        "\n/all_commands — перелік можливих команд; "
        "\n/search_by_date — пошук матчів за датою;"
        "\n/search_by_team — пошук інформації за командою;"
    )


@bot.message_handler(commands=['search_by_date'])
def search_by_date_com(message):
    bot.send_message(
        message.chat.id,
        "Введіть дату у форматі: дд.мм.рррр")
    bot.register_next_step_handler(message, send_matches_by_date)


def send_matches_by_date(message):
    msg = message.text
    msg = msg.split('.')
    if not check_date(msg):
        bot.send_message(
            message.chat.id,
            "Некоректний ввід. Почніть пошук ще раз"
        )
        return
    msg.reverse()
    date = '-'.join(msg)
    parser = DateParser(date)
    if not parser.leagues:
        bot.send_message(
            message.chat.id,
            "Матчів на цю дату немає. Почніть пошук ще раз"
        )
    else:
        for i in parser.messages:
            bot.send_message(
                message.chat.id,
                i,
                parse_mode="Markdown"
            )
            time.sleep(0.1)
    end(message)

@bot.message_handler(commands=['search_by_team'])
def search_by_team_com(message):
    bot.send_message(
        message.chat.id,
        "Введіть назву футбольної команди:")
    bot.register_next_step_handler(message, search_by_team)


def search_by_team(message):
    msg = message.text
    if not check_team(msg):
        bot.send_message(
            message.chat.id,
            text="Такої команди немає. Почніть пошук ще раз"
        )
        return
    parser = TeamParser(msg)
    for match in parser.calendar:
        bot.send_message(
            message.chat.id,
            text=match
        )
    for stat in parser.stats:
        bot.send_message(
            message.chat.id,
            text=stat
        )
    for news in parser.news:
        bot.send_message(
            message.chat.id,
            text=news
        )
    end(message)

@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == "Пошук за датою":
        search_by_date_com(message)
    elif message.text == "Пошук за командою":
        search_by_team_com(message)
    elif message.text == "Допомога":
        help(message)


bot.polling(none_stop=True)
