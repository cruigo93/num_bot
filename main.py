import telebot
import random
import speech_recognition as sr
import soundfile as sf
import subprocess
import os
import config

bot = telebot.TeleBot(config.TOKEN)
num_dict = {}
r = sr.Recognizer()
def generate_num():
    num = random.randint(1000, 9999)
    return num
@bot.message_handler(commands=['start'])
def start_messaging(message):
    num = generate_num()
    num_dict[message.chat.id] = num
    bot.send_message(message.chat.id, f"Ваше число {num}")

@bot.message_handler(content_types=['voice'])
def get_audio(message):

    num = num_dict[message.chat.id]

    file_info = bot.get_file(message.voice.file_id)
    # print(file_info)
    downloaded_file = bot.download_file(file_info.file_path)
    # print(downloaded_file)
    with open('test.wav', 'wb') as new_file:
        new_file.write(downloaded_file)
    os.remove("test2.wav")
    process = subprocess.run(['ffmpeg', '-i', 'test.wav', 'test2.wav'])
    print(f"Chat {message.chat.id} save wav")

    with sr.AudioFile('test2.wav') as source:
        audio = r.record(source)
    
    try:
        n_client = r.recognize_google(audio, language="ru_RU")
        n_client = "".join(n_client.split())
        print(n_client)
        # print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language="ru_RU"))
        if n_client == str(num):
            bot.send_message(message.chat.id, f"Спасибо, вы продиктовали {num}!")
        else:
            bot.send_message(message.chat.id, f"Мы не смогли распознать запись с числом {num}!")
            num = generate_num()
            num_dict[message.chat.id] = num
            
            bot.send_message(message.chat.id, f"Ваше число {num}!")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    
    # num = num_dict[message.chat.id]
    # if message.text == str(num):
    #     bot.send_message(message.chat.id, f"Спасибо, вы продиктовали {num}!")
    # else:
    #     num = generate_num()
    #     num_dict[message.chat.id] = num
    #     bot.send_message(message.chat.id, f"Ваше число {num}!")
    

bot.polling()