import telebot
import random
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode






bot=telebot.TeleBot("5073492003:AAHk453E3wfm_kloCVkTDQyjhRGYOTlrzZQ")

@bot.message_handler(commands=['start'])
def hello(message):
    bot.reply_to(message,message.chat.first_name +"welcome my bot")


@bot.message_handler(commands = ['help'])
def help(message):
    bot.reply_to(message, """/start
خوش‌آمد گویی!
/game
میتونیم باهم بازی حدس اعداد رو انجام بدیم.
/age
تاریخ تولدت رو به شکل 1378/7/30وارد کن تا سن دقیقت رو بهت بگم

/voice
هر جمله انگلیسی که دوست داری وارد کن تا ویس اون جمله رو بهت بدم😎
/max
آرایه به فرمت "14,7,78,15,8,19,20" وارد کن،تا بزرگ ترین عدد رو بهت بگم
/argmax
یدونه آرایه به فرمت"14,7,78,15,8,19,20" وارد کن تا من بهت معرفی کنم که بزرگ ترین عدد توی کدوم خونه قایم شده
/qrcode
متن خودت رو وارد کن من بهت بارکد اون متن رو میدم
/help
برای راهنمایی دستورات اینجا هستم""")


@bot.message_handler(commands = ['game'])
def game(message):
    global random_number
    random_number = random.randint(1, 100)
    user_message = bot.send_message(message.chat.id, "قراره یه عدد بین 1 تا 100 رو حدس بزنی. حالا حدست رو وارد کن.")
    bot.register_next_step_handler(user_message, game_helper)

markup = telebot.types.ReplyKeyboardMarkup(row_width = 1)
button = telebot.types.KeyboardButton("new game")
markup.add(button)

def game_helper(message):
    global random_number
        
    if message.text == "new game":
            random_number = random.randint(1, 100)
            user_message = bot.send_message(message.chat.id, "دوباره بازی رو شروع می‌کنیم. حدست رو وارد کن.")
            bot.register_next_step_handler(user_message, game_helper)

    elif int(message.text) < random_number:
            user_message = bot.send_message(message.chat.id, "برو بالا", reply_markup = markup)
            bot.register_next_step_handler(user_message, game_helper)

    elif int(message.text) > random_number:
            user_message = bot.send_message(message.chat.id, "برو پایین", reply_markup = markup)
            bot.register_next_step_handler(user_message, game_helper)

    elif int(message.text) == random_number:
            bot.send_message(message.chat.id, "برنده شدی!", reply_markup = telebot.types.ReplyKeyboardRemove(selective = True))
            


@bot.message_handler(commands = ['age'])
def age(message): 
 HBD=bot.send_message(message.chat.id, "تاریخ تولدت رو با فرمت \"1378/7/30\" وارد کن.")
 bot.register_next_step_handler( HBD ,age)

def age(message):
    bd = message.text.split("/")
    age = JalaliDatetime.now() - JalaliDatetime(bd[0] , bd[1] , bd[2] )
    bot.send_message(message.chat.id , age )

bot.infinity_polling()


@bot.message_handler(commands = ['voice'])
def voice(message):
    user_message = bot.send_message(message.chat.id, "هر جمله انگلیسی که دوست داری وارد کن تا ویس اون جمله رو بهت بدم")
    bot.register_next_step_handler(user_message, voice_maker)

def voice_maker(message):
    try:
        language = "en"
        message_voice = gTTS(text = message.text, lang = language, slow = False)
        message_voice.save("voice.mp3")
        voice_file = open("voice.mp3", "rb")
        bot.send_voice(message.chat.id, voice_file)
    except:
        user_message = bot.send_message(message.chat.id, "فقط متن وارد کن نه چیز دیگه!")
        bot.register_next_step_handler(user_message, voice_maker)



@bot.message_handler(commands='max')
def Max(message):
    arr = bot.reply_to(message ,"آرایه به فرمت 14,7,77,15,8,19,20 وارد کن تا بزرگ ترین عدد رو بهت بگم")
    bot.register_next_step_handler(arr , findMax )

def findMax(message) :
    arr = message.text.split(',')
    maxNum = max(arr)
    bot.send_message(message.chat.id ,  maxNum)


@bot.message_handler(commands='argmax')
def MaxIndex(message):
    arr= bot.send_message(message.chat.id,"یک آرایه به فرمت 14,7,78,15,8,19,20 وارد کن تا من بهت بگم بزرگ ترین عدد داخل کدام خانه قایم شده")
    bot.register_next_step_handler(arr , findMaxIndex)
def findMaxIndex(message) :
    arr = message.text.split(',')
    maxNumIndex = arr.index(max(arr))
    bot.send_message(message.chat.id ,  maxNumIndex)


@bot.message_handler(commands=['qrcode'])
def text_to_qrcode(message):
    bot.reply_to(message,"لطفا متن مورد نظرت رو وارد کن :") 
    bot.register_next_step_handler(message ,toqrcode)
    
def toqrcode(message):
    img = qrcode.make(message) 
    img.save("qrcode.png")
    photo = open("qrcode.png", 'rb')
    bot.send_photo(message.chat.id, photo)


bot.infinity_polling() 




