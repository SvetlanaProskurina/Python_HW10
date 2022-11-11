from re import I
from telebot import types
import telebot.types
from telebot import TeleBot
from time import time 
from datetime import datetime   
import logging

bot = TeleBot('5750665963:AAEJP12QWonHXi0asBFMTZjlv4cLB8ezipM')
# конфигурирование формата сообщения в лог файле
logging.basicConfig(filename='logg.txt', filemode='a', format='%(asctime)s %(levelname)s %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


# логирование
def do_log(msg: telebot.types.Message):
    with open('logg.txt' , 'a') as f_log:
        print(datetime.now(), f'Пользователь ({msg.from_user.id}) прислал сообщение: {msg.text}', file=f_log)


def find_sign_simple(txt):
   return ''.join([char for char in "+-/*" if char in txt])   

def simple_func(msgs):
    res = 0
    try:    
        if len(find_sign_simple(msgs)) == 1:
            if find_sign_simple(msgs) == "-":
                lst = msgs.split("-")
                res = float(lst[0]) - float(lst[1])
                return str(res)
                
            if find_sign_simple(msgs) == "+":
                lst = msgs.split("+")
                res = float(lst[0]) + float(lst[1])
                return str(res)
                
            if find_sign_simple(msgs) == "*":
                lst = msgs.split("*")
                res = float(lst[0]) * float(lst[1])
                return str(res)
            
            if find_sign_simple(msgs) == "/":
                lst = msgs.split("/")
                if float(lst[1]) != 0.0:
                    res = float(lst[0]) / float(lst[1])
                    return str(res)
                else:
                    logging.error(f'Делить на ноль нельзя')
                    return 'Делить на ноль нельзя'
    except:
        logging.error(f'Неправильный ввод чисел, возможно введены буквы или лишние знаки')
        return 'Введите числа и знак между ними'   
    
    logging.info(f'Результат вычисления = {res}')


def complex_func(msg):
    txt = msg
    res = None
    lst = txt.split()
    try:
        if lst[1] == '-':
            res = complex(lst[0]) - complex(lst[2])
            logging.info(f'Результат вычисления комплексных чисел = {res}')
            return str(res)
        elif lst[1] == '+':
            res = complex(lst[0]) + complex(lst[2])
            logging.info(f'Результат вычисления комплексных чисел = {res}')
            return str(res)
        elif lst[1] == '/':
            res = complex(lst[0]) / complex(lst[2])
            logging.info(f'Результат вычисления комплексных чисел = {res}')
            return str(res)
        elif lst[1] == '*':
            res = complex(lst[0]) * complex(lst[2])
            logging.info(f'Результат вычисления комплексных чисел = {res}')
            return str(res)           
        else:
            res = 'Неверный ввод'
            return res
    except:
        logging.error(f'Ошибка ввода комплексных чисел')
        return 'Ошибка ввода комплексных чисел'

@bot.message_handler(commands=['log'])
def log_com(msg: telebot.types.Message):
    logging.info(f'Пользователь запросил лог файл')
    bot.send_document(chat_id=msg.from_user.id, document=open('logg.txt', 'rb'))

@bot.message_handler(commands=['start'])
def send_start_message(msg: telebot.types.Message):
    do_log(msg)
    bot.send_message(msg.chat.id, f'Привет,{msg.from_user.first_name}! Это бот калькулятор. Выберите действие:\n'
                                                      'Вычисление простых чисел /simple \n'
                                                      'Вычисление комплексных чисел /complex \n'
                                                      'Загрузить лог файл /log \n')

@bot.message_handler(commands=['simple'])
def simple_com(msg: telebot.types.Message):
    do_log(msg)
    bot.send_message(chat_id=msg.from_user.id, text= 'Введите два числа и действие между ними, например: 15 - 8')
    bot.register_next_step_handler(callback=simple_calc, message=msg)

def simple_calc(msg: telebot.types.Message):
        bot.send_message(chat_id=msg.from_user.id, text=simple_func(msg.text))
        

@bot.message_handler(commands=['complex'])
def complex_com(msg: telebot.types.Message):
    do_log(msg)
    bot.send_message(chat_id=msg.from_user.id, text= 'Введите два комплексных числа и действие между ними, например: 15+8j - 17+2j')
    bot.register_next_step_handler(callback=complex_calc, message=msg)

def complex_calc(msg: telebot.types.Message):
        bot.send_message(chat_id=msg.from_user.id, text=complex_func(msg.text))
        
bot.polling()