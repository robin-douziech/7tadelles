import random, os
from account import models

def generate_token(length) :

	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	token = ""
	for i in range(length) :
		token += alphabet[random.randint(0, len(alphabet)-1)]

	return token

def find_user_by_email(email) :

	for user in models.User.objects.all() :
		if user.email == email :
			return user

	return None

def delete_media_file(path) :
	try :
		if os.path.isfile(path) :
			os.remove(path)
			return True
		else :
			return False
	except Exception as e :
		print(f"Erreur lors de la suppression d'un fichier media : {str(e)}")
		return False