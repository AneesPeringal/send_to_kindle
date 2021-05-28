import pickle
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

class User:
    def __init__(self, chat_id="", kindle_email=""):
        
        self.chat_id = chat_id
        self.kindle_email = kindle_email
        self.no_books = 0
        self.list_feasible=[]
        self.title=''
        self.book_id =-1
        
    def read_details(self):
        print(self.chat_id)
        print(self.kindle_email)
        print(self.no_books)
        
    def add_book(self,title):
        self.no_books=self.no_books+1
        self.books.apped(title)
        
    def search(self):
        s = LibgenSearch()
        results =s.search_title(self.title)
        
        for i in range(len(results)):
            if results[i]['Extension'] in ['epub','mobi','azw3']:
                self.list_feasible.append(results[i])
        
    def download(self):
        mirror_url = self.list_feasible[self.book_id]["Mirror_1"]
        mirror_request = requests.get(mirror_url,verify =False, timeout =5)
        soup = BeautifulSoup(mirror_request.content, 'html.parser')
        online_file =soup.findChild("a")['href']
        print(online_file)
        wget.download(online_file)
        current_name = online_file.split("/")[-1]
        return(current_name)

    def send_email(self):
    
        subject = "An email with attachment from Python"
        body = "This is an email with attachment sent from Python"
        sender_email = "aneeskindle@gmail.com"
        receiver_email = self.kindle_email
        password = "treelover123"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = self.title+".mobi"  # In same directory as script

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

            
file1 = open('database.log','rb')
user = User()
try:
    while True:
        user = pickle.load(file1)
        print(user.chat_id)
except EOFError:
    print("file ended")
