import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
bot = telebot.TeleBot("6324084068:AAHb4_u-2hPPA78wDfvh8WFTg4yLE-nDBYY",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Выбери время года"
text_button_1 = "Зима"
text_button_2 = "Весна"
text_button_3 = "Лето"


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Как дела? Готов читать стихи?',
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Отлично! *Как тебя* _зовут_?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'А сколько тебе [лет](https://ru.pinterest.com/)?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'Спасибо, что ответил на вопросы! А теперь выбери время года, о котором хочешь прочитать стих.', reply_markup=menu_keyboard)
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Однажды скучным серым днём земля покрылась серебром.\nВот так на радость детворе зима приходит в декабре.", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Когда от весны удирала зима, такая вокруг началась кутерьма. \nИ столько на землю свалилось хлопот, Что утром, не выдержав, тронулся лёд.", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "До чего хорош денёк! Веет лёгкий ветерок. \nСолнца летнего лучи так приятно горячи!", reply_markup=menu_keyboard)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()

