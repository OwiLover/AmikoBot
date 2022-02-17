from asyncio.windows_events import NULL
from cgitb import text
from datetime import datetime
import logging
from multiprocessing import context
import os
import logging
import types
from array import *
from pydoc import describe
from unicodedata import category
from venv import create
from numpy import NaN
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ReplyMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
import sqlite3
import datetime

con = sqlite3.connect('Amiko.db', check_same_thread=False)
cur=con.cursor()

reply_keyboard = [['/create', '/review'], ['/update']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
    
def start (bot, update):
    user_id = bot.message.from_user.id
    if (cur.execute("SELECT IdUser FROM Users WHERE IdUser=?",(user_id,)).fetchone() is None) :
        num=bot.message.from_user.username
        cur.execute("INSERT INTO Users (IdUser,Username) VALUES (?,?)",(str(user_id) , str(num))),
        con.commit()
    else:
        num=bot.message.from_user.username
        cur.execute("UPDATE Users SET Username=? WHERE IdUser=?", (num,user_id,))
        con.commit()


    bot.message.reply_text(f'Приветик, {bot.effective_user.first_name}, я трейд Бот Амико! Ты можешь создавать объявления или просматривать их, для этого нажми на соответствующую панель в меню, или напиши ручками "Создать" или "Просмотреть"', reply_markup=markup)

def review (bot, context: CallbackContext):
    reply_keyboards = [['Электроника 📱', 'Игрушки 🧸','Животные 🐶'], ['Другое 🤔']]
    markup = ReplyKeyboardMarkup(reply_keyboards, one_time_keyboard=False, resize_keyboard=False)
    bot.message.reply_text("Сперва выберите тэг, который Вас интересует", reply_markup=markup)
    return 1
    
    
def showRes(bot, context: CallbackContext):
    if (bot.message.text!='Электроника 📱' and bot.message.text!='Игрушки 🧸' and bot.message.text!='Животные 🐶' and bot.message.text!='Другое 🤔'):
        bot.message.reply_text('Ну нет, выбери уже существующие тэги!')
        return 1
    reply_keyboard = [['/create', '/review'], ['/update']]
    tag=bot.message.text
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
    user_id = bot.message.from_user.id
    for value in cur.execute("SELECT Name, PhotoId, Description,UserId, U.Username FROM Offers JOIN Users U on U.IdUser=Offers.UserId WHERE UserId != ? AND Tag=?", (user_id,tag,)) :
        # for value2 in cur.execute("SELECT Username FROM Users WHERE IdUser=?", (value[3],)) :

        bot.message.reply_photo(value[1], caption = value[0] +'\n' + '\n'+value[2] +'\n'+'\n'+"Создатель объявления: "+'@'+value[4])
    bot.message.reply_text("Перед Вами список всех доступных объявлений!",reply_markup=markup)
    return ConversationHandler.END

#  bot.message.reply_photo(value[1], caption = value[0] +'\n' + '\n'+value[2] +'\n' + '\n'+"Ссылка на создателя объявления: "+'@'+value2[0])       
def update(update, context: CallbackContext):
    user_id = update.message.from_user.id
    # for value in cur.execute("SELECT Name, PhotoId, Description FROM Offers WHERE UserId = ?", (user_id,)) :
    #     markupp = InlineKeyboardMarkup([[InlineKeyboardButton("Тыкни меня!",'https://vk.com/feed'),InlineKeyboardButton("И снова!!!",'https://vk.com/feed')]])
    #     update.message.reply_photo(value[1], caption = value[0] +'\n' + '\n'+value[2],reply_markup = markupp)
    update.message.reply_text(
        'Хорошо, давайте просмотрим все Ваши объявления! Выберите то, которое хотите отредактировать (Отправь цифру!)',
        reply_markup=ReplyKeyboardRemove(),
    )
    counter=1;
    for value in cur.execute("SELECT Name, PhotoId, Description FROM Offers WHERE UserId = ?", (user_id,)) :

        update.message.reply_text(f'{counter}. {value[0]}')
        counter=counter+1;
    return 1

def choosedOffer(bot, context: CallbackContext):
    user_id = bot.message.from_user.id
    user_message = bot.message.text
    if (user_message.isdigit()==False):
        bot.message.reply_text("Пожалуйста, введи цифру!")
        return 1
    counter=0;
    for value in cur.execute("SELECT * FROM Offers WHERE UserId = ?", (user_id,)) :
        counter=counter+1;
        if (counter>=int(user_message)) : 
            bot.message.reply_text("Такой Заказ Есть!")
            reply_keyboard = [['Название', 'Фото', 'Описание', 'Тэг'], ['Удалить Объявление'],['Назад']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
            bot.message.reply_photo(value[2], caption = value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5],reply_markup = markup)
            bot.message.reply_text("Выберите, что хотите поменять в заявке (Или удалить её)")
            cur.execute("DELETE FROM Buffer WHERE UserId=?",(user_id,))
            cur.execute("INSERT INTO Buffer (UserID, Name, PhotoId, Descr, DateTime, Tag) VALUES(?,?,?,?,?,?)", (value[0],value[1],value[2],value[3],value[4],value[5]))
            con.commit();
            return 2
  
    bot.message.reply_text("Такого заказа нет, попробуйте снова!")
    return 1

def pathOffer(bot, context: CallbackContext):
    if (bot.message.text=="Название"):
        bot.message.reply_text("Отлично, напишите новое название!", reply_markup=ReplyKeyboardRemove())
        return 3
    if (bot.message.text=="Фото"):
        bot.message.reply_text("Прекрасно, пришлите новое фото!",reply_markup=ReplyKeyboardRemove(),)
        return 4
    if (bot.message.text=="Описание"):
        bot.message.reply_text("Хорошо, напишите новое описание!",reply_markup=ReplyKeyboardRemove(),)
        return 5
    if (bot.message.text=="Тэг"):
        reply_keyboards = [['Электроника 📱', 'Игрушки 🧸','Животные 🐶'], ['Другое 🤔']]
        markup = ReplyKeyboardMarkup(reply_keyboards, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text('Выберите новый тэг товара',reply_markup=markup)
        return 6
    if(bot.message.text=="Удалить Объявление"):
        reply_keyboards = [["Да","Нет"]]
        markup = ReplyKeyboardMarkup(reply_keyboards, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Вы уверены, что хотите удалить это объявление?",reply_markup=markup)
        return 7
    if(bot.message.text=="Назад"):
        reply_keyboard = [['/create', '/review'], ['/update']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Хорошо, теперь вы в главном меню!",reply_markup = markup)
        return ConversationHandler.END
        
        
    bot.message.reply_text("Эй, пользуйся специальной клавиатурой!")
    return 2
    
def nameUpdate(bot, context: CallbackContext):
    user_id=bot.message.from_user.id
    answer=bot.message.text
    for value in cur.execute("SELECT * FROM Offers WHERE UserId =?;", (user_id,)) :
        if (answer.lower()==value[1].lower()):
            bot.message.reply_text("У вас уже существует такой товар! Придумайте что-то другое")
            return 3
    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        cur.execute("UPDATE Offers SET Name=? WHERE UserId=? AND PhotoId=? AND Description=? AND DateTime=?", (answer,value[0],value[2],value[3],value[4]))
        con.commit();
        cur.execute("UPDATE Buffer SET Name=? WHERE UserId=?",(answer, value[0]))
        con.commit();
        
    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        reply_keyboard = [['Название', 'Фото', 'Описание', 'Тэг'], ['Удалить Объявление'],['Назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Имя обновлено! Желаете поменять что-нибудь ещё в этом объявлении?",reply_markup = markup)
        bot.message.reply_photo(value[2], caption = value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5])
        return 2

def photoUpdate(bot, context: CallbackContext):
    user_id=bot.message.from_user.id
    answer=bot.message.photo[0].file_id

    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        cur.execute("UPDATE Offers SET PhotoId=? WHERE UserId=? AND Name=? AND Description=? AND DateTime=?", (answer,value[0],value[1],value[3],value[4]))
        con.commit();
        cur.execute("UPDATE Buffer SET PhotoId=? WHERE UserId=?",(answer, user_id))
        con.commit();
    
    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) : 
        reply_keyboard = [['Название', 'Фото', 'Описание', 'Тэг'], ['Удалить Объявление'],['Назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Фото обновлено! Желаете поменять что-нибудь ещё в этом объявлении?",reply_markup = markup)
        bot.message.reply_photo(value[2], caption = value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5])
        return 2
    
def descrUpdate(bot, context: CallbackContext):
    user_id=bot.message.from_user.id
    answer=bot.message.text

    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        cur.execute("UPDATE Offers SET Description=? WHERE UserId=? AND PhotoId=? AND Name=? AND DateTime=?", (answer,value[0],value[2],value[1],value[4]))
        con.commit();
        cur.execute("UPDATE Buffer SET Descr=? WHERE UserId=?",(answer, value[0]))
        con.commit();
        
    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        reply_keyboard = [['Название', 'Фото', 'Описание', 'Тэг'], ['Удалить Объявление'],['Назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Описание обновлено! Желаете поменять что-нибудь ещё в этом объявлении?",reply_markup = markup)
        bot.message.reply_photo(value[2], caption = value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5])
        return 2
    
def tagUpdate(bot, context: CallbackContext):
    if (bot.message.text!='Электроника 📱' and bot.message.text!='Игрушки 🧸' and bot.message.text!='Животные 🐶' and bot.message.text!='Другое 🤔'):
        bot.message.reply_text('Ну нет, выбери уже существующие тэги!')
        return 6
    user_id=bot.message.from_user.id
    answer=bot.message.text
    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        cur.execute("UPDATE Offers SET Tag=? WHERE UserId=? AND PhotoId=? AND Name=? AND Description =? AND DateTime=?", (answer,value[0],value[2],value[1],value[3],value[4]))
        con.commit();
        cur.execute("UPDATE Buffer SET Tag=? WHERE UserId=?",(answer, value[0]))
        con.commit();
        
    for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
        reply_keyboard = [['Название', 'Фото', 'Описание', 'Тэг'], ['Удалить Объявление'],['Назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Тэг обновлён! Желаете поменять что-нибудь ещё в этом объявлении?",reply_markup = markup)
        bot.message.reply_photo(value[2], caption = value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[5])
        return 2

def deleteOffer(bot,context: CallbackContext):
    if (bot.message.text=="Да") :
        user_id=bot.message.from_user.id
        for value in cur.execute("SELECT * FROM Buffer WHERE UserId=?", (user_id,)) :
            cur.execute("DELETE FROM Offers WHERE UserId=? AND Name=? AND PhotoId=? AND Description=? AND DateTime=?",(value[0],value[1],value[2],value[3],value[4]))
            con.commit()
        cur.execute("DELETE FROM Buffer WHERE UserId=?", (user_id,))
        con.commit()
        reply_keyboard = [['/create', '/review'], ['/update']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Объявление удалено",reply_markup = markup)
        return ConversationHandler.END
    if (bot.message.text=="Нет") :
        reply_keyboard = [['Название', 'Фото', 'Описание', 'Тэг'], ['Удалить Объявление'],['Назад']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=False)
        bot.message.reply_text("Желаете поменять что-нибудь ещё в этом объявлении?",reply_markup = markup)
        return 2
    bot.message.reply_text("Пожалуйста, используйте специальную клавиатуру!")
    return 7
        
    
def create(update, context: CallbackContext):
    update.message.reply_text(
        'Хорошо, давайте создадим Ваше объявление! Для начала напишите название товара',
        reply_markup=ReplyKeyboardRemove(),
    )
    return 1

def naming(update, context: CallbackContext):
    user_id=update.message.from_user.id
    answer=update.message.text
    for value in cur.execute("SELECT * FROM Offers WHERE UserId =?;", (user_id,)) :
        if (answer.lower()==value[1].lower()):
            update.message.reply_text("Вы уже создавали этот товар! Придумайте что-то другое")
            return 1
    date = datetime.datetime.now()
    cur.execute("INSERT INTO Offers (UserId, Name,DateTime) VALUES(?,?,?)",(user_id, answer, date))
    update.message.reply_text(
        'Прекрасное название! Теперь отправьте фото Вашего товара',
    )
    return 2
def photo(bot, update):
    idPhoto=bot.message.photo[0].file_id
    user_id=bot.message.from_user.id
    cur.execute(f'UPDATE Offers SET PhotoId=? WHERE UserId=? AND DateTime=(SELECT MAX(DateTime) FROM Offers WHERE UserId=?)',(idPhoto, user_id, user_id))
    # bot.message.reply_photo(idPhoto)
    bot.message.reply_text(
        'Предложение почти создано, придумайте описание Вашего товара',
    ) 
    return 3

def rename(bot,update):
    bot.message.reply_text('Вы уже создавали этот товар! Придумайте что-то другое')
    return 1


    
def desc(bot, update):
    # определяем пользователя
    desc = bot.message.text
    user_id=bot.message.from_user.id
    cur.execute(f'UPDATE Offers SET Description=? WHERE UserId=? AND DateTime=(SELECT MAX(DateTime) FROM Offers WHERE UserId=?)',(desc, user_id, user_id))
    reply_keyboards = [['Электроника 📱', 'Игрушки 🧸','Животные 🐶'], ['Другое 🤔']]
    markup = ReplyKeyboardMarkup(reply_keyboards, one_time_keyboard=False, resize_keyboard=False)
    bot.message.reply_text('А теперь выберите тэг товара',reply_markup=markup)
    return 5

def tag(bot,update):
    if (bot.message.text!='Электроника 📱' and bot.message.text!='Игрушки 🧸' and bot.message.text!='Животные 🐶' and bot.message.text!='Другое 🤔'):
        bot.message.reply_text('Ну нет, выбери уже существующие тэги!')
        return 5
    tag=bot.message.text
    user_id=bot.message.from_user.id
    cur.execute(f'UPDATE Offers SET Tag=? WHERE UserId=? AND DateTime=(SELECT MAX(DateTime) FROM Offers WHERE UserId=?)',(tag, user_id, user_id))
    con.commit()
    bot.message.reply_text(f'Отлично, у Вас получилось вот такое объявление:', reply_markup=markup)
    for value in cur.execute("SELECT UserId, Name, PhotoId, Description, Tag FROM Offers WHERE UserId=? AND DateTime=(SELECT MAX(DateTime) FROM Offers WHERE UserId=?)",(user_id, user_id)) :
        print(value[1])
        bot.message.reply_photo(value[2], caption = value[1] +'\n' + '\n'+value[3] +'\n'+ '\n'+'Тэг: '+value[4])
    return ConversationHandler.END



def cancel (update, context: CallbackContext):
    update.message.reply_text(f'Как скажете, создание предложения отменено', reply_markup=markup)
    return ConversationHandler.END

conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('create', create)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        
        states={
           1: [MessageHandler(Filters.text, naming, pass_user_data=True)],
           2: [MessageHandler(Filters.photo, photo, pass_user_data=True)],
           3: [MessageHandler(Filters.text, desc, pass_user_data=True)],
           4: [MessageHandler(Filters.text, rename,pass_user_data=True)],
           5: [MessageHandler(Filters.text, tag,pass_user_data=True)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )
conv_handler2 = ConversationHandler(
    entry_points=[CommandHandler('update', update)],
    states={
           1: [MessageHandler(Filters.text, choosedOffer, pass_user_data=True)],
           2: [MessageHandler(Filters.text, pathOffer, pass_user_data=True)],
           3: [MessageHandler(Filters.text, nameUpdate, pass_user_data=True)],
           4: [MessageHandler(Filters.photo, photoUpdate, pass_user_data=True)],
           5: [MessageHandler(Filters.text, descrUpdate, pass_user_data=True)],
           6: [MessageHandler(Filters.text, tagUpdate, pass_user_data=True)],
           7: [MessageHandler(Filters.text, deleteOffer, pass_user_data=True)],
        },
    fallbacks=[CommandHandler('cancel', cancel)],
)
conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler('review', review)],
    states={
           1: [MessageHandler(Filters.text, showRes, pass_user_data=True)],
        },
    fallbacks=[CommandHandler('cancel', cancel)],
)
        
def hello(update, context: CallbackContext) -> None:
    update.message.reply_text(f'Приветик {update.effective_user.first_name}')

def ping(update, context: CallbackContext) :
    update.message.reply_text(f'Pong')
    update.message.reply_text(f'It took' )
    
updater = Updater('Enter Your Token')

dp = updater.dispatcher

dp.add_handler(conv_handler)
dp.add_handler(conv_handler2)
dp.add_handler(conv_handler3)
dp.add_handler(CommandHandler('hello', hello))
dp.add_handler(CommandHandler('start', start))
dp.add_handler(CommandHandler('ping', ping))

# text_handler = MessageHandler (Filters.text, echo)
# dp.add_handler(text_handler)

updater.start_polling()
updater.idle()
con.close()

