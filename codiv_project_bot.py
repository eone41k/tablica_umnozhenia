import telebot
from telebot.types import CallbackQuery, InlineKeyboardButton as IB, ReplyKeyboardMarkup, InlineKeyboardMarkup
import random

bot= telebot.TeleBot('8392810308:AAHBe9Y2Y69dDpF_IrfW-tDzh1J8GOw3cqY')

class UserSession:
    def __init__(self):
        self.score = 0
        self.total = 0
        self.current_question = None
        self.current_answer = None
        self.difficult = 10

user_data={}



@bot.message_handler(['start'])
def start(msg):
    user_id=msg.from_user.id
    if user_id not in user_data:
        user_data[msg.from_user.id]=UserSession()
    kb = ReplyKeyboardMarkup()
    kb.row("🎯начать треннировку🎯")
    kb.row("сложность")
    kb.row("статистика")
    kb.row("помощь")
    bot.send_message(msg.from_user.id,'Привет, я умножайка! Давай поучим таблицу умножения!'
                     , reply_markup=kb)


@bot.message_handler(func=lambda message: message.text == 'помощь')
def help(msg):
    '''информация о программе плюс командах'''
    user_id = msg.from_user.id
    if user_id not in user_data:
        user_data[msg.from_user.id] = UserSession()
    bot.send_message(msg.from_user.id, 'основные комманды бота:'
                                       '\n🎯начать треннировку🎯 - начать игру '
                                       '\nсложность- выбор сложности'
                                       '\nстатистика - посмотреть статистику'
                                       '\nпомощь - рукаводство к боту')

@bot.message_handler(func=lambda message: message.text == 'статистика')
def stats(msg):
    '''вывод статистики'''
    user_id = msg.from_user.id
    if user_id not in user_data:
        user_data[msg.from_user.id] = UserSession()
    user = user_data[user_id]
    if user.total==0:
        bot.send_message(msg.from_user.id, 'у вас еще нет статистики, начните треннировку')
    else:
        bot.send_message(msg.from_user.id, f'правильных ответов: {user.score}'
                                       f'\nвсего ответов: {user.total}'
                                       f'\nуровень сложности: {user.difficult}'
                                       f'\nпроцент правильных ответов: {(user.score/user.total)*100}%')

@bot.message_handler(func=lambda message: message.text == 'сложность')
def choice_difficult(msg):
    '''выбор сложности
    легко-1, 5
    средне-1, 10
    сложно-1, 15'''
    user_id = msg.from_user.id
    if user_id not in user_data:
        user_data[msg.from_user.id] = UserSession()

    kb=InlineKeyboardMarkup()
    kb.add(IB('Легко(1-5)', callback_data='diff_5'))
    kb.add(IB('Средне(1-10)', callback_data='diff_10'))
    kb.add(IB('Трудно(1-15)', callback_data='diff_15'))
    bot.send_message(msg.from_user.id,'выберите уровень сложности', reply_markup=kb)

@bot.callback_query_handler(func=lambda call: call.data.startswith('diff_'))
def set_difficult(call: CallbackQuery):
    user_id = call.message.chat.id
    if user_id not in user_data:
        user_data[user_id] = UserSession()
    a=call.data.split('_')
    user_data[user_id].difficult=int(a[1])
    bot.answer_callback_query(call.id)
    bot.edit_message_text(f'сложность:1-{a[1]}', user_id, call.message.message_id)




@bot.message_handler(func=lambda message: message.text =='🎯начать треннировку🎯')
def training(msg):
    user_id=msg.from_user.id
    if user_id not in user_data:
        user_data[msg.from_user.id]=UserSession()
    send_question(user_id)
def send_question(user_id):
    kb = ReplyKeyboardMarkup()
    kb.row("стоп")
    kb.row("статистика")

    user=user_data[user_id]
    num1=random.randint(1, user.difficult)
    num2=random.randint(1, user.difficult)
    user.current_question=f'сколько будет: {num1}*{num2}?'
    user.current_answer = num1*num2
    bot.send_message(user_id,user.current_question, reply_markup=kb)

@bot.message_handler(func=lambda message: message.text =='стоп')
def stop_training(msg):
    bot.send_message(msg.from_user.id, 'треннеровка остановлена')
    start(msg)


@bot.message_handler(func=lambda message: True)
def check_answer(msg):
    user_id = msg.chat.id
    if user_id not in user_data or user_data[user_id].current_answer is None:
        return

    try:
        user_answer= int(msg.text)
        user_data[user_id].total+=1
        if user_answer == user_data[user_id].current_answer:
            user_data[user_id].score+=1
            bot.send_message(user_id, 'правильно!')
        else:
            bot.send_message(user_id, f'не правильно, правильный ответ: {user_data[user_id].current_answer}')
        send_question(user_id)
    except ValueError:
        bot.send_message(user_id, 'введите число')




bot.infinity_polling()