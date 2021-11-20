import telebot # import применяется для того, чтобы сделать код в одном модуле доступным для работы в другом
import requests#Библиотека Requests дает вам возможность посылать HTTP/1.1-запросы, используя Python.
from telebot import types



bot=telebot.TeleBot('1688513164:AAEShtdW3XayQ0TN5jWr7CqLr3dm85F0Clo')

headers = {
    'x-rapidapi-key': "502d93af37mshb810b0fbd2d32eep142068jsn728a7939f616",
    'x-rapidapi-host': "fixer-fixer-currency-v1.p.rapidapi.com"
    }
@bot.message_handler(commands=['help'])
def help(message):
	# keyboard = telebot.types.ReplyKeyboardMarkup()
	# btn_random = telebot.types.KeyboardButton('How random works?')
	# btn_definition = telebot.types.KeyboardButton('How definition works?')
	# btn_show = telebot.types.KeyboardButton('How show works?')
	# keyboard.add(btn_random, btn_definition, btn_show)
	# bot.send_message(message.chat.id, "Please, choose an option", reply_markup=keyboard)

	keyboard = telebot.types.InlineKeyboardMarkup()
	btn_exchange = telebot.types.InlineKeyboardButton('exchange как работает?', callback_data='exchange')
	btn_calculator = telebot.types.InlineKeyboardButton('calculator как работает?', callback_data='calculator')
	keyboard.add(btn_exchange, btn_calculator)
	bot.send_message(message.chat.id, "Please, choose an option", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			if call.data == 'exchange':
				bot.send_message(call.message.chat.id, 'Эта команда позволяет вам перевести доллары в тенге ')
			elif call.data == 'calculator':
				bot.send_message(call.message.chat.id, 'Эта команд делает вычисления')
	except Exception as e:
		print(repr(e))


@bot.message_handler(commands=['calculator'])
def send_welcome(message):
    print(message)
    # убрать клавиатуру Telegram полностью
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Привет " + message.from_user.first_name + ", Я калькулятор \nВведите число", reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)

# введите первое число
def process_num1_step(message, user_result = None):
    try:
       global user_num1

       # запоминаем число
       if user_result == None:
          user_num1 = int(message.text)
       else:
          # если был передан результат ранее
          # пишем в первое число, не спрашивая
          user_num1 = str(user_result)

       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
       itembtn1 = types.KeyboardButton('+')
       itembtn2 = types.KeyboardButton('-')
       itembtn3 = types.KeyboardButton('*')
       itembtn4 = types.KeyboardButton('/')
       markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

       msg = bot.send_message(message.chat.id, "Выберите операцию", reply_markup=markup)
       bot.register_next_step_handler(msg, process_proc_step)
    except Exception as e:
       bot.reply_to(message, 'Это не число или что то пошло не так...')

# выберите операцию +, -, *, /
def process_proc_step(message):
    try:
       global user_proc

       # запоминаем операцию
       user_proc = message.text
       # убрать клавиатуру Telegram полностью
       markup = types.ReplyKeyboardRemove(selective=False)

       msg = bot.send_message(message.chat.id, "Введите еще число", reply_markup=markup)
       bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
       bot.reply_to(message, 'Вы ввели что то другое или что то пошло не так...')

# введите второе число
def process_num2_step(message):
    try:
       global user_num2

       # запоминаем число
       user_num2 = int(message.text)

       markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
       itembtn1 = types.KeyboardButton('Результат')
       itembtn2 = types.KeyboardButton('Продолжить вычисление')
       markup.add(itembtn1, itembtn2)

       msg = bot.send_message(message.chat.id, "Показать результат или продолжить операцию?", reply_markup=markup)
       bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
       bot.reply_to(message, 'Это не число или что то пошло не так...')

# показать результат или продолжить операцию
def process_alternative_step(message):
    try:
       # сделать вычисление
       calc()

       # убрать клавиатуру Telegram полностью
       markup = types.ReplyKeyboardRemove(selective=False)

       if message.text.lower() == 'результат':
          bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
       elif message.text.lower() == 'продолжить вычисление':
          # перейти на шаг, где спрашиваем оператор
          # передаем результат, как первое число
          process_num1_step(message, user_result)

    except Exception as e:
       bot.reply_to(message, 'Что то пошло не так...')

# Вывод результата пользователю
def calcResultPrint():
    global user_num1, user_num2, user_proc, user_result
    return "Результат: " + str(user_num1) + ' ' + user_proc + ' ' + str(user_num2) + ' = ' + str( user_result )

# Вычисление
def calc():
    global user_num1, user_num2, user_proc, user_result

    user_result = eval(str(user_num1) + user_proc + str(user_num2))

    return user_result

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
	print(message)
	if message.chat.type in ['user', 'group', 'supergroup']:
		bot.send_message(message.chat.id, f'Hello, {message.from_user.first_name}!')


@bot.message_handler(content_types=['left_chat_members'])
def goodbye(message):
	print(message)
	if message.chat.type in ['user','group', 'supergroup']:
		bot.send_message(message.chat.id, f'Goodbye, {message.from_user.first_name}!')
@bot.message_handler(commands=['start'])
def start(message):
	print(message)
	bot.send_message(message.chat.id, 'Hello, {}'.format(message.from_user.first_name))
#@bot.message_handler(commands=['usd'])
#def USD(message):
	#msg = bot.send_message(message.chat.id, 'Пожалуйста введите число')
	#bot.register_next_step_handler(msg, ask_word_for_usd)


#def ask_word_for_usd(message):
#   amount = message.text.lower()ddddddddddddddd
#   url = "https://fixer-fixer-currency-v1.p.rapidapi.com/convert"
#   querystring={"amount": {amount}, "to": "KZT", "from": "USD"}
#   response = requests.request("GET", url, headers=headers, params=querystring)
#   data=response.json()
#   result=data['result']
#   bot.send_message(message.chat.id,result)
#@bot.message_handler(commands=['rub'])
#def RUB(message):
	#msg = bot.send_message(message.chat.id, 'Пожалуйста введите число')
	#bot.register_next_step_handler(msg, ask_word_for_rub)

@bot.message_handler(content_types=['text'])
def exchange (message):
    if message.text == '/exchange':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('₽', '$')
        msg = bot.send_message(message.chat.id, 'Выберите валюту', reply_markup=markup)
        bot.register_next_step_handler(msg, currency)

def currency(message):
    if message.text == '₽':
        msg = bot.send_message(message.chat.id, 'Введите сумму в рублях')
        bot.register_next_step_handler(msg, rub)
    if message.text == '$':
            msg = bot.send_message(message.chat.id, 'Введите сумму в долларах')
            bot.register_next_step_handler(msg, usd)
def rub(message):
    amount = message.text.lower()
    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/convert"
    querystring={"amount": {amount}, "to": "KZT", "from": "RUB"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data=response.json()
    result=data['result']
    bot.send_message(message.chat.id,result)
def usd(message):
    amount = message.text.lower()
    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/convert"
    querystring={"amount": {amount}, "to": "KZT", "from": "USD"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    data=response.json()
    result=data['result']
    bot.send_message(message.chat.id,result)
bot.polling(none_stop=True)
# def ask_word_for_rub(message):
# amount = message.text.lower()
# url = "https://fixer-fixer-currency-v1.p.rapidapi.com/convert"
# querystring={"amount": {amount}, "to": "KZT", "from": "RUB"}
# response = requests.request("GET", url, headers=headers, params=querystring)
# data=response.json()
# result=data['result']
# bot.send_message(message.chat.id,result)

#Алгоритм:
#1 Создать 4 переменные:
  #Первое число, операция, второе число, результат
#2 Создать функцию которая делает вычисления
#3 Запросить у пользователя первое число, операцию, второе число
#4 Сделать вычисления, в зависимости от выбора пользователя,
  #показать результат или продолжить вычисление
#5 оператор "+" приходит строкой, он ни во что не преобразовывается,
  #ведь это оператор. А 3 "+" 2 операция не выполнима, выдаст ошибку.
  #В таком случае используется функция eval(), в которую передаем строку,
  #'3 + 2' и операция выполняется верно.
#6 Зациклить вычисление, то есть если выбрал "Результат" - показать результат,
  #если выбрал "Продолжить вычисление", передать результат вычисления, как первое число.





