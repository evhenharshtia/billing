import telebot
import random
from found import get_date_telnet
from found import get_date_user
from found import get_date_account
from found import format_mac

import logging
logging.basicConfig(filename="sample.log", level=logging.INFO)
 
logging.debug("This is a debug message")
logging.info("Informational message")
logging.error("An error has happened!")


bot = telebot.TeleBot('Your TOKEN')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row("user","olt")
keyboard1.row("/start","/help")


keyboard_choice = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_choice.row("mac","port")
keyboard_choice.row("/start")

keyboard_user = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_user.row("login","licevoy")
keyboard_user.row("/start")


keyboard_start = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_start.row("/start")

keyboard_olt = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_olt.row("192.168.10.87","192.168.10.88" ,"192.168.10.89")
keyboard_olt.row("192.168.10.90","192.168.10.91" ,"192.168.10.92")
keyboard_olt.row("192.168.10.93","192.168.10.94" ,"192.168.10.95")
keyboard_olt.row("192.168.10.96","192.168.10.97" ,"/start")

keyboard_comm = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_comm.row("mac_onu_list", "signal_from_onu" )
keyboard_comm.row("signal_from_olt","/start")

@bot.message_handler(commands=['start'])
def start_message(message):
    #bot.send_message(message.chat.id, "Привет. С чем будем работать?", reply_markup=markup)
    bot.send_message(message.chat.id, "Привіт, {0.first_name}!\nЯ - <b>{1.first_name}</b>. З чого почнемо роботу.".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=keyboard1)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Для отримання данних по абоненту, в головному меню натисніть<b> USER</b>,\r\n та введіть номер <b>особового рахунку</b>.\r\nДля пошуку інформаціх по ONU, виберіть в меню <b>OLT</b>.\r\nДалі ІР OLT-a, і ідентифікатор для пошуку. ".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=keyboard_start)



@bot.message_handler(content_types=["text"])
def send_text(message):
    try:
        #bot.send_message(message.chat.id, message.text)
        
        if message.text.lower() == 'user':
            numb = message.text
            bot.send_message(message.chat.id, 'По чому шукатимемо?',reply_markup=keyboard_user)
            bot.register_next_step_handler(message, select_ident)
            #bot.send_message(message.chat.id, 'Для отримання данних потрібно знати номер особового рахунку')
            #bot.register_next_step_handler(message, get_user)
        elif message.text.lower() == 'olt':
            bot.send_message(message.chat.id, 'Виберіть ОЛТ для роботи', reply_markup=keyboard_olt)
            bot.register_next_step_handler(message, get_date_olt)
        else:
            #bot.send_message(message.chat.id, 'Введений mac не знайдено: ' + mac,  reply_markup=keyboard_start)
            bot.send_message(message.chat.id, "Ви ввели невідому команду", reply_markup=keyboard_start)
    except Exception as e:
        print(repr(e))
@bot.message_handler(content_types=["text"])

def get_date_olt(message):
    global ip
    ip = message.text
    if ip == '/start':
        bot.send_message(message.chat.id, 'Головне меню',  reply_markup=keyboard_start)
    else:
        bot.send_message(message.chat.id, 'Виберіть ідентифікатор для пошуку данних на ' +ip, reply_markup=keyboard_choice)
        bot.register_next_step_handler(message, choice)

@bot.message_handler(content_types=["text"])
def choice(message):
    try:
        choice = message.text
        bot.send_message(message.chat.id, choice)
        if choice == 'mac':
            print (choice)
            bot.send_message(message.chat.id, 'Введіть мак ОНУ')
            bot.register_next_step_handler(message, fdb)
        elif choice == 'port':
            print (choice)
            bot.send_message(message.chat.id, 'Введіть номер порта')
            bot.register_next_step_handler(message, select_command)
        else:
            bot.register_next_step_handler(message, start_message)
    except Exception as e:
        print(repr(e))

def select_command(message):
    global port_id
    port_id = ''
    port_id = message.text
    bot.send_message(message.chat.id, 'Що бажаєте подивитися по '+port_id+' на OLT ' +ip+'?', reply_markup=keyboard_comm)
    bot.register_next_step_handler(message, data_onu)

# def select_selector(message):
#      global port_id
#      port_id = ''
#      port_id = message.text
#      bot.send_message(message.chat.id, 'Що бажаєте подивитися по '+port_id+' на OLT ' +ip+'?', reply_markup=keyboard_comm)
#      bot.register_next_step_handler(message, select_selector)

def select_ident(message):
    global ident
    ident = ''
    ident = message.text
    if ident == 'login':
        bot.send_message(message.chat.id, 'Введіть логін', reply_markup=keyboard_user)
        bot.register_next_step_handler(message, user_data)
    elif ident == 'licevoy':
        bot.send_message(message.chat.id, 'Введіть номер рахунку', reply_markup=keyboard_user)
        bot.register_next_step_handler(message, account_data)
    else:
        bot.send_message(message.chat.id, 'Ви ввели невідомий ідентифікатор. Поверніться в головне меню, і спробуйте знову', reply_markup=keyboard_start)

def fdb(message):

    mac = ''
    mac = message.text
    if len(mac) == 17:
        mac =  format_mac(mac)
        command = 'show epon active-onu mac-address '
        fdb = get_date_telnet(mac,ip,command)
        bot.send_message(message.chat.id, fdb, reply_markup=keyboard_start)
    else:
        bot.send_message(message.chat.id, 'Введені данні не є MAC адресою', reply_markup=keyboard_start)

def data_onu(message):
    try:
        global command
        command = message.text
        if command == 'mac_onu_list':
            command = 'show mac address-table interface epon '
            fdb = get_date_telnet(port_id,ip,command)
            bot.send_message(message.chat.id, fdb)
        elif command == 'signal_from_onu':
            command = 'show epon optical-transceiver-diagnosis interface epon '
            fdb = get_date_telnet(port_id,ip,command)
            bot.send_message(message.chat.id, fdb, reply_markup=keyboard_start)
        elif command == 'signal_from_olt':
            command = 'show epon interface epoN ' 
            port_id_ = port_id+' onu ctc optical-transceiver-diagnosis '
            fdb = get_date_telnet(port_id_,ip,command)
            bot.send_message(message.chat.id, fdb, reply_markup=keyboard_start)
        else:
            command = 'show system mtu'
            fdb = get_date_telnet(port_id,ip,command)
            bot.send_message(message.chat.id, fdb, reply_markup=keyboard_start)
    
    except Exception as e:
        print(repr(e))

def account_data(message):
    accnumber = ''
    accnumber = message.text
    if accnumber.isdigit():
        if len(accnumber) == 5:
            user_data = get_date_account(accnumber)
            bot.send_message(message.chat.id, user_data, reply_markup=keyboard_start)
        else:
            bot.send_message(message.chat.id, 'Введені данні не є номером рахунку', reply_markup=keyboard_start)
    else:
        bot.send_message(message.chat.id, 'Введені данні не є номером рахунку', reply_markup=keyboard_start)

def user_data(message):
    username = ''
    username = message.text
    user_data = get_date_user(username)
    bot.send_message(message.chat.id, user_data, parse_mode='html', reply_markup=keyboard_start)
    #bot.send_message(message.chat.id, 'Введені данні не є номером рахунку', reply_markup=keyboard_start)
    

if __name__ == '__main__':
     bot.polling(none_stop=True)
#bot.polling(none_stop=True, interval=0)

