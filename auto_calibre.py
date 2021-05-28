##all together
import telebot
from libgen_api import LibgenSearch
import requests
import wget
from bs4 import BeautifulSoup
import os
from capybre import convert
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



API_KEY = '501182282:AAH8yf5rehcqk1IImi4ACM5rPM-RPkOGpFs'
bot = telebot.TeleBot(API_KEY)
list_feasible =[]
@bot.message_handler()
def greet(message):
    global list_feasible
    command = message.text[0:5]
    title = message.text[6:]
    chat_id = message.chat.id
    if command == "/book":
        bot.reply_to(message, "I will search the book name: "+ title)
        list_feasible = search(title)
        #tell the user what are the possible options 
    
        for i in range(len(list_feasible)):
            option ="id: "+str(i)+" title: "+list_feasible[i]['Title'] +" author: "+ list_feasible[i]['Author'] +" file_type: "+list_feasible[i]['Extension']
            bot.send_message(chat_id, option)
    elif command == "/down":
        name = download(title)
        bot.reply_to(message, "the requested book has been downloaded")
        new_name = list_feasible[int(title)]['Title']
        os.rename(name,new_name+name[-5:])
        convert(new_name+name[-5:], as_ext='mobi')
        list_feasible =[]
        send_email(new_name+".mobi")
def search(title):
    s = LibgenSearch()
#search in descending order of extension later
    results = s.search_title(title)
    global list_feasible
    for i in range(len(results)):
        if results[i]['Extension'] in ['epub','mobi','azw3']:
            list_feasible.append(results[i])
    return(list_feasible)

def download(index):
    global list_feasible
    mirror_url = list_feasible[int(index)]["Mirror_1"]
    mirror_request = requests.get(mirror_url,verify =False, timeout =5)
    soup = BeautifulSoup(mirror_request.content, 'html.parser')
    online_file =soup.findChild("a")['href']
    print(online_file)
    wget.download(online_file)
    current_name = online_file.split("/")[-1]
    return(current_name)

def send_email(name):
    
    subject = "An email with attachment from Python"
    body = "This is an email with attachment sent from Python"
    sender_email = "aneeskindle@gmail.com"
    receiver_email = "ANEES870_SCL0RT@KINDLE.COM"
    password = "treelover123"

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = name  # In same directory as script

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

bot.polling()
