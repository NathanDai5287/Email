from getpass import getpass
import scrypt
import pickle

password = scrypt.hash(getpass('Passwsord: '), 'random salt')

with open('password.pkl', 'wb') as f:
	pickle.dump(password, f)
