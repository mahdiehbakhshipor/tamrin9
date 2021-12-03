import time
import telebot
import qrcode
import random
import datetime
from telebot import types
from gtts import gTTS
from telebot.types import Message
from time import sleep


def hejri_to_miladi(jy, jm, jd):
    jy += 1595
    days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
    if (jm < 7):
        days += (jm - 1) * 31
    else:
        days += ((jm - 7) * 30) + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if (days > 36524):
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if (days >= 365):
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if (days > 365):
        gy += ((days - 1) // 365)
        days = (days - 1) % 365
    gd = days + 1
    if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while (gm < 13 and gd > sal_a[gm]):
        gd -= sal_a[gm]
        gm += 1
    return [gy, gm, gd]




bot = telebot.TeleBot("5060949802:AAFwGxcjQstW4NdNHx6AxHvCfN6pJTz_Tmg")


@bot.message_handler(commands=['start'])
def welcome(massage):
    bot.reply_to(massage, "سلام خوش اومدی عزیزه دل "+massage.fram_user.first_name)

@bot.message_handler(commands=['help'])
def komak(massage):
    bot.reply_to(massage,""""
    /game - بازی حدس اعداد
    /voice - متن را به صدا تبدیل کن
    /max - بزرگترین عدد را حدس بزن
    /age - سن راا محاسبه کن
    /argmax - اندیس بزرگترین مقدار آرایه را چاپ کن
    /qrcode - qrcode را چاپ کن""")

@bot.message_handler(commands=['game'])
def game(massage):
    random_number =random.randint(0,50)
    guess_number = bot.send_massage(massage.chat.id,"""قوانین بازی را مطالعه کن:1:لطفا اعداد صحیح وارد بشود
    2:صبر کن تا بات جواب بده بعد دوباره پیام بده
    3:برای شروع دوباره دکمه استارت رو بزن
    4:از اینکه مارو انتخاب کردی چاکرتیم بیا شروع کنیم...""")


    time.sleep(5)
    guess_number = bot.send_message(massage.chat.id, "بازی شروع شد عدد را وارد کنید")
    bot.register_next_step_handler(guess_number, guess_number_game,random_number)

def guess_number_game(number,random_number):
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    exitButton = types.KeyboardButton('خروج از بازی')
    button = telebot.types.KeyboardButton('شروع دوباره')
    markup.add(button,exitButton)
    if number.text == 'خروج از بازی':
        markup = telebot.types.ReplyKeyboardRemove(selective=True)
        button = telebot.types.ReplyKeyboardRemove(selective=True)
        exitButton = telebot.types.ReplyKeyboardRemove(selective=True)
        bot.send_message(number.chat.id, "خب عزیز خارج شدی یک کامند دیگر انتخاب کن", reply_markup=markup)

    elif number.text == 'شروع دوباره':
        random_number = random.randint(0,50)
        bot.send_message(number.chat.id, "بازی شروع شد عدد را وارد کنید", reply_markup=markup)
        bot.register_next_step_handler(number, guess_number_game,random_number)
    
    else:
        try:
            if int(number.text) == random_number:
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                button = telebot.types.ReplyKeyboardRemove(selective=True)
                exitButton = telebot.types.ReplyKeyboardRemove(selective=True)
                bot.send_message(number.chat.id,"🏆آخجون برنده شدی داداچ", reply_markup=markup)
            elif int(number.text) == random_number - 1:
                bot.send_message(number.chat.id,"بالاتر", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
            elif int(number.text) < random_number:
                bot.send_message(number.chat.id,"نه دیگه نشد هنوزم بالاتر", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
            elif int(number.text) == random_number + 1:
                bot.send_message(number.chat.id,"پایین تر", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
            elif int(number.text) > random_number:
                bot.send_message(number.chat.id,"شرمنده!بازم پایین تر", reply_markup=markup)
                bot.register_next_step_handler(number, guess_number_game,random_number)
        except:
            number = bot.send_message(number.chat.id," لطفا فقط عدد صحیح وارد کن", reply_markup=markup)
            bot.register_next_step_handler(number, guess_number_game,random_number)

  

@bot.message_handler(commands=['age'])
def cal_age(message):
    b_day = bot.send_message(message.chat.id,"""لطفا تاریخ تولد مورد نظر را مانند نمونه به شمسی وارد کنید1377/09/18""")
    bot.register_next_step_handler(b_day, calculate_age)

def calculate_age(b_day):
    try:
        now = datetime.datetime.now()
        today = []
        temp = []
        today.append(int(now.year))
        today.append(int(now.month))
        today.append(int(now.day))
        text = b_day.text
        text = text.split("/")
        temp.append(int(text[0]))
        temp.append(int(text[1]))
        temp.append(int(text[2]))
        miladi_birthday_user = hejri_to_miladi(temp[0],temp[1],temp[2])
        if miladi_birthday_user[2] > today[2]:
            if miladi_birthday_user[2] > today[2]:
                today[0] -= 1
                today[1] += 11
                today[2] += 30
        elif miladi_birthday_user[1] > today[1]:
            today[0] -= 1
            today[1] += 12
        age_year = today[0] - miladi_birthday_user[0]
        age_month = today[1] - miladi_birthday_user[1]
        age_day = today[2] - miladi_birthday_user[2]
        if age_month > 12 :
            age_month -= 12
            age_year += 1
        age_h = now.hour
        age_min = now.minute
        age_sec = now.second
        
        AGETXT = "سن شما " + str(age_year) + " سال و " + str(age_month) + " ماه و " + str(age_day) + " روز و " + str(age_h) + " ساعت و " + str(age_min) + " دقیقه و " + str(age_sec) + "ثانیه است ."
        
        bot.send_message(b_day.chat.id,AGETXT)
    except:
        b_day = bot.send_message(b_day.chat.id,"اشتبااااه!دوبارع تلاش کنید")
        bot.register_next_step_handler(b_day, calculate_age)


        @bot.message_handler(commands=['voice'])
        def voice(message):
          user_voice = bot.send_message(message.chat.id , 'لطفا متن رو به انگلیسی وارد کن تا تبدیل به ویس کنم واست ')
          bot.register_next_step_handler(user_voice , voice_creating)

def voice_creating(user_voice):
    convert = gTTS(text = user_voice.text , lang = 'en' , slow = True)
    convert.save('voice.wma')
    convert = open('voice.wma' , 'rb')
    bot.send_voice(user_voice.chat.id , convert )


@bot.message_handler(commands=['max'])
def maximum(message):
    arry = bot.send_message(message.chat.id , 'مانند مثال چند تا عدد بگو تا بزرگترینشون رو واست حدس بزنم : [1,10,100,50,...]')
    bot.register_next_step_handler(arry , max_searching)

def max_searching(arry):  
    temp = list(map(int, arry.text.split(',')))
    number = max(temp)
    bot.send_message(arry.chat.id , number)
    
@bot.message_handler(commands=['argmax'])
def argmax_command(message):
    msg = bot.reply_to(message, "آرایه را به فرمت [x,x,x,x] بدون براکت وارد کنید")
    bot.register_next_step_handler(msg, print_argmax)


def print_argmax(message):
    chat_id = message.chat.id
    try:
        text = message.text

        array = [int(x) for x in text.split(',')]
        bot.send_message(chat_id, 'اندیس ماکسیمم آرایه عدد زیر است')
        bot.send_message(chat_id, str(array.index(max(array))))
    except Exception as e:
        bot.send_message(chat_id, 'اوووه خطااا، بار دیگر دستور رو وارد کنید!')
        
@bot.message_handler(commands=['qrcode'])
def get_qrcode(message):
    qr_code = bot.send_message(
        message.chat.id, 'لطفا برام یک متن  بفرست تا تبدیلش کنم به کد کیو آر :')
    bot.register_next_step_handler(qr_code, make_qrcode)

def make_qrcode(message):
    try:
        qrcode_image = qrcode.make(message.text)
        qrcode_image.save('QR-Code.jpg')
        photo = open('QR-Code.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    
    except:
        qr_code = bot.send_message(message.chat.id, 'فقط متن!')
        bot.register_next_step_handler(qr_code, make_qrcode)




 
  

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
	     bot.reply_to(message, "متاسفم!نمیفهمم چی داری میگی؟!دوباره تلاش کن")


bot.infinity_polling()