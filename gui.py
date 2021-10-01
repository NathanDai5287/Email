import os

import pandas as pd

from tkinter import *

import smtplib, ssl
from email.mime.text import MIMEText

import pyperclip
import pickle
from getpass import getpass
import scrypt

with open('password.pkl', 'rb') as f:
	password = pickle.load(f)

class Gui(Frame):
	def __init__(self, master: Tk):
		super().__init__(master)

		self.port = 465  # For SSL
		self.email = os.environ['email']
		self.password = os.environ['email_password']
		self.context = ssl.create_default_context()
		self.df = pd.read_csv('members.csv', comment='#')
		# self.df = pd.read_csv('test.csv')
		self.recipients = self.df['Email'].tolist()
		print(self.recipients)

		self.grid()

		self.root = master

		self.subject = Text(self, undo=True, width=40, height=1)
		self.subject.grid()

		self.body = Text(self, undo=True, height=20, width=70, wrap=WORD)
		self.body.grid()
		self.send = Button(self, text="Send", command=self.send)
		self.send.grid()

	def send(self):
		subject = self.subject.get(1.0, END).strip('\n')
		body = self.body.get(1.0, END).rstrip('\n')

		message = MIMEText(body)
		message['Subject'] = subject
		message['From'] = self.email
		message['To'] = ', '.join(self.recipients)

		guess = scrypt.hash(getpass('Password: '), 'random salt')

		if (guess == password):
			with smtplib.SMTP_SSL('smtp.gmail.com', self.port, context=self.context) as server:
				server.login(self.email, self.password)
				server.sendmail(self.email, self.recipients, message.as_string())

			print('Email sent!')

			pyperclip.copy(body)
			self.root.destroy()
		else:
			print('Incorrect password!')

root = Tk()
root.title('Send Emails')
gui = Gui(root)
gui.mainloop()
