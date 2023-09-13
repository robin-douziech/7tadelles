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

def register_view(request, current_view, real_view) :

	request.session['last_view'] = current_view
	if real_view :
		request.session['last_real_view'] = request.session.get('last_real_view', [])
		if len(request.session['last_real_view']) > 0 :
			if request.session['last_real_view'][-1] != current_view :
				request.session['last_real_view'].append(current_view)
		else :
			request.session['last_real_view'] = [current_view]

		if len(request.session['last_real_view']) > 10 :
			request.session['last_real_view'] = request.session['last_real_view'][-10:]

	print(f"last_view      : {request.session['last_view']}")
	print(f"last_real_view : {request.session['last_real_view']}")