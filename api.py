import win32com.client
import os
import openai
from config import openai_apikey
from config import news_apikey
from config import weather_apikey
import speech_recognition as sr
openai.api_key=openai_apikey

def translate():
    from easygoogletranslate import EasyGoogleTranslate
    translator=EasyGoogleTranslate(source_language='auto',target_language='hi',timeout=10)
    say("Tell the text you want to translate")
    text=takecommand()
    result=translator.translate(text)
    print(result)
    
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold=1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            say("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said : {query}")
            return query
        except Exception as e:
            return "Some error occurred Sorry from JARVIS"

def say(text):
    # print("Enter the word you want to speak it out by computer ")
    # s=input()
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def news():
    import requests
    url = 'https://newsapi.org/v2/top-headlines'
    params = {'country': 'in', 'apiKey': news_apikey }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_json = response.json()

        def display_headlines(news_data):
            articles = news_data.get('articles', [])

            if articles:
                for i, article in enumerate(articles, start=1):
                    print(f"{i}. {article['title']} - {article['url']}")
                    say(f"{i}. {article['title']}")
            else:
                print("No articles found.")
        display_headlines(response_json)
    else:
        print(f"Error: {response.status_code} - {response.text}")

def weather():
    import requests
    api_key = weather_apikey
    base_url = 'http://api.weatherapi.com/v1/current.json?'
    say("Tell city name:")
    city_name = takecommand()
    complete_url = base_url + 'key=' + api_key + '&q=' + city_name
    response = requests.get(complete_url)
    if response.status_code == 200:
        data = response.json()
        print(f"Weather in {city_name}:")
        print(f"localtime: {data['location']['localtime']}")
        print(f"Temperature: {data['current']['temp_c']}°C")
        print(f"Condition: {data['current']['condition']['text']}")
        print(f"Humidity: {data['current']['humidity']}%")
        print(f"Wind speed: {data['current']['wind_kph']}km/hr")
        say(f"Weather in {city_name}:")
        say(f"localtime: {data['location']['localtime']}")
        say(f"Temperature: {data['current']['temp_c']}°C")
        say(f"Condition: {data['current']['condition']['text']}")
        say(f"Humidity: {data['current']['humidity']}%")
        say(f"Wind speed: {data['current']['wind_kph']}km/hr")
    else:
        print(f"Error {response.status_code}: {response.text}")

def generatechatresponse(prompt):
    messages=[]
    messages.append({"role":"system","content":"You are a helpful assistant."})
    question={}
    question['role']='user'
    question['content']=prompt
    messages.append(question)
    text=""
    text += str(question['content']+'?')
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    try:
        answer=response['choices'][0]['message']['content']
        text+=f"\n {answer}"
        if not os.path.exists("memory"):
            os.mkdir("memory")
        with open(f"ai voice/memory/{prompt}.txt", "w") as file:
            file.write(text)
    except:
        answer='oops something went wrong'
    return answer

def stock():
    import yfinance as yf
    say("Enter symbol of company name")
    symbol = input("Enter symbol of company name with `.NS`: ")
    stock_data = yf.download(symbol, start='2023-11-10')
    print(stock_data.head())

def playonyt():
    import pywhatkit
    say("Enter the topic you want to play")
    topic=takecommand()
    say(f"Playing {topic} on youtube")
    pywhatkit.playonyt(topic)

def whatsapp():
    import pywhatkit
    say("Enter the phone number with country code")
    phone=input("Enter receiver's phone number with country code : ")
    say("Tell the message you want to send")
    message=takecommand()
    say("Tell the hour")
    hour=int(takecommand())
    say("Tell the minute")
    min=int(takecommand())
    pywhatkit.sendwhatmsg(phone,message,hour,min)

def takenotes():
    say("Taking notes...")
    with open("notes.txt", "a") as file:
        while True:
            say("Enter the note you want to take")
            note = takecommand()
            if note == "stop":
                break
            file.write(note + "\n")
    say("Notes taken successfully")
    print("Notes taken successfully")

def email():
    import smtplib
    ob = smtplib.SMTP('smtp.gmail.com', 587)
    ob.starttls()
    # remember to give authoriztion to the gmail account
    say("Enter your gmail:")
    gmail = input("Enter your gmail id: ")
    say("Enter your password:")
    password = input("Enter your password: ")
    ob.login(gmail, password)
    say("Tell the subject of your mail:")
    subject = takecommand()
    say("Tell the body of your mail:")
    body = input("Enter the body of your mail: ")
    message = "Subject:{}\n\n{}".format(subject, body)
    say("Check it sir")
    print(message)
    add = []
    say("Enter the number of users:")
    users_count = int(input("Enter the number of users: "))

    for i in range(users_count):
        say("Enter the recipient gmail id:")
        usergmail = input("Enter the recipient gmail id: ")
        add.append(usergmail)

    to_addrs = ', '.join(add)
    say("Sending...")
    ob.sendmail(gmail, add, message)
    say("Email successfully sent")
    print("Email successfully sent")
    ob.quit()