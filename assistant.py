import win32com.client
import webbrowser
import subprocess
import datetime
import openai
from api import generatechatresponse
from api import news
from api import weather
from api import stock
from api import translate
from api import takecommand
from api import say
from api import playonyt
from api import whatsapp
from api import email
from api import takenotes

def chat(user):
    charstr= ""
    messages=[]
    messages.append({"role":"system","content":"You are a helpful assistant."})
    question={}
    charstr+=f" Sujal: {user}\n Jarvis: "
    print(charstr,end="")
    question['role']='user'
    question['content']=user
    messages.append(question)
    response=openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=messages)
    try:
        answer=response['choices'][0]['message']['content']
        charstr+=f"{answer}\n"
    except:
        answer='oops something went wrong'
    return answer
 
if __name__ == '__main__':
    say("Hello I am JARVIS AI ")
    while True:
        print("Listening...")
        say("Listening...")
        query = takecommand()
        # query=input("enter :")
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],["github", "https://github.com/"],["chatgpt", "https://chat.openai.com/"]]
        for site in sites:
            if site[0].lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        if "time" in query.lower():
            timenow = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir the time is {timenow}")
        elif "artificial intelligence" in query.lower():
                say("tell me the question")
                question=takecommand()
                ans=generatechatresponse(question)
                print(ans)
                say(ans)
        elif "chatting" in query.lower():
            while True:
                say("Tell :")
                # user=input()
                user=takecommand()
                if "stop" in user.lower():
                    say("Thank you for chatting with me")
                    print("Thank you for chatting with me")
                    exit()
                output=chat(user)
                print(output)
                say(output)
        
        elif "news" in query.lower():
            news()
        elif "weather" in query.lower():
            weather()
        elif "stock" in query.lower():
            stock()
        elif "translate" in query.lower():
            translate()
        elif "on youtube" in query.lower():
            playonyt()
        elif "message" in query.lower():
            whatsapp()
        elif "send email" in query.lower():
            email()
        elif "note" in query.lower():
            takenotes()
        elif "stop" in query.lower():
            exit()
